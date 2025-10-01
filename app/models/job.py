from pydantic import BaseModel
from enum import Enum
from typing import Optional


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class JobRequest(BaseModel):
    file_id: str


class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    result: Optional[dict] = None
