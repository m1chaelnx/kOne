import { useState } from 'react';
import Welcome from './pages/Welcome';
import Assessment from './pages/Assessment';
import Results from './pages/Results';
import './App.css';

function App() {
  const [page, setPage] = useState('welcome');
  const [companyInfo, setCompanyInfo] = useState(null);
  const [result, setResult] = useState(null);

  const startAssessment = (info) => { setCompanyInfo(info); setPage('assessment'); };
  const showResults = (data) => { setResult(data); setPage('results'); };
  const restart = () => { setCompanyInfo(null); setResult(null); setPage('welcome'); };

  return (
    <div className="app">
      <header className="app-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, cursor: 'pointer' }} onClick={restart}>
          <span style={{
            fontSize: 13, fontWeight: 500, letterSpacing: 4,
            color: 'var(--text-1)', textTransform: 'uppercase'
          }}>Noxra</span>
          <span style={{
            fontSize: 10, color: 'var(--text-3)', letterSpacing: 2
          }}>kOne</span>
        </div>
        <span style={{
          fontSize: 9, color: 'var(--text-3)', letterSpacing: 3, textTransform: 'uppercase'
        }}>NIS2 Scanner</span>
      </header>

      <main className="app-main">
        {page === 'welcome' && <Welcome onStart={startAssessment} />}
        {page === 'assessment' && <Assessment companyInfo={companyInfo} onComplete={showResults} onBack={restart} />}
        {page === 'results' && <Results result={result} onRestart={restart} />}
      </main>

      <footer className="app-footer">
        <span>2026 Noxra</span>
        <span>noxra.ai</span>
      </footer>
    </div>
  );
}

export default App;
