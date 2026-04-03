"""
kOne data models.
Using Pydantic for API request/response validation.
"""

from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class AnswerValue(str, Enum):
    YES = "yes"
    PARTIAL = "partial"
    NO = "no"
    NOT_APPLICABLE = "na"


class QuestionResponse(BaseModel):
    """A single question in the API response."""
    id: str
    domain_id: str
    domain_name_cs: str
    domain_name_en: str
    text_cs: str
    text_en: str
    weight: int
    article_ref: str


class Answer(BaseModel):
    """A single answer submitted by the user."""
    question_id: str
    value: AnswerValue
    note: str = ""


class AssessmentSubmission(BaseModel):
    """The full assessment submitted by a user."""
    company_name: str
    company_size: str  # "micro", "small", "medium", "large"
    sector: str
    answers: list[Answer]


class DomainScore(BaseModel):
    """Score breakdown for a single domain."""
    domain_id: str
    domain_name_cs: str
    domain_name_en: str
    score: float
    max_score: int
    percentage: float
    status: str  # "compliant", "partial", "non_compliant"
    gaps: list[dict]  # questions answered "no" with remediation hints


class AssessmentResult(BaseModel):
    """The complete assessment result."""
    id: str
    company_name: str
    company_size: str
    sector: str
    timestamp: str
    overall_score: float
    max_score: int
    overall_percentage: float
    overall_status: str
    domain_scores: list[DomainScore]
    total_gaps: int
    critical_gaps: int  # gaps with weight >= 4
    priority_actions: list[dict]  # top 5 things to fix first
