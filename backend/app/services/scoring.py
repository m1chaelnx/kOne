"""
kOne Scoring Engine
Calculates compliance scores from assessment answers.
"""

import uuid
from datetime import datetime, timezone

from app.models.schemas import (
    AnswerValue, AssessmentSubmission, AssessmentResult,
    DomainScore, Answer
)
from app.data.nis2_questions import NIS2_DOMAINS, get_total_max_score


# How much of the weight each answer type earns
ANSWER_MULTIPLIERS = {
    AnswerValue.YES: 1.0,
    AnswerValue.PARTIAL: 0.5,
    AnswerValue.NO: 0.0,
    AnswerValue.NOT_APPLICABLE: None,  # excluded from scoring
}


def calculate_score(submission: AssessmentSubmission) -> AssessmentResult:
    """
    Takes a completed assessment and returns a full scored result.
    This is the core of kOne's value — turning answers into actionable scores.
    """
    # Index answers by question_id for fast lookup
    answer_map: dict[str, Answer] = {
        a.question_id: a for a in submission.answers
    }

    domain_scores = []
    all_gaps = []

    for domain in NIS2_DOMAINS:
        domain_score = 0.0
        domain_max = 0
        domain_gaps = []

        for question in domain["questions"]:
            answer = answer_map.get(question["id"])

            if answer is None:
                # Unanswered questions count as "no"
                answer_value = AnswerValue.NO
            else:
                answer_value = answer.value

            multiplier = ANSWER_MULTIPLIERS[answer_value]

            if multiplier is None:
                # N/A — skip this question entirely
                continue

            domain_max += question["weight"]
            domain_score += question["weight"] * multiplier

            # Track gaps (anything that's not a full "yes")
            if answer_value in (AnswerValue.NO, AnswerValue.PARTIAL):
                gap = {
                    "question_id": question["id"],
                    "question_cs": question["text_cs"],
                    "question_en": question["text_en"],
                    "answer": answer_value.value,
                    "weight": question["weight"],
                    "remediation": question["remediation_hint"],
                    "article_ref": question["article_ref"],
                    "domain_id": domain["id"],
                    "domain_name_cs": domain["name_cs"],
                    "domain_name_en": domain["name_en"],
                }
                domain_gaps.append(gap)
                all_gaps.append(gap)

        # Calculate domain percentage
        percentage = (domain_score / domain_max * 100) if domain_max > 0 else 0

        # Determine domain status
        if percentage >= 80:
            status = "compliant"
        elif percentage >= 50:
            status = "partial"
        else:
            status = "non_compliant"

        domain_scores.append(DomainScore(
            domain_id=domain["id"],
            domain_name_cs=domain["name_cs"],
            domain_name_en=domain["name_en"],
            score=round(domain_score, 1),
            max_score=domain_max,
            percentage=round(percentage, 1),
            status=status,
            gaps=domain_gaps,
        ))

    # Overall calculations
    overall_score = sum(ds.score for ds in domain_scores)
    overall_max = sum(ds.max_score for ds in domain_scores)
    overall_percentage = (overall_score / overall_max * 100) if overall_max > 0 else 0

    if overall_percentage >= 80:
        overall_status = "compliant"
    elif overall_percentage >= 50:
        overall_status = "partial"
    else:
        overall_status = "non_compliant"

    # Priority actions: sort all gaps by weight (highest first), take top 5
    critical_gaps = [g for g in all_gaps if g["weight"] >= 4]
    priority_actions = sorted(all_gaps, key=lambda g: g["weight"], reverse=True)[:5]

    return AssessmentResult(
        id=str(uuid.uuid4()),
        company_name=submission.company_name,
        company_size=submission.company_size,
        sector=submission.sector,
        timestamp=datetime.now(timezone.utc).isoformat(),
        overall_score=round(overall_score, 1),
        max_score=overall_max,
        overall_percentage=round(overall_percentage, 1),
        overall_status=overall_status,
        domain_scores=domain_scores,
        total_gaps=len(all_gaps),
        critical_gaps=len(critical_gaps),
        priority_actions=priority_actions,
    )
