import { useState, useEffect } from 'react';
import { getQuestions, submitAssessment } from '../services/api';

const OPTS = [
  { value: 'yes', label: 'Ano', cls: 'selected-yes' },
  { value: 'partial', label: 'Částečně', cls: 'selected-partial' },
  { value: 'no', label: 'Ne', cls: 'selected-no' },
  { value: 'na', label: 'N/A', cls: 'selected-na' },
];

function Assessment({ companyInfo, onComplete, onBack }) {
  const [domains, setDomains] = useState([]);
  const [cur, setCur] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    getQuestions()
      .then(d => { setDomains(d); setLoading(false); })
      .catch(() => { setError('Backend nedostupný'); setLoading(false); });
  }, []);

  const ans = (qid, val) => setAnswers(p => ({ ...p, [qid]: val }));
  const d = domains[cur];
  const totalQ = domains.reduce((s, x) => s + x.questions.length, 0);
  const doneQ = Object.keys(answers).length;
  const pct = totalQ > 0 ? (doneQ / totalQ) * 100 : 0;
  const isLast = cur === domains.length - 1;

  const next = () => {
    if (isLast) submit();
    else { setCur(p => p + 1); window.scrollTo({ top: 0, behavior: 'smooth' }); }
  };

  const prev = () => {
    if (cur > 0) { setCur(p => p - 1); window.scrollTo({ top: 0, behavior: 'smooth' }); }
  };

  const submit = async () => {
    setSubmitting(true);
    try {
      const res = await submitAssessment({
        ...companyInfo,
        answers: Object.entries(answers).map(([question_id, value]) => ({ question_id, value })),
      });
      onComplete(res);
    } catch { setError('Odeslání selhalo.'); setSubmitting(false); }
  };

  if (loading) return <div className="text-center mt-48"><p className="mono">Načítání...</p></div>;
  if (error) return <div className="text-center mt-48"><p style={{ color: 'var(--signal-red)', marginBottom: 16 }}>{error}</p><button className="btn" onClick={onBack}>← Zpět</button></div>;
  if (!d) return null;

  return (
    <div className="fade-in">
      <div className="progress-meta">
        <span>{doneQ} / {totalQ}</span>
        <span>{Math.round(pct)}%</span>
      </div>
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${pct}%` }} />
      </div>

      <div className="domain-nav">
        {domains.map((x, i) => {
          const done = x.questions.every(q => answers[q.id] !== undefined);
          let cls = 'domain-pill';
          if (i === cur) cls += ' active';
          else if (done) cls += ' complete';
          return <button key={x.id} className={cls} onClick={() => setCur(i)}>{i + 1}</button>;
        })}
      </div>

      <div className="mb-8">
        <div className="label-upper mb-8">{d.article_ref}</div>
        <h2>{d.name_cs}</h2>
        <p style={{ fontSize: 12, color: 'var(--text-3)', marginTop: 2 }}>{d.name_en}</p>
      </div>

      <div className="divider" />

      {d.questions.map(q => (
        <div key={q.id} className={`q-card ${answers[q.id] ? 'answered' : ''}`}>
          <p className="q-text-primary">{q.text_cs}</p>
          <p className="q-text-secondary">{q.text_en}</p>
          <div className="answer-group">
            {OPTS.map(o => (
              <button key={o.value} className={`answer-btn ${answers[q.id] === o.value ? o.cls : ''}`} onClick={() => ans(q.id, o.value)}>
                {o.label}
              </button>
            ))}
          </div>
        </div>
      ))}

      <div className="divider" />

      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <button className="btn" onClick={cur === 0 ? onBack : prev}>
          ← {cur === 0 ? 'Zpět' : 'Předchozí'}
        </button>
        <button className={isLast ? 'btn-chrome' : 'btn'} onClick={next} disabled={submitting}
          style={isLast ? { height: 40, padding: '0 24px', border: 'none', borderRadius: 'var(--r)', fontFamily: 'var(--font)', cursor: 'pointer' } : {}}>
          {submitting ? 'Odesílání...' : isLast ? 'Zobrazit výsledky →' : 'Další →'}
        </button>
      </div>
    </div>
  );
}

export default Assessment;
