# kOne — NIS2 Compliance Scanner

AI-powered NIS2 / Czech Cybersecurity Act compliance assessment tool.

## What this does

kOne scans your organization's cybersecurity posture against the requirements
of the Czech Cybersecurity Act (Act No. 264/2025 Coll.) which implements the
EU NIS2 Directive. It produces a compliance score, identifies gaps, and
recommends specific fixes — in both Czech and English.

## Project structure

```
kone/
├── backend/
│   ├── main.py                          # FastAPI server (run this)
│   ├── requirements.txt                 # Python dependencies
│   └── app/
│       ├── data/
│       │   └── nis2_questions.py        # NIS2 question database (41 questions, 10 domains)
│       ├── models/
│       │   └── schemas.py               # Data models (Pydantic)
│       └── services/
│           └── scoring.py               # Compliance scoring engine
└── frontend/                            # React frontend (next step)
```

## Quick start

### 1. Backend

```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

### 2. Test it

Open http://localhost:8000/docs — FastAPI auto-generates interactive API docs.

Try these endpoints:
- `GET /api/domains` — list all 10 assessment domains
- `GET /api/questions` — get all questions
- `GET /api/stats` — database statistics
- `POST /api/assess` — submit an assessment (see example below)

### 3. Example assessment submission

```json
{
  "company_name": "Moje Firma s.r.o.",
  "company_size": "medium",
  "sector": "manufacturing",
  "answers": [
    {"question_id": "gov_01", "value": "yes"},
    {"question_id": "gov_02", "value": "no"},
    {"question_id": "gov_03", "value": "partial"},
    {"question_id": "ir_01", "value": "yes"},
    {"question_id": "ir_02", "value": "no"}
  ]
}
```

Any unanswered questions are scored as "no" (worst case).

## Scoring

- **yes** = full points (weight × 1.0)
- **partial** = half points (weight × 0.5)
- **no** = zero points
- **na** = excluded from scoring

Status thresholds:
- **≥ 80%** = Compliant
- **50-79%** = Partially compliant
- **< 50%** = Non-compliant

## What's next

- [ ] Phase 2: PDF gap report generator
- [ ] Phase 3: User accounts + dashboard
- [ ] Phase 4: AI-powered recommendations (Claude API)
- [ ] Phase 5: Go to market — landing page + payments

## License

Proprietary — kOne © 2026
