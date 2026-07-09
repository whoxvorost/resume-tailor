from fastapi import APIRouter, UploadFile, HTTPException, File, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.resume import Resume
from app.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    GenerateRequest,
    GenerateResponse,
    ExportResponse,
)
from app.services.resume_parser import parse_resume
from app.services.ats_scorer import calculate_ats_score
from app.services.ai_generator import generate_tailored_resume
from app.services.pdf_generator import generate_pdf
from app.auth import get_current_user
from app.exceptions import ResumeNotFoundException, FileTypeException, FileSizeException
from fastapi.responses import FileResponse
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    if not file.filename.endswith((".pdf", ".docx")):
        raise FileTypeException()

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise FileSizeException()

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

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


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    request: AnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()

    if not resume:
        raise ResumeNotFoundException(request.resume_id)

    resume_text = parse_resume(resume.file_path)
    ats_result = calculate_ats_score(resume_text, request.job_description)

    return AnalyzeResponse(
        resume_id=request.resume_id,
        ats_score=ats_result["score"],
        missing_keywords=ats_result["missing_keywords"],
    )


@router.post("/generate", response_model=GenerateResponse)
async def generate_resume(
    request: GenerateRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()

    if not resume:
        raise ResumeNotFoundException(request.resume_id)

    resume_text = parse_resume(resume.file_path)
    ats_result = calculate_ats_score(resume_text, request.job_description)
    generated = generate_tailored_resume(
        resume_text, request.job_description, ats_result["missing_keywords"]
    )

    return GenerateResponse(
        resume_id=request.resume_id,
        ats_score=ats_result["score"],
        generated_resume=generated,
    )


@router.post("/export", response_model=ExportResponse)
async def export_resume(
    request: GenerateRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()

    if not resume:
        raise ResumeNotFoundException(request.resume_id)

    resume_text = parse_resume(resume.file_path)
    ats_result = calculate_ats_score(resume_text, request.job_description)
    generated = generate_tailored_resume(
        resume_text, request.job_description, ats_result["missing_keywords"]
    )
    pdf_path = generate_pdf(generated, f"resume_{request.resume_id}")

    return ExportResponse(
        resume_id=request.resume_id,
        ats_score=ats_result["score"],
        pdf_path=pdf_path,
        status="exported",
    )


@router.get("/download/{resume_id}")
async def download_pdf(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    pdf_path = f"outputs/resume_{resume_id}.pdf"

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found. Generate first.")

    return FileResponse(
        path=pdf_path, media_type="application/pdf", filename=f"resume_{resume_id}.pdf"
    )
