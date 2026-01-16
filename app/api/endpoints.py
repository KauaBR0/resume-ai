import os
import shutil
import uuid
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from celery.result import AsyncResult
from celery import chord

from app.tasks.worker import process_resume_task, consolidate_results_task
from app.models.schemas import TaskResponse, TaskStatus

router = APIRouter()

TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@router.post("/analyze", response_model=TaskResponse)
async def analyze_resumes(
    files: List[UploadFile] = File(...),
    job_description: str = Form(...)
):
    """
    Upload multiple resumes (PDF) and a job description to start the analysis process.
    """
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="Please upload at least 2 resumes.")
    
    saved_paths = []
    
    try:
        # Save files to disk for workers to access
        for file in files:
            if not file.filename or not file.filename.lower().endswith(".pdf"):
                continue # Skip non-pdf or files with no name
            
            # Create unique filename to avoid collisions
            unique_name = f"{uuid.uuid4()}_{file.filename}"
            file_path = os.path.join(TEMP_DIR, unique_name)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            saved_paths.append(file_path)
            
        if not saved_paths:
            raise HTTPException(status_code=400, detail="No valid PDF files uploaded.")

        # Create Celery Workflow (Chord)
        # 1. Header: Group of parallel tasks
        task_group = [
            process_resume_task.s(path, job_description) # type: ignore
            for path in saved_paths
        ]
        
        # 2. Body: Callback task to run after group finishes
        workflow = chord(task_group)(consolidate_results_task.s(job_description)) # type: ignore
        
        return TaskResponse(
            task_id=workflow.id,
            status="PROCESSING",
            message=f"Started analysis of {len(saved_paths)} resumes."
        )

    except Exception as e:
        # Cleanup if something fails during dispatch
        for path in saved_paths:
            if os.path.exists(path):
                os.remove(path)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/result/{task_id}", response_model=TaskStatus)
async def get_result(task_id: str):
    """
    Check the status of the analysis task and retrieve results.
    """
    task_result = AsyncResult(task_id)
    
    if task_result.state == 'PENDING':
        return TaskStatus(task_id=task_id, status="PENDING")
    elif task_result.state == 'FAILURE':
        return TaskStatus(task_id=task_id, status="FAILED", result=None)
    elif task_result.state == 'SUCCESS':
        return TaskStatus(
            task_id=task_id, 
            status="COMPLETED", 
            result=task_result.result
        )
    else:
        return TaskStatus(task_id=task_id, status=task_result.state)
