from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.resume import Resume
import shutil
import os
from app.services.resume_parser import parse_resume
from app.services.ats_scorer import calculate_ats_score

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume = Resume(filename=file.filename, file_path=file_path)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    text = parse_resume(file_path)

    return {
        "id": resume.id,
        "filename": resume.filename,
        "status": "saved",
        "text_length": len(text),
    }


@router.post("/analyze")
async def analyze_resume(
    resume_id: int, job_description: str, db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        return {"error": "Resume not found"}

    resume_text = parse_resume(resume.file_path)
    ats_result = calculate_ats_score(resume_text, job_description)

    return {
        "resume_id": resume_id,
        "ats_score": ats_result["score"],
        "missing_keywords": ats_result["missing_keywords"],
    }
