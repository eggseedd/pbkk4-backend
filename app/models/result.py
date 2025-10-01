# app/models/result.py
from pydantic import BaseModel
from typing import Any, Optional

class ResultResponse(BaseModel):
    job_id: str
    output: Optional[Any] = None  # flexible, depends on AI processing
