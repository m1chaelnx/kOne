import { useState } from 'react';

function Expandable({ title, count, defaultOpen = false, children }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div style={{ marginBottom: 2 }}>
      <div onClick={() => setOpen(!open)} style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        padding: '12px 16px', cursor: 'pointer',
        background: open ? 'rgba(15, 20, 40, 0.6)' : 'rgba(10, 14, 30, 0.4)',
        borderLeft: '2px solid ' + (open ? '#1a3670' : 'transparent'),
        transition: 'all 0.15s'
      }}>
        <span style={{ fontSize: 13, fontWeight: 500, color: '#c8c6c0' }}>{title} <span style={{ fontSize: 11, color: '#4a4a56', fontWeight: 400 }}>({count})</span></span>
        <span style={{ fontSize: 9, color: '#4a4a56', transform: open ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }}>&#9662;</span>
      </div>
      {open && <div style={{ padding: '16px', background: 'rgba(8, 10, 24, 0.5)' }}>{children}</div>}
    </div>
  );
}

function Results({ result, onRestart }) {
  if (!result) return null;

  const sc = result.overall_status === 'compliant' ? '#3d8c6a' : result.overall_status === 'partial' ? '#9e8528' : '#a04040';
  const scBg = result.overall_status === 'compliant' ? 'rgba(61,140,106,0.06)' : result.overall_status === 'partial' ? 'rgba(158,133,40,0.06)' : 'rgba(160,64,64,0.06)';
  const label = result.overall_status === 'compliant' ? 'VYHOVUJICI' : result.overall_status === 'partial' ? 'CASTECNE' : 'NEVYHOVUJICI';
  const bc = (p) => p >= 80 ? '#3d8c6a' : p >= 50 ? '#9e8528' : '#a04040';
  const okCount = result.domain_scores.filter(d => d.status === 'compliant').length;

  return (
    <div className="fade-in" style={{ maxWidth: 1080, margin: '0 auto', padding: '0 24px' }}>

      <div style={{ textAlign: 'center', marginTop: 32, marginBottom: 32 }}>
        <p style={{ fontSize: 9, letterSpacing: 4, color: '#1a3670', textTransform: 'uppercase', marginBottom: 10 }}>Assessment Complete</p>
        <h1 style={{ fontSize: 24, fontWeight: 500, color: '#c8c6c0', letterSpacing: '-0.02em', marginBottom: 4 }}>{result.company_name}</h1>
        <p style={{ fontSize: 10, color: '#4a4a56', letterSpacing: 1 }}>{new Date(result.timestamp).toLocaleDateString('cs-CZ')}  |  {result.sector}</p>
      </div>

      <div style={{ height: 1, background: 'linear-gradient(90deg, transparent, #1a3670, transparent)', marginBottom: 32, opacity: 0.4 }} />

      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: 32, alignItems: 'start' }}>

        <div style={{ position: 'sticky', top: 64 }}>

          <div style={{
            background: 'rgba(10, 14, 30, 0.5)',
            border: '1px solid rgba(26, 54, 112, 0.15)',
            borderRadius: 4, padding: '36px 24px', textAlign: 'center',
            marginBottom: 12
          }}>
            <div style={{
              width: 150, height: 150, borderRadius: '50%',
              border: '1px solid ' + sc,
              display: 'flex', flexDirection: 'column',
              alignItems: 'center', justifyContent: 'center',
              margin: '0 auto 16px',
              background: scBg,
              boxShadow: '0 0 40px ' + sc + '08'
            }}>
              <span style={{ fontSize: 46, fontWeight: 300, color: sc, letterSpacing: -2, lineHeight: 1 }}>
                {Math.round(result.overall_percentage)}
                <span style={{ fontSize: 18, opacity: 0.5 }}>%</span>
              </span>
              <span style={{ fontSize: 10, color: '#4a4a56', marginTop: 4, letterSpacing: 1 }}>
                {result.overall_score} / {result.max_score}
              </span>
            </div>

            <span style={{
              display: 'inline-block', fontSize: 9, fontWeight: 500, letterSpacing: 2,
              color: sc, padding: '4px 12px', borderRadius: 2,
              border: '1px solid ' + sc + '25', background: sc + '08'
            }}>{label}</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 2, marginBottom: 12 }}>
            {[
              { val: result.critical_gaps, lbl: 'Kritickych mezer', c: '#a04040' },
              { val: result.total_gaps, lbl: 'Celkem mezer', c: '#9e8528' },
              { val: okCount + '/' + result.domain_scores.length, lbl: 'Domen v souladu', c: '#3d8c6a' },
            ].map((s, i) => (
              <div key={i} style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                padding: '12px 16px',
                background: 'rgba(10, 14, 30, 0.4)',
                borderLeft: '2px solid ' + s.c + '40',
              }}>
                <span style={{ fontSize: 11, color: '#6a6a76', letterSpacing: 0.5 }}>{s.lbl}</span>
                <span style={{ fontSize: 18, fontWeight: 400, color: s.c, letterSpacing: -0.5 }}>{s.val}</span>
              </div>
            ))}
          </div>

          <div style={{
            background: 'rgba(10, 14, 30, 0.4)',
            border: '1px solid rgba(26, 54, 112, 0.1)',
            borderRadius: 4, padding: '20px 16px'
          }}>
            <p style={{ fontSize: 9, letterSpacing: 3, color: '#1a3670', textTransform: 'uppercase', marginBottom: 14 }}>Domains</p>
            {result.domain_scores.map(ds => {
              const pct = Math.round(ds.percentage);
              const c = bc(ds.percentage);
              return (
                <div key={ds.domain_id} style={{ marginBottom: 12 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <span style={{ fontSize: 11, color: '#8a8a96' }}>{ds.domain_name_cs}</span>
                    <span style={{ fontSize: 11, fontWeight: 500, color: c }}>{pct}%</span>
                  </div>
                  <div style={{ width: '100%', height: 2, background: 'rgba(255,255,255,0.04)', borderRadius: 1 }}>
                    <div style={{
                      width: pct + '%', height: '100%', borderRadius: 1,
                      background: 'linear-gradient(90deg, ' + c + ', ' + c + '60)',
                      transition: 'width 0.5s ease'
                    }} />
                  </div>
                </div>
              );
            })}
          </div>

          <div style={{ marginTop: 16, display: 'flex', flexDirection: 'column', gap: 6 }}>
            <button
              onClick={() => {
                const API_BASE = window.location.hostname === 'localhost' ? 'http://localhost:8000' : '';
                window.open(API_BASE + '/api/report/' + result.id, '_blank');
              }}
              style={{
                width: '100%', height: 42, border: 'none', borderRadius: 3,
                background: 'linear-gradient(180deg, #1a3670 0%, #0f2050 100%)',
                color: '#a0b0d0', fontFamily: 'var(--font)',
                fontSize: 11, letterSpacing: 2, textTransform: 'uppercase',
                cursor: 'pointer', transition: 'all 0.15s'
              }}
              onMouseEnter={e => { e.currentTarget.style.background = 'linear-gradient(180deg, #2a4a8c 0%, #1a3670 100%)'; e.currentTarget.style.color = '#c0d0f0'; }}
              onMouseLeave={e => { e.currentTarget.style.background = 'linear-gradient(180deg, #1a3670 0%, #0f2050 100%)'; e.currentTarget.style.color = '#a0b0d0'; }}
            >
              Stahnout PDF report
            </button>
            <button className="btn" onClick={onRestart} style={{ width: '100%' }}>Nove hodnoceni</button>
          </div>
        </div>

        <div>

          {result.priority_actions.length > 0 && (
            <div style={{ marginBottom: 24 }}>
              <p style={{ fontSize: 9, letterSpacing: 3, color: '#1a3670', textTransform: 'uppercase', marginBottom: 8 }}>Fix These First</p>
              <h2 style={{ fontSize: 16, fontWeight: 500, color: '#c8c6c0', letterSpacing: '-0.01em', marginBottom: 16 }}>
                Prioritni akce
                <span style={{ fontSize: 12, color: '#4a4a56', fontWeight: 400, marginLeft: 8 }}>({result.priority_actions.length})</span>
              </h2>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                {result.priority_actions.map((gap, i) => {
                  const wt = gap.weight;
                  const wc = wt >= 5 ? '#a04040' : wt >= 4 ? '#9e8528' : '#4a4a56';
                  return (
                    <div key={i} style={{
                      padding: '16px 18px',
                      borderLeft: '2px solid ' + wc,
                      background: 'rgba(10, 14, 30, 0.4)',
                      transition: 'background 0.15s'
                    }}
                    onMouseEnter={e => e.currentTarget.style.background = 'rgba(15, 20, 40, 0.6)'}
                    onMouseLeave={e => e.currentTarget.style.background = 'rgba(10, 14, 30, 0.4)'}
                    >
                      <span style={{
                        display: 'inline-block', fontSize: 8, fontWeight: 500,
                        padding: '2px 5px', borderRadius: 2, letterSpacing: 1,
                        color: wc, background: wc + '10', border: '1px solid ' + wc + '20',
                        marginBottom: 8
                      }}>{wt}/5</span>

                      <p style={{ fontSize: 14, fontWeight: 400, color: '#c8c6c0', lineHeight: 1.5, marginBottom: 3 }}>
                        {gap.question_cs}
                      </p>
                      <p style={{ fontSize: 11, color: '#4a4a56', fontWeight: 300, marginBottom: 10, lineHeight: 1.4 }}>
                        {gap.question_en}
                      </p>

                      <p style={{ fontSize: 12, color: '#8a8a96', lineHeight: 1.6, fontWeight: 300 }}>
                        <span style={{ color: '#1a3670', marginRight: 4 }}>&#8594;</span>
                        {gap.remediation}
                      </p>

                      <p style={{ fontSize: 8, color: '#3a3a46', letterSpacing: 1, marginTop: 10, textTransform: 'uppercase' }}>
                        {gap.article_ref}  |  {gap.domain_name_cs}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          <div>
            <p style={{ fontSize: 9, letterSpacing: 3, color: '#1a3670', textTransform: 'uppercase', marginBottom: 8 }}>Full Analysis</p>
            <h2 style={{ fontSize: 16, fontWeight: 500, color: '#c8c6c0', letterSpacing: '-0.01em', marginBottom: 12 }}>
              Analyza podle domen
            </h2>

            {result.domain_scores.filter(ds => ds.gaps.length > 0).map(ds => (
              <Expandable
                key={ds.domain_id}
                title={ds.domain_name_cs + ' \u2014 ' + Math.round(ds.percentage) + '%'}
                count={ds.gaps.length}
              >
                <div style={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                  {ds.gaps.map((gap, i) => {
                    const wt = gap.weight;
                    const wc = wt >= 5 ? '#a04040' : wt >= 4 ? '#9e8528' : '#4a4a56';
                    return (
                      <div key={i} style={{
                        padding: '14px 16px 14px 14px',
                        borderLeft: '2px solid ' + wc,
                        background: 'rgba(8, 10, 24, 0.4)',
                      }}>
                        <p style={{ fontSize: 13, fontWeight: 400, color: '#b0aea8', lineHeight: 1.5, marginBottom: 2 }}>
                          {gap.question_cs}
                        </p>
                        <p style={{ fontSize: 10, color: '#4a4a56', fontWeight: 300, marginBottom: 8 }}>
                          {gap.question_en}
                        </p>
                        <p style={{ fontSize: 11, color: '#6a6a76', lineHeight: 1.6, fontWeight: 300 }}>
                          <span style={{ color: '#1a3670', marginRight: 4 }}>&#8594;</span>
                          {gap.remediation}
                        </p>
                        <p style={{ fontSize: 7, color: '#3a3a46', letterSpacing: 1, marginTop: 8, textTransform: 'uppercase' }}>
                          {gap.article_ref}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </Expandable>
            ))}

            {result.domain_scores.filter(d => !d.gaps.length).length > 0 && (
              <div style={{ marginTop: 16, padding: '16px', background: 'rgba(10, 14, 30, 0.3)' }}>
                <p style={{ fontSize: 9, letterSpacing: 3, color: '#3d8c6a', textTransform: 'uppercase', marginBottom: 10 }}>V souladu</p>
                {result.domain_scores.filter(d => !d.gaps.length).map(d => (
                  <p key={d.domain_id} style={{ fontSize: 12, color: '#6a6a76', marginBottom: 4 }}>
                    <span style={{ color: '#3d8c6a', marginRight: 6 }}>&#10003;</span>
                    {d.domain_name_cs} - {Math.round(d.percentage)}%
                  </p>
                ))}
              </div>
            )}
          </div>

          <div style={{ marginTop: 32, paddingTop: 16, borderTop: '1px solid rgba(255,255,255,0.03)' }}>
            <p style={{ fontSize: 8, color: '#3a3a46', letterSpacing: 1 }}>
              Zakon c. 264/2025 Sb.  |  EU NIS2  |  NUKIB  |  2026 Noxra
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Results;
