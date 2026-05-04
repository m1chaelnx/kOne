import { useState } from 'react';

const SECTORS = [
  { value: 'energy', label: 'Energetika' },
  { value: 'transport', label: 'Doprava' },
  { value: 'healthcare', label: 'Zdravotnictví' },
  { value: 'digital_infra', label: 'Digitální infrastruktura' },
  { value: 'ict_services', label: 'ICT služby' },
  { value: 'public_admin', label: 'Veřejná správa' },
  { value: 'manufacturing', label: 'Výroba' },
  { value: 'finance', label: 'Finance' },
  { value: 'water', label: 'Vodní hospodářství' },
  { value: 'food', label: 'Potravinářství' },
  { value: 'chemicals', label: 'Chemický průmysl' },
  { value: 'research', label: 'Výzkum' },
  { value: 'defense', label: 'Obranný průmysl' },
  { value: 'other', label: 'Jiné' },
];

const SIZES = [
  { value: 'micro', label: '1-9 zaměstnanců' },
  { value: 'small', label: '10-49 zaměstnanců' },
  { value: 'medium', label: '50-249 zaměstnanců' },
  { value: 'large', label: '250+ zaměstnanců' },
];

function Welcome({ onStart }) {
  const [name, setName] = useState('');
  const [size, setSize] = useState('');
  const [sector, setSector] = useState('');
  const canStart = name.trim() && size && sector;

  return (
    <div className="fade-in" style={{ maxWidth: 520, margin: '0 auto' }}>

      {/* Hero — tight, direct, no wasted space */}
      <div style={{ marginTop: 40, marginBottom: 48 }}>
        <p style={{
          fontSize: 11, fontWeight: 500, letterSpacing: 3,
          color: 'var(--chrome)', textTransform: 'uppercase', marginBottom: 16
        }}>
          NIS2 Compliance Assessment
        </p>

        <h1 style={{
          fontSize: 32, fontWeight: 500, letterSpacing: '-0.03em',
          lineHeight: 1.2, marginBottom: 16, color: 'var(--text-1)'
        }}>
          Vyhovujete zákonu o kybernetické bezpečnosti?
        </h1>

        <p style={{
          fontSize: 15, lineHeight: 1.7, color: 'var(--text-2)',
          fontWeight: 300, marginBottom: 0
        }}>
          Zákon č. 264/2025 Sb. je v platnosti. Pokuty až 250 mil. CZK.
          Zjistěte skutečný stav vaší organizace za 10 minut.
        </p>
      </div>

      {/* Stats bar — horizontal, compact, above the form */}
      <div style={{
        display: 'grid', gridTemplateColumns: '1fr 1fr 1fr',
        borderTop: '1px solid var(--edge-subtle)',
        borderBottom: '1px solid var(--edge-subtle)',
        marginBottom: 40
      }}>
        {[
          { val: '41', lbl: 'Kontrol' },
          { val: '10', lbl: 'Domén' },
          { val: '10 min', lbl: 'Čas' },
        ].map((s, i) => (
          <div key={i} style={{
            padding: '16px 0', textAlign: 'center',
            borderLeft: i > 0 ? '1px solid var(--edge-subtle)' : 'none'
          }}>
            <div style={{ fontSize: 22, fontWeight: 400, color: 'var(--text-1)', letterSpacing: '-1px' }}>{s.val}</div>
            <div style={{ fontSize: 9, color: 'var(--text-3)', letterSpacing: 3, textTransform: 'uppercase', marginTop: 2 }}>{s.lbl}</div>
          </div>
        ))}
      </div>

      {/* Form — clean, no card wrapper, just fields */}
      <div style={{ marginBottom: 16 }}>
        <label>Organizace</label>
        <input
          type="text"
          placeholder="Nazev vasi organizace"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 24 }}>
        <div>
          <label>Velikost</label>
          <select value={size} onChange={(e) => setSize(e.target.value)}>
            <option value="">Vyberte...</option>
            {SIZES.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
          </select>
        </div>
        <div>
          <label>Sektor</label>
          <select value={sector} onChange={(e) => setSector(e.target.value)}>
            <option value="">Vyberte...</option>
            {SECTORS.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
          </select>
        </div>
      </div>

      <button
        className="btn-chrome"
        style={{
          width: '100%', height: 48, border: 'none',
          borderRadius: 'var(--r)', fontFamily: 'var(--font)',
          cursor: canStart ? 'pointer' : 'not-allowed',
          opacity: canStart ? 1 : 0.15,
          fontSize: 12, letterSpacing: 2,
          transition: 'all 0.2s'
        }}
        onClick={() => canStart && onStart({
          company_name: name.trim(),
          company_size: size,
          sector
        })}
        disabled={!canStart}
      >
        ZAHAJIT HODNOCENI
      </button>

      {/* Trust bar — legal references, subtle */}
      <div style={{
        marginTop: 48, paddingTop: 24,
        borderTop: '1px solid var(--edge)',
        display: 'flex', justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <p style={{ fontSize: 10, color: 'var(--text-3)', letterSpacing: 1 }}>
          Zákon č. 264/2025 Sb. | EU NIS2 | NUKIB
        </p>
        <p style={{ fontSize: 10, color: 'var(--text-3)', letterSpacing: 1 }}>
          Zdarma | Bez registrace
        </p>
      </div>
    </div>
  );
}

export default Welcome;
