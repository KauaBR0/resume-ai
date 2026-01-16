import json
import logging
import requests
from typing import List
from app.core.config import settings
from app.models.schemas import CandidateAnalysis, RankedCandidate

logger = logging.getLogger(__name__)

# Using a reliable model capable of JSON instruction following
MODEL_NAME = "openai/gpt-3.5-turbo" 

def analyze_resume_with_llm(resume_text: str, job_description: str) -> CandidateAnalysis:
    """
    Sends resume text and job description to LLM to extract structured data.
    """
    
    prompt = f"""
    You are an expert HR Recruiter. Extract information from the Resume below and match it against the Job Description.
    
    JOB DESCRIPTION:
    {job_description}
    
    RESUME TEXT:
    {resume_text}
    
    RULES FOR SENIORITY (Based on years of experience):
    - JUNIOR: 0 to 2 years
    - PLENO: 2 to 5 years
    - SENIOR: 5+ years
    
    Return a JSON object strictly adhering to this structure:
    {{
        "full_name": "string",
        "email": "string or null",
        "phone": "string or null",
        "years_of_experience": float,
        "skills": ["skill1", "skill2"],
        "last_role": "string or null",
        "companies": ["company1", "company2"],
        "education": [{{"institution": "string", "degree": "string", "field": "string"}}],
        "seniority": "JUNIOR" | "PLENO" | "SENIOR",
        "summary": "string",
        "strengths": ["string"],
        "weaknesses": ["string"],
        "match_score": float (0-100 based on job fit),
        "ranking_justification": "string explaining the score"
    }}
    
    Calculate years_of_experience based on work history. Assign seniority strictly according to the rules above.
    """

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Automatiz/ResumeAnalyzer", 
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        content = data['choices'][0]['message']['content']
        
        # Parse JSON and validate with Pydantic
        parsed_data = json.loads(content)
        return CandidateAnalysis(**parsed_data)
        
    except Exception as e:
        logger.error(f"LLM Analysis failed: {e}")
        # Return a dummy/empty analysis in case of failure to avoid crashing the whole batch
        return CandidateAnalysis(
            full_name="Unknown (Parse Error)",
            years_of_experience=0,
            skills=[],
            companies=[],
            seniority="JUNIOR",
            summary=f"Failed to process resume: {str(e)}",
            strengths=[],
            weaknesses=[]
        )

def generate_consolidated_report(ranked_candidates: List[RankedCandidate], job_description: str) -> str:
    """
    Generates a final text recommendation based on the ranking.
    """
    candidates_summary = "\n".join([
        f"{c.rank}. {c.candidate.full_name} (Score: {c.score}, Seniority: {c.candidate.seniority})\n   Strengths: {', '.join(c.candidate.strengths)}"
        for c in ranked_candidates
    ])

    prompt = f"""
    Analyze this list of ranked candidates for the following Job Description:
    
    JOB DESCRIPTION:
    {job_description}
    
    RANKED CANDIDATES:
    {candidates_summary}
    
    Write a professional hiring recommendation (in Portuguese) summarizing who should be interviewed and why.
    """
    
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Automatiz/ResumeAnalyzer",
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Could not generate recommendation: {str(e)}"
