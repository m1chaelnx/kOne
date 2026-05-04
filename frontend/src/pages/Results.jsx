import { useState } from 'react';

function Section({ title, label, defaultOpen = true, count, children }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div style={{ marginBottom: 8 }}>
      <div
        onClick={() => setOpen(!open)}
        style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          padding: '16px 0', borderBottom: '1px solid var(--edge)',
          cursor: 'pointer', userSelect: 'none',
          transition: 'color 0.15s'
        }}
      >
        <div>
          {label && <p style={{ fontSize: 9, letterSpacing: 3, color: 'var(--chrome-dim)', textTransform: 'uppercase', marginBottom: 4 }}>{label}</p>}
          <h3 style={{ fontSize: 15, fontWeight: 500, color: 'var(--text-1)', letterSpacing: '-0.01em' }}>
            {title}
            {count !== undefined && <span style={{ fontSize: 11, color: 'var(--text-3)', fontWeight: 400, marginLeft: 8 }}>({count})</span>}
          </h3>
        </div>
        <span style={{ fontSize: 10, color: 'var(--text-3)', transform: open ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }}>&#9662;</span>
      </div>
      {open && <div style={{ paddingTop: 20 }}>{children}</div>}
    </div>
  );
}

function Results({ result, onRestart }) {
  if (!result) return null;

  const colorMap = { compliant: '#4a9e78', partial: '#b8942a', non_compliant: '#c45050' };
  const labelMap = { compliant: 'VYHOVUJICI', partial: 'CASTECNE VYHOVUJICI', non_compliant: 'NEVYHOVUJICI' };
  const sc = colorMap[result.overall_status];
  const barColor = (p) => p >= 80 ? '#4a9e78' : p >= 50 ? '#b8942a' : '#c45050';
  const compliantCount = result.domain_scores.filter(d => d.status === 'compliant').length;

  return (
    <div className="fade-in" style={{ maxWidth: 600, margin: '0 auto' }}>

      {/* Header — company + date */}
      <div style={{ textAlign: 'center', marginTop: 32, marginBottom: 40 }}>
        <p style={{ fontSize: 9, letterSpacing: 3, color: 'var(--chrome-dim)', textTransform: 'uppercase', marginBottom: 12 }}>
          Assessment Complete
        </p>
        <h1 style={{ fontSize: 26, fontWeight: 500, letterSpacing: '-0.03em', color: 'var(--text-1)', marginBottom: 6 }}>
          {result.company_name}
        </h1>
        <p style={{ fontSize: 11, color: 'var(--text-3)', letterSpacing: 1 }}>
          {new Date(result.timestamp).toLocaleDateString('cs-CZ')}  |  {result.sector}
        </p>
      </div>

      {/* Score ring */}
      <div style={{
        width: 180, height: 180, borderRadius: '50%',
        border: '1.5px solid ' + sc,
        display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center',
        margin: '0 auto 12px',
        boxShadow: '0 0 60px ' + sc + '10',
        background: sc + '08'
      }}>
        <span style={{ fontSize: 52, fontWeight: 300, color: sc, letterSpacing: -3, lineHeight: 1 }}>
          {Math.round(result.overall_percentage)}
          <span style={{ fontSize: 22, opacity: 0.5 }}>%</span>
        </span>
        <span style={{ fontSize: 11, color: 'var(--text-3)', marginTop: 6, letterSpacing: 1 }}>
          {result.overall_score} / {result.max_score}
        </span>
      </div>

      {/* Status badge */}
      <div style={{ textAlign: 'center', marginBottom: 40 }}>
        <span style={{
          display: 'inline-flex', alignItems: 'center', gap: 8,
          fontSize: 10, fontWeight: 500, letterSpacing: 2,
          color: sc, padding: '6px 16px', borderRadius: 20,
          border: '1px solid ' + sc + '30',
          background: sc + '0a'
        }}>
          <span style={{ width: 5, height: 5, borderRadius: '50%', background: sc }} />
          {labelMap[result.overall_status]}
        </span>
      </div>

      {/* Key metrics — three cells */}
      <div style={{
        display: 'grid', gridTemplateColumns: '1fr 1fr 1fr',
        gap: 1, background: 'var(--edge)',
        borderRadius: 4, overflow: 'hidden', marginBottom: 48
      }}>
        {[
          { val: result.critical_gaps, lbl: 'KRITICKYCH', color: '#c45050' },
          { val: result.total_gaps, lbl: 'CELKEM MEZER', color: '#b8942a' },
          { val: compliantCount + '/' + result.domain_scores.length, lbl: 'DOMEN OK', color: '#4a9e78' },
        ].map((s, i) => (
          <div key={i} style={{ background: 'var(--surface-1)', padding: '20px 16px', textAlign: 'center' }}>
            <div style={{ fontSize: 26, fontWeight: 300, color: s.color, letterSpacing: -1 }}>{s.val}</div>
            <div style={{ fontSize: 8, color: 'var(--text-3)', letterSpacing: 2, marginTop: 4 }}>{s.lbl}</div>
          </div>
        ))}
      </div>

      {/* Domain breakdown */}
      <Section title="Prehled domen" label="Domain Breakdown">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {result.domain_scores.map(ds => {
            const pct = Math.round(ds.percentage);
            const bc = barColor(ds.percentage);
            return (
              <div key={ds.domain_id}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 }}>
                  <span style={{ fontSize: 13, fontWeight: 400, color: 'var(--text-1)' }}>{ds.domain_name_cs}</span>
                  <span style={{ fontSize: 13, fontWeight: 500, color: bc, letterSpacing: -0.5 }}>{pct}%</span>
                </div>
                <div style={{ width: '100%', height: 3, background: 'var(--edge-subtle)', borderRadius: 2, overflow: 'hidden' }}>
                  <div style={{ width: pct + '%', height: '100%', background: bc, borderRadius: 2, transition: 'width 0.6s ease' }} />
                </div>
              </div>
            );
          })}
        </div>
      </Section>

      {/* Priority actions */}
      {result.priority_actions.length > 0 && (
        <Section title="Prioritni akce" label="Fix These First" count={result.priority_actions.length}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            {result.priority_actions.map((gap, i) => {
              const wt = gap.weight;
              const wc = wt >= 5 ? '#c45050' : wt >= 4 ? '#b8942a' : 'var(--text-3)';
              return (
                <div key={i} style={{
                  padding: '18px 20px 18px 18px',
                  borderLeft: '2px solid ' + wc,
                  background: 'var(--surface-1)',
                  marginBottom: 2,
                  transition: 'background 0.15s'
                }}
                onMouseEnter={e => e.currentTarget.style.background = 'var(--surface-2)'}
                onMouseLeave={e => e.currentTarget.style.background = 'var(--surface-1)'}
                >
                  {/* Weight badge */}
                  <span style={{
                    display: 'inline-block', fontSize: 9, fontWeight: 500,
                    padding: '2px 6px', borderRadius: 2, letterSpacing: 1,
                    color: wc, background: wc + '12', border: '1px solid ' + wc + '25',
                    marginBottom: 8
                  }}>
                    {wt}/5
                  </span>

                  {/* Question */}
                  <p style={{ fontSize: 14, fontWeight: 500, color: 'var(--text-1)', lineHeight: 1.5, marginBottom: 4 }}>
                    {gap.question_cs}
                  </p>
                  <p style={{ fontSize: 12, color: 'var(--text-3)', fontWeight: 300, marginBottom: 10 }}>
                    {gap.question_en}
                  </p>

                  {/* Remediation */}
                  <p style={{ fontSize: 13, color: 'var(--text-2)', lineHeight: 1.65, fontWeight: 300 }}>
                    <span style={{ color: 'var(--chrome-dim)', marginRight: 6 }}>&#8594;</span>
                    {gap.remediation}
                  </p>

                  {/* Reference */}
                  <p style={{ fontSize: 9, color: 'var(--text-3)', letterSpacing: 1, marginTop: 10, textTransform: 'uppercase' }}>
                    {gap.article_ref}  |  {gap.domain_name_cs}
                  </p>
                </div>
              );
            })}
          </div>
        </Section>
      )}

      {/* Full gap analysis by domain */}
      {result.domain_scores.filter(ds => ds.gaps.length > 0).map(ds => (
        <Section
          key={ds.domain_id}
          title={ds.domain_name_cs + ' - ' + Math.round(ds.percentage) + '%'}
          label={ds.domain_name_en}
          defaultOpen={false}
          count={ds.gaps.length}
        >
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            {ds.gaps.map((gap, i) => {
              const wt = gap.weight;
              const wc = wt >= 5 ? '#c45050' : wt >= 4 ? '#b8942a' : 'var(--text-3)';
              return (
                <div key={i} style={{
                  padding: '16px 18px 16px 16px',
                  borderLeft: '2px solid ' + wc,
                  background: 'var(--surface-1)',
                  marginBottom: 2
                }}>
                  <p style={{ fontSize: 13, fontWeight: 500, color: 'var(--text-1)', lineHeight: 1.5, marginBottom: 3 }}>
                    {gap.question_cs}
                  </p>
                  <p style={{ fontSize: 11, color: 'var(--text-3)', fontWeight: 300, marginBottom: 8 }}>
                    {gap.question_en}
                  </p>
                  <p style={{ fontSize: 12, color: 'var(--text-2)', lineHeight: 1.6, fontWeight: 300 }}>
                    <span style={{ color: 'var(--chrome-dim)', marginRight: 6 }}>&#8594;</span>
                    {gap.remediation}
                  </p>
                  <p style={{ fontSize: 8, color: 'var(--text-3)', letterSpacing: 1, marginTop: 8, textTransform: 'uppercase' }}>
                    {gap.article_ref}
                  </p>
                </div>
              );
            })}
          </div>
        </Section>
      ))}

      {/* Actions */}
      <div style={{ marginTop: 48, paddingTop: 24, borderTop: '1px solid var(--edge)', paddingBottom: 40 }}>
        <div style={{ display: 'flex', justifyContent: 'center', gap: 12 }}>
          <button
            className="btn-chrome"
            onClick={() => {
              const API_BASE = window.location.hostname === 'localhost' ? 'http://localhost:8000' : '';
              window.open(API_BASE + '/api/report/' + result.id, '_blank');
            }}
            style={{
              height: 44, padding: '0 28px', border: 'none',
              borderRadius: 3, fontFamily: 'var(--font)',
              fontSize: 11, letterSpacing: 2, cursor: 'pointer'
            }}
          >
            STAHNOUT PDF
          </button>
          <button className="btn" onClick={onRestart}>Nove hodnoceni</button>
        </div>

        <p style={{ textAlign: 'center', fontSize: 9, color: 'var(--text-3)', letterSpacing: 1, marginTop: 20 }}>
          Zakon c. 264/2025 Sb.  |  EU NIS2  |  NUKIB  |  2026 Noxra
        </p>
      </div>
    </div>
  );
}

export default Results;
