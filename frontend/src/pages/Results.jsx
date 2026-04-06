import { useState } from 'react';

function Section({ title, label, defaultOpen = false, children }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="mb-8">
      <div className="collapse-header" onClick={() => setOpen(!open)}>
        <div>
          {label && <div className="label-upper mb-4">{label}</div>}
          <h3>{title}</h3>
        </div>
        <span className={`collapse-arrow ${open ? 'open' : ''}`}>▾</span>
      </div>
      {open && <div className="collapse-body" style={{ paddingTop: 16 }}>{children}</div>}
    </div>
  );
}

function Results({ result, onRestart }) {
  if (!result) return null;

  const sc = { compliant: 'var(--signal-green)', partial: 'var(--signal-amber)', non_compliant: 'var(--signal-red)' };
  const sl = { compliant: 'Vyhovující', partial: 'Částečně vyhovující', non_compliant: 'Nevyhovující' };
  const bc = (p) => p >= 80 ? 'good' : p >= 50 ? 'warn' : 'bad';
  const bcc = (p) => p >= 80 ? 'var(--signal-green)' : p >= 50 ? 'var(--signal-amber)' : 'var(--signal-red)';

  return (
    <div className="fade-in">
      <div className="text-center mb-8" style={{ marginTop: 24 }}>
        <div className="label-upper mb-12">Assessment Complete</div>
        <h1 style={{ marginBottom: 4 }}>{result.company_name}</h1>
        <p className="mono">{new Date(result.timestamp).toLocaleDateString('cs-CZ')} · {result.sector}</p>
      </div>

      <div className="divider-chrome" />

      <div className={`score-ring ${result.overall_status}`}>
        <div className="score-number" style={{ color: sc[result.overall_status] }}>
          {Math.round(result.overall_percentage)}<span className="score-unit">%</span>
        </div>
        <div className="score-subtitle">{result.overall_score} / {result.max_score}</div>
      </div>

      <div className="text-center mb-32">
        <span className={`status-badge ${result.overall_status}`}>{sl[result.overall_status]}</span>
      </div>

      <div className="stats-row">
        <div className="stat-cell">
          <div className="stat-val" style={{ color: 'var(--signal-red)' }}>{result.critical_gaps}</div>
          <div className="stat-lbl">Kritické</div>
        </div>
        <div className="stat-cell">
          <div className="stat-val" style={{ color: 'var(--signal-amber)' }}>{result.total_gaps}</div>
          <div className="stat-lbl">Celkem mezer</div>
        </div>
        <div className="stat-cell">
          <div className="stat-val" style={{ color: 'var(--signal-green)' }}>
            {result.domain_scores.filter(d => d.status === 'compliant').length}/{result.domain_scores.length}
          </div>
          <div className="stat-lbl">Domén OK</div>
        </div>
      </div>

      <Section title="Přehled domén" label="Domain breakdown" defaultOpen={true}>
        {result.domain_scores.map(ds => (
          <div key={ds.domain_id} className="domain-bar">
            <div className="domain-bar-header">
              <span className="domain-bar-name">{ds.domain_name_cs}</span>
              <span className="domain-bar-pct" style={{ color: bcc(ds.percentage) }}>{Math.round(ds.percentage)}%</span>
            </div>
            <div className="domain-bar-track">
              <div className={`domain-bar-fill ${bc(ds.percentage)}`} style={{ width: `${ds.percentage}%` }} />
            </div>
          </div>
        ))}
      </Section>

      {result.priority_actions.length > 0 && (
        <Section title="Prioritní akce" label="Fix these first" defaultOpen={true}>
          {result.priority_actions.map((gap, i) => (
            <div key={i} className={`gap-item w${gap.weight}`}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
                <span className="mono" style={{
                  fontSize: 9, padding: '2px 5px', borderRadius: 2, letterSpacing: 1,
                  background: gap.weight >= 5 ? 'var(--signal-red-bg)' : gap.weight >= 4 ? 'var(--signal-amber-bg)' : 'var(--surface-2)',
                  color: gap.weight >= 5 ? 'var(--signal-red)' : gap.weight >= 4 ? 'var(--signal-amber)' : 'var(--text-3)',
                  border: `1px solid ${gap.weight >= 5 ? 'var(--signal-red-border)' : gap.weight >= 4 ? 'var(--signal-amber-border)' : 'var(--edge-subtle)'}`,
                }}>{gap.weight}/5</span>
              </div>
              <div className="gap-question">{gap.question_cs}</div>
              <div className="gap-en">{gap.question_en}</div>
              <div className="gap-fix"><span className="gap-arrow">→ </span>{gap.remediation}</div>
              <div className="gap-ref">{gap.article_ref} · {gap.domain_name_cs}</div>
            </div>
          ))}
        </Section>
      )}

      {result.domain_scores.filter(ds => ds.gaps.length > 0).map(ds => (
        <Section key={ds.domain_id} title={`${ds.domain_name_cs} — ${Math.round(ds.percentage)}%`} label={ds.domain_name_en}>
          {ds.gaps.map((gap, i) => (
            <div key={i} className={`gap-item w${gap.weight}`}>
              <div className="gap-question">{gap.question_cs}</div>
              <div className="gap-en">{gap.question_en}</div>
              <div className="gap-fix"><span className="gap-arrow">→ </span>{gap.remediation}</div>
              <div className="gap-ref">{gap.article_ref}</div>
            </div>
          ))}
        </Section>
      ))}

      <div className="divider-chrome" />

      <div style={{ display: 'flex', justifyContent: 'center', gap: 12, paddingBottom: 32 }}>
        <button className="btn-chrome" onClick={() => {
          const API_BASE = window.location.hostname === 'localhost' ? 'http://localhost:8000' : '';
          window.open(`${API_BASE}/api/report/${result.id}`, '_blank');
        }} style={{ height: 40, padding: '0 24px', border: 'none', borderRadius: 'var(--r)', fontFamily: 'var(--font)', cursor: 'pointer' }}>
          Stáhnout PDF report
        </button>
        <button className="btn" onClick={onRestart}>Nové hodnocení</button>
        <button className="btn" onClick={() => window.print()}>Tisk</button>
      </div>
    </div>
  );
}

export default Results;
