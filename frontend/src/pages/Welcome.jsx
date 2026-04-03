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
  { value: 'micro', label: '1–9 zaměstnanců' },
  { value: 'small', label: '10–49 zaměstnanců' },
  { value: 'medium', label: '50–249 zaměstnanců' },
  { value: 'large', label: '250+ zaměstnanců' },
];

function Welcome({ onStart }) {
  const [name, setName] = useState('');
  const [size, setSize] = useState('');
  const [sector, setSector] = useState('');
  const canStart = name.trim() && size && sector;

  return (
    <div className="fade-in">
      <div className="mb-48" style={{ marginTop: 32 }}>
        <div className="label-upper mb-16">NIS2 Compliance Assessment</div>
        <h1 style={{ marginBottom: 12, maxWidth: 480 }}>
          Vyhovujete zákonu,{' '}
          <span style={{ color: 'var(--chrome)' }}>nebo si to jen myslíte?</span>
        </h1>
        <p style={{ fontSize: 14, color: 'var(--text-2)', maxWidth: 440, lineHeight: 1.7, fontWeight: 300 }}>
          Zákon o kybernetické bezpečnosti je v platnosti. Pokuty dosahují 250 milionů CZK. 
          Zjistěte skutečný stav vaší organizace za 10 minut.
        </p>
      </div>

      <div className="chrome-line mb-32" />

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 200px', gap: 32, alignItems: 'start' }}>
        <div>
          <div className="mb-16">
            <label>Organizace</label>
            <input type="text" placeholder="Název vaší organizace" value={name} onChange={(e) => setName(e.target.value)} />
          </div>
          <div className="mb-16">
            <label>Velikost</label>
            <select value={size} onChange={(e) => setSize(e.target.value)}>
              <option value="">Vyberte...</option>
              {SIZES.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
            </select>
          </div>
          <div className="mb-24">
            <label>Sektor</label>
            <select value={sector} onChange={(e) => setSector(e.target.value)}>
              <option value="">Vyberte...</option>
              {SECTORS.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
            </select>
          </div>
          <button
            className="btn-chrome"
            style={{ width: '100%', height: 44, border: 'none', borderRadius: 'var(--r)', fontFamily: 'var(--font)', cursor: canStart ? 'pointer' : 'not-allowed', opacity: canStart ? 1 : 0.2, transition: 'all 0.2s' }}
            onClick={() => canStart && onStart({ company_name: name.trim(), company_size: size, sector })}
            disabled={!canStart}
          >
            Zahájit hodnocení →
          </button>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 1, background: 'var(--edge)', borderRadius: 'var(--r)', overflow: 'hidden' }}>
          <div style={{ background: 'var(--surface-1)', padding: '20px 16px', textAlign: 'center' }}>
            <div style={{ fontSize: 32, fontWeight: 300, letterSpacing: '-2px', color: 'var(--chrome)' }}>41</div>
            <div className="label-upper" style={{ fontSize: 8, marginTop: 6, color: 'var(--text-3)' }}>Kontrol</div>
          </div>
          <div style={{ background: 'var(--surface-1)', padding: '20px 16px', textAlign: 'center' }}>
            <div style={{ fontSize: 32, fontWeight: 300, letterSpacing: '-2px', color: 'var(--chrome)' }}>10</div>
            <div className="label-upper" style={{ fontSize: 8, marginTop: 6, color: 'var(--text-3)' }}>Domén</div>
          </div>
          <div style={{ background: 'var(--surface-1)', padding: '20px 16px', textAlign: 'center' }}>
            <div style={{ fontSize: 32, fontWeight: 300, letterSpacing: '-2px', color: 'var(--chrome)' }}>10</div>
            <div className="label-upper" style={{ fontSize: 8, marginTop: 6, color: 'var(--text-3)' }}>Minut</div>
          </div>
        </div>
      </div>

      <div className="chrome-line mt-48" />

      <p className="mono text-center mt-16" style={{ fontSize: 10 }}>
        Zákon č. 264/2025 Sb. · EU NIS2 Directive · NÚKIB
      </p>
    </div>
  );
}

export default Welcome;
