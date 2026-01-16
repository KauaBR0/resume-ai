import os
import logging
from typing import List, Dict, Any
from app.core.celery_app import celery_app
from app.services.pdf_service import extract_text_from_pdf
from app.services.llm_service import analyze_resume_with_llm, generate_consolidated_report
from app.services.ranking_service import rank_candidates
from app.models.schemas import CandidateAnalysis, ConsolidatedReport

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5}, retry_backoff=True)
def process_resume_task(self, file_path: str, job_description: str) -> Dict[str, Any]:
    """
    Task to process a single resume: Read PDF -> Extract Text -> Analyze with LLM.
    Retries automatically on exceptions (e.g., LLM timeout).
    """
    try:
        logger.info(f"Processing file: {file_path}")
        
        # Read file from disk
        with open(file_path, "rb") as f:
            content = f.read()
        
        # 1. Extract Text
        text = extract_text_from_pdf(content)
        if not text:
            # If plain text fails, we might just log and return empty analysis 
            # instead of retrying forever if the PDF is truly broken.
            logger.warning(f"Empty text extracted from {file_path}")
            raise ValueError("Could not extract text from PDF")

        # 2. Analyze with LLM
        analysis = analyze_resume_with_llm(text, job_description)
        
        # Cleanup file after processing
        try:
            os.remove(file_path)
        except OSError:
            pass # Best effort cleanup

        # Return dict representation for Celery serialization
        return analysis.model_dump()

    except Exception as e:
        logger.error(f"Task failed for {file_path}: {e}")
        # Re-raise to trigger auto-retry mechanism provided by Celery decorator
        raise self.retry(exc=e)

@celery_app.task
def consolidate_results_task(results: List[Dict[str, Any]], job_description: str) -> Dict[str, Any]:
    """
    Task to receive all analyzed resumes, rank them, and generate the final report.
    """
    # Convert dicts back to Pydantic models
    analyses = [CandidateAnalysis(**res) for res in results]
    
    # 1. Rank
    ranked_candidates = rank_candidates(analyses)
    
    # 2. Generate Text Recommendation
    recommendation = generate_consolidated_report(ranked_candidates, job_description)
    
    # 3. Create Final Report
    report = ConsolidatedReport(
        job_description=job_description[:100] + "...", # Truncate for display
        total_candidates=len(analyses),
        ranking=ranked_candidates,
        recommendation=recommendation
    )
    
    return report.model_dump()
