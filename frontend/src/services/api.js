/**
 * kOne API Service
 * Handles all communication with the FastAPI backend.
 * 
 * Think of this as the phone line between the frontend (what users see)
 * and the backend (where the scoring happens).
 */

const API_BASE = window.location.hostname === 'localhost' ? 'http://localhost:8000' : '';

/**
 * Fetch all assessment domains (the 10 security categories).
 * Used to build the questionnaire navigation.
 */
export async function getDomains() {
  const res = await fetch(`${API_BASE}/api/domains`);
  return res.json();
}

/**
 * Fetch all questions grouped by domain.
 * This is the main data that powers the questionnaire UI.
 */
export async function getQuestions() {
  const res = await fetch(`${API_BASE}/api/questions`);
  return res.json();
}

/**
 * Submit a completed assessment and get the compliance score back.
 * This is the core action — user fills out the form, we send it to the
 * scoring engine, and display the results.
 * 
 * @param {Object} submission - { company_name, company_size, sector, answers[] }
 * @returns {Object} AssessmentResult with scores, gaps, and priority actions
 */
export async function submitAssessment(submission) {
  const res = await fetch(`${API_BASE}/api/assess`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(submission),
  });
  return res.json();
}

/**
 * Fetch a previously completed assessment by ID.
 */
export async function getResult(assessmentId) {
  const res = await fetch(`${API_BASE}/api/results/${assessmentId}`);
  return res.json();
}

/**
 * Get basic stats about the question database.
 */
export async function getStats() {
  const res = await fetch(`${API_BASE}/api/stats`);
  return res.json();
}
