# app/api/results.py
from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

from app.models.result import ResultResponse

router = APIRouter()

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)


def result_file_path(job_id: str) -> Path:
    return RESULTS_DIR / f"{job_id}.json"


@router.get("/{job_id}", response_model=ResultResponse)
async def get_result(job_id: str):
    path = result_file_path(job_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Result not found")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return ResultResponse(**data)
