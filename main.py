from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import resume
import uvicorn
from app.routers import auth


app = FastAPI(title="Resume Tailor API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect routers
app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
