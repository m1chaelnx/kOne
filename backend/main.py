"""
kOne — NIS2 Compliance Scanner
FastAPI Backend Server

Run with: uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data.nis2_questions import NIS2_DOMAINS, get_all_questions
from app.models.schemas import (
    AssessmentSubmission, AssessmentResult, QuestionResponse
)
from app.services.scoring import calculate_score


app = FastAPI(
    title="kOne NIS2 Compliance Scanner",
    description="AI-powered NIS2/Czech Cybersecurity Act compliance assessment tool",
    version="0.1.0",
)

# Allow the React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for now (we'll add a database in Phase 3)
assessments_db: dict[str, AssessmentResult] = {}


@app.get("/")
def root():
    return {
        "name": "kOne NIS2 Compliance Scanner",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/api/domains")
def get_domains():
    """Return all assessment domains (without questions)."""
    return [
        {
            "id": d["id"],
            "name_cs": d["name_cs"],
            "name_en": d["name_en"],
            "description_cs": d["description_cs"],
            "description_en": d["description_en"],
            "article_ref": d["article_ref"],
            "question_count": len(d["questions"]),
        }
        for d in NIS2_DOMAINS
    ]


@app.get("/api/questions")
def get_questions():
    """Return all assessment questions grouped by domain."""
    return NIS2_DOMAINS


@app.get("/api/questions/{domain_id}")
def get_domain_questions(domain_id: str):
    """Return questions for a specific domain."""
    for domain in NIS2_DOMAINS:
        if domain["id"] == domain_id:
            return domain
    return {"error": "Domain not found"}


@app.post("/api/assess", response_model=AssessmentResult)
def submit_assessment(submission: AssessmentSubmission):
    """
    Submit a completed assessment and get the compliance score.
    This is the main endpoint — the core of kOne.
    """
    result = calculate_score(submission)

    # Store the result
    assessments_db[result.id] = result

    return result


@app.get("/api/results/{assessment_id}", response_model=AssessmentResult)
def get_result(assessment_id: str):
    """Retrieve a previously completed assessment result."""
    if assessment_id in assessments_db:
        return assessments_db[assessment_id]
    return {"error": "Assessment not found"}


@app.get("/api/stats")
def get_stats():
    """Basic stats about the question database."""
    total_questions = sum(len(d["questions"]) for d in NIS2_DOMAINS)
    total_domains = len(NIS2_DOMAINS)
    max_score = sum(
        q["weight"]
        for d in NIS2_DOMAINS
        for q in d["questions"]
    )
    return {
        "total_domains": total_domains,
        "total_questions": total_questions,
        "max_possible_score": max_score,
        "assessments_completed": len(assessments_db),
    }
