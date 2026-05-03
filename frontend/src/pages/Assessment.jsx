import { useState, useEffect } from 'react';
import { getQuestions, submitAssessment } from '../services/api';

const OPTS = [
  { value: 'yes', label: 'Ano', cls: 'selected-yes' },
  { value: 'partial', label: 'Castecne', cls: 'selected-partial' },
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
      .catch(() => { setError('Backend nedostupny'); setLoading(false); });
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
    } catch { setError('Odeslani selhalo.'); setSubmitting(false); }
  };

  if (loading) return <div style={{ textAlign: 'center', marginTop: 80 }}><p style={{ fontSize: 12, color: 'var(--text-3)', letterSpacing: 2 }}>NACITANI...</p></div>;
  if (error) return <div style={{ textAlign: 'center', marginTop: 80 }}><p style={{ color: '#c45050', marginBottom: 16, fontSize: 14 }}>{error}</p><button className="btn" onClick={onBack}>Zpet</button></div>;
  if (!d) return null;

  return (
    <div className="fade-in" style={{ maxWidth: 640, margin: '0 auto' }}>

      {/* Progress — minimal */}
      <div style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        marginBottom: 6, fontSize: 11, color: 'var(--text-3)', letterSpacing: 1
      }}>
        <span>{doneQ} / {totalQ}</span>
        <span>{Math.round(pct)}%</span>
      </div>
      <div style={{
        width: '100%', height: 2, background: 'var(--edge-subtle)',
        marginBottom: 32, overflow: 'hidden'
      }}>
        <div style={{
          height: '100%', width: pct + '%',
          background: 'var(--chrome-dim)',
          transition: 'width 0.4s ease'
        }} />
      </div>

      {/* Domain nav — numbered, compact */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 36 }}>
        {domains.map((x, i) => {
          const done = x.questions.every(q => answers[q.id] !== undefined);
          const isActive = i === cur;
          return (
            <button
              key={x.id}
              onClick={() => setCur(i)}
              style={{
                width: 34, height: 30,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                borderRadius: 3, border: '1px solid',
                borderColor: isActive ? 'var(--chrome-dim)' : done ? 'rgba(74, 158, 120, 0.25)' : 'var(--edge)',
                background: isActive ? 'rgba(25, 40, 80, 0.4)' : 'transparent',
                color: isActive ? 'var(--chrome)' : done ? 'rgba(74, 158, 120, 0.7)' : 'var(--text-3)',
                fontFamily: 'var(--font)', fontSize: 12, fontWeight: 400,
                cursor: 'pointer', transition: 'all 0.15s'
              }}
            >
              {i + 1}
            </button>
          );
        })}
      </div>

      {/* Domain header */}
      <div style={{ marginBottom: 12 }}>
        <p style={{
          fontSize: 10, fontWeight: 500, letterSpacing: 3,
          color: 'var(--chrome-dim)', textTransform: 'uppercase', marginBottom: 8
        }}>
          {d.article_ref}
        </p>
        <h2 style={{
          fontSize: 22, fontWeight: 500, letterSpacing: '-0.02em',
          color: 'var(--text-1)', marginBottom: 4
        }}>
          {d.name_cs}
        </h2>
        <p style={{ fontSize: 13, color: 'var(--text-3)', fontWeight: 300 }}>
          {d.name_en}
        </p>
      </div>

      <div style={{ height: 1, background: 'var(--edge-subtle)', marginBottom: 8 }} />

      {/* Questions */}
      {d.questions.map(q => (
        <div key={q.id} style={{
          padding: '24px 0',
          borderBottom: '1px solid var(--edge)',
        }}>
          <p style={{
            fontSize: 16, fontWeight: 400, lineHeight: 1.55,
            color: 'var(--text-1)', marginBottom: 4
          }}>
            {q.text_cs}
          </p>
          <p style={{
            fontSize: 13, color: 'var(--text-3)', lineHeight: 1.5,
            fontWeight: 300, marginBottom: 16
          }}>
            {q.text_en}
          </p>

          {/* Answer buttons */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 6 }}>
            {OPTS.map(o => {
              const isSelected = answers[q.id] === o.value;
              let bg = 'var(--surface-1)';
              let border = 'var(--edge)';
              let color = 'var(--text-3)';

              if (isSelected) {
                if (o.value === 'yes') { bg = 'rgba(74, 158, 120, 0.1)'; border = 'rgba(74, 158, 120, 0.3)'; color = '#4a9e78'; }
                else if (o.value === 'partial') { bg = 'rgba(184, 148, 42, 0.1)'; border = 'rgba(184, 148, 42, 0.3)'; color = '#b8942a'; }
                else if (o.value === 'no') { bg = 'rgba(196, 80, 80, 0.1)'; border = 'rgba(196, 80, 80, 0.3)'; color = '#c45050'; }
                else { bg = 'var(--surface-2)'; border = 'var(--edge-visible)'; color = 'var(--text-2)'; }
              }

              return (
                <button
                  key={o.value}
                  onClick={() => ans(q.id, o.value)}
                  style={{
                    height: 40, border: '1px solid',
                    borderColor: border, borderRadius: 3,
                    background: bg, color: color,
                    fontFamily: 'var(--font)', fontSize: 12,
                    fontWeight: isSelected ? 500 : 400,
                    letterSpacing: 1, textTransform: 'uppercase',
                    cursor: 'pointer', transition: 'all 0.15s',
                  }}
                >
                  {o.label}
                </button>
              );
            })}
          </div>
        </div>
      ))}

      {/* Navigation */}
      <div style={{
        display: 'flex', justifyContent: 'space-between',
        marginTop: 32, paddingBottom: 24
      }}>
        <button className="btn" onClick={cur === 0 ? onBack : prev}>
          {cur === 0 ? 'Zpet' : 'Predchozi'}
        </button>
        {isLast ? (
          <button
            className="btn-chrome"
            onClick={next}
            disabled={submitting}
            style={{
              height: 42, padding: '0 28px', border: 'none',
              borderRadius: 3, fontFamily: 'var(--font)',
              fontSize: 12, letterSpacing: 2,
              cursor: submitting ? 'not-allowed' : 'pointer',
              opacity: submitting ? 0.4 : 1
            }}
          >
            {submitting ? 'ODESILANI...' : 'VYSLEDKY'}
          </button>
        ) : (
          <button className="btn" onClick={next}>
            Dalsi
          </button>
        )}
      </div>
    </div>
  );
}

export default Assessment;
