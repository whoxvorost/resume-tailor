from fastapi import APIRouter, UploadFile, File
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Create uploads folder if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save file to disk
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "status": "saved", "path": file_path}
