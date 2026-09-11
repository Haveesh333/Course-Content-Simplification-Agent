import React, { useState } from 'react';
import { useSimplify } from './hooks/useSimplify';
import UploadArea from './components/UploadArea';
import TextInput from './components/TextInput';
import LevelSelector from './components/LevelSelector';
import SimplifyButton from './components/SimplifyButton';
import ResultsPanel from './components/ResultsPanel';
import TermsPanel from './components/TermsPanel';
import ExamplesPanel from './components/ExamplesPanel';
import QuizPanel from './components/QuizPanel';
import './styles/App.css';

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [text, setText] = useState<string>('');
  const [level, setLevel] = useState<string>('beginner');
  const { simplify, data, loading, error } = useSimplify();

  const handleSimplify = () => {
    simplify(file, text, level);
  };

  return (
    <div className="app">
      <header className="app__header">
        <h1>CourseEase AI</h1>
        <p className="app__subtitle">Course Content Simplification Agent</p>
      </header>

      <main className="app__main">
        <section className="input-card">
          <UploadArea file={file} onFileChange={setFile} />
          <div className="divider"><span>or</span></div>
          <TextInput value={text} onChange={setText} />
          <LevelSelector level={level} onChange={setLevel} />
          <SimplifyButton
            onClick={handleSimplify}
            loading={loading}
            disabled={!file && !text.trim()}
          />
          {error && <div className="error-banner">{error}</div>}
        </section>

        {data && (
          <section className="results">
            <ResultsPanel
              explanation={data.simplified_explanation}
              keyPoints={data.key_points}
            />
            {data.difficult_terms.length > 0 && (
              <TermsPanel terms={data.difficult_terms} />
            )}
            {data.examples.length > 0 && (
              <ExamplesPanel examples={data.examples} />
            )}
            <QuizPanel quiz={data.quiz} />
          </section>
        )}
      </main>

      {loading && (
        <div className="loading-overlay">
          <div className="loading-overlay__spinner" />
          <p>Analyzing your content...</p>
        </div>
      )}
    </div>
  );
};

export default App;
