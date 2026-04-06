"""
kOne — NIS2 Compliance Scanner
FastAPI Backend Server

Dev:  uvicorn main:app --reload
Prod: uvicorn main:app --host 0.0.0.0 --port 8000
"""

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response

from app.data.nis2_questions import NIS2_DOMAINS, get_all_questions
from app.models.schemas import (
    AssessmentSubmission, AssessmentResult, QuestionResponse
)
from app.services.scoring import calculate_score
from app.services.pdf_report import generate_report


app = FastAPI(
    title="kOne NIS2 Compliance Scanner",
    description="AI-powered NIS2/Czech Cybersecurity Act compliance assessment tool",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

assessments_db: dict[str, AssessmentResult] = {}

STATIC_DIR = Path(__file__).parent / "static"


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


@app.get("/api/report/{assessment_id}")
def download_report(assessment_id: str):
    """Generate and download a PDF compliance report."""
    if assessment_id not in assessments_db:
        return {"error": "Assessment not found"}

    result = assessments_db[assessment_id]
    pdf_bytes = generate_report(result)

    filename = f"kone-nis2-report-{result.company_name.replace(' ', '_')}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# Serve the React frontend in production
# This must come AFTER all API routes
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/{path:path}")
    async def serve_frontend(path: str):
        """Serve React app for all non-API routes."""
        file_path = STATIC_DIR / path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(STATIC_DIR / "index.html")
