from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def extract_keywords(text: str) -> list:
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    return list(set(words))


def calculate_ats_score(resume_text: str, job_text: str) -> dict:
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([resume_text, job_text])
    score = cosine_similarity(matrix[0], matrix[1])[0][0]

    resume_keywords = set(extract_keywords(resume_text))
    job_keywords = set(extract_keywords(job_text))
    missing = list(job_keywords - resume_keywords)[:10]

    return {"score": round(float(score) * 100, 2), "missing_keywords": missing}
