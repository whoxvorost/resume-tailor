from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import resume
import uvicorn

# Create the FastAPI application instance
app = FastAPI(title="Resume Tailor API")

# Allow all origins during development so the frontend can reach the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect routers
app.include_router(resume.router, prefix="/resume", tags=["resume"])


# Health check endpoint — used to verify the server is running
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Entry point: run with `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
