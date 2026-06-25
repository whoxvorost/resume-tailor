from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ResumeResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True


class AnalyzeRequest(BaseModel):
    resume_id: int
    job_description: str


class AnalyzeResponse(BaseModel):
    resume_id: int
    ats_score: float
    missing_keywords: list[str]


class GenerateRequest(BaseModel):
    resume_id: int
    job_description: str


class GenerateResponse(BaseModel):
    resume_id: int
    ats_score: float
    generated_resume: str


class ExportResponse(BaseModel):
    resume_id: int
    ats_score: float
    pdf_path: str
    status: str
