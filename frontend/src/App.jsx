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
        <span className="header-tag" style={{ cursor: 'pointer' }} onClick={restart}>kOne</span>
        <span className="header-tag">Noxra Enterprises</span>
      </header>

      <main className="app-main">
        {page === 'welcome' && <Welcome onStart={startAssessment} />}
        {page === 'assessment' && <Assessment companyInfo={companyInfo} onComplete={showResults} onBack={restart} />}
        {page === 'results' && <Results result={result} onRestart={restart} />}
      </main>

      <footer className="app-footer">
        <span>© 2026 Noxra Enterprises</span>
        <span>NIS2 · Zákon 264/2025 Sb.</span>
      </footer>
    </div>
  );
}

export default App;
