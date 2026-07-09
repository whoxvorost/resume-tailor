from fastapi import HTTPException


class ResumeNotFoundException(HTTPException):
    def __init__(self, resume_id: int):
        super().__init__(
            status_code=404, detail=f"Resume with id {resume_id} not found"
        )


class FileTypeException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Only PDF and DOCX files are allowed")


class FileSizeException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="File size must be less than 10MB")


class AIServiceException(HTTPException):
    def __init__(self):
        super().__init__(status_code=503, detail="AI service is currently unavailable")
