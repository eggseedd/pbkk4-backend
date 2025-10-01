from fastapi import APIRouter, UploadFile, File, Form
from pathlib import Path
import shutil
import uuid

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    title: str = Form(None),
    author: str = Form(None),
):
    file_id = str(uuid.uuid4())
    original_name = file.filename or "uploaded_file"
    file_ext = Path(original_name).suffix
    saved_path = UPLOAD_DIR / f"{file_id}{file_ext}"

    with saved_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "file_id": file_id,
        "filename": original_name,
        "saved_path": str(saved_path),
        "title": title,
        "author": author,
    }

