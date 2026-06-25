import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def generate_tailored_resume(
    resume_text: str, job_description: str, ats_missing: list
) -> str:
    prompt = f"""You are a professional resume writer.

Original resume:
{resume_text}

Job description:
{job_description}

Missing keywords to include: {", ".join(ats_missing)}

Write a tailored one-page resume that:
- Includes missing keywords naturally
- Keeps only real experience from original resume
- Makes bullet points impact-based
- Follows structure: Summary, Skills, Experience, Education

Return only the resume text, no explanations."""

    response = requests.post(
        OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}
    )

    return response.json()["response"]
