from fastapi import APIRouter, HTTPException
from uuid import uuid4
from pathlib import Path
import json
from datetime import datetime
from typing import Optional

from app.models.job import JobRequest, JobResponse, JobStatus
from app.services import job_service

router = APIRouter()

# Directory for persistent job storage
JOBS_DIR = Path("jobs")
JOBS_DIR.mkdir(exist_ok=True)


def job_file_path(job_id: str) -> Path:
    return JOBS_DIR / f"{job_id}.json"


def save_job(job_id: str, data: dict):
    # Ensure status is stored as string for JSON
    if isinstance(data.get("status"), JobStatus):
        data["status"] = data["status"].value

    data["updated_at"] = datetime.utcnow().isoformat()
    with job_file_path(job_id).open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_job(job_id: str) -> Optional[dict]:
    path = job_file_path(job_id)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
        # Cast status back to JobStatus Enum
        if "status" in data:
            data["status"] = JobStatus(data["status"])
        return data


@router.post("/", response_model=JobResponse)
async def create_job(request: JobRequest):
    if not request.file_id:
        raise HTTPException(status_code=400, detail="file_id is required")

    job_id = str(uuid4())
    job_data = {
        "job_id": job_id,
        "file_id": request.file_id,
        "status": JobStatus.PENDING,
        "result_path": None,  # pointer to results file, set later
        "created_at": datetime.utcnow().isoformat(),
    }

    save_job(job_id, job_data)

    # Trigger async job (dummy for now)
    # inside create_job
    job_service.process_job(job_id, request.file_id, save_job, load_job)


    return JobResponse(job_id=job_id, status=JobStatus.PENDING)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    job = load_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobResponse(
        job_id=job["job_id"],
        status=job["status"],
        result=job.get("result_path"),  # return pointer instead of full result
    )
