import React, { useState } from 'react';
import { QuizQuestion } from '../types';

interface QuizPanelProps {
  quiz: QuizQuestion[];
}

const OPTION_LETTERS = ['A', 'B', 'C', 'D'];

const QuizPanel: React.FC<QuizPanelProps> = ({ quiz }) => {
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState<number | null>(null);

  const handleSelect = (questionIndex: number, letter: string) => {
    if (submitted) return;
    setSelectedAnswers((prev) => ({ ...prev, [questionIndex]: letter }));
  };

  const handleSubmit = () => {
    let correct = 0;
    quiz.forEach((q, i) => {
      if (selectedAnswers[i] === q.answer) {
        correct += 1;
      }
    });
    setScore(correct);
    setSubmitted(true);
  };

  const handleRetry = () => {
    setSelectedAnswers({});
    setSubmitted(false);
    setScore(null);
  };

  const allAnswered = quiz.length > 0 && quiz.every((_, i) => selectedAnswers[i] !== undefined);

  return (
    <section className="quiz-panel">
      <h2 className="quiz-panel__title">Quiz</h2>

      {submitted && score !== null && (
        <div className="quiz-panel__score">
          You scored <strong>{score} / {quiz.length}</strong>
        </div>
      )}

      <ol className="quiz-panel__questions">
        {quiz.map((q, qIndex) => {
          const selected = selectedAnswers[qIndex];
          const isCorrect = selected === q.answer;

          return (
            <li key={qIndex} className="quiz-panel__question">
              <p className="quiz-panel__question-text">{q.question}</p>
              <ul className="quiz-panel__options">
                {q.options.map((option, oIndex) => {
                  const letter = OPTION_LETTERS[oIndex];
                  const isSelected = selected === letter;
                  const isThisCorrect = letter === q.answer;

                  let optionClass = 'quiz-panel__option';
                  if (submitted) {
                    if (isSelected && isCorrect) {
                      optionClass += ' quiz-panel__option--correct';
                    } else if (isSelected && !isCorrect) {
                      optionClass += ' quiz-panel__option--incorrect';
                    } else if (isThisCorrect) {
                      optionClass += ' quiz-panel__option--correct-answer';
                    }
                  } else if (isSelected) {
                    optionClass += ' quiz-panel__option--selected';
                  }

                  return (
                    <li key={letter} className={optionClass}>
                      <label className="quiz-panel__option-label">
                        <input
                          type="radio"
                          name={`question-${qIndex}`}
                          value={letter}
                          checked={isSelected}
                          onChange={() => handleSelect(qIndex, letter)}
                          disabled={submitted}
                          className="quiz-panel__radio"
                        />
                        {option}
                      </label>
                    </li>
                  );
                })}
                {submitted && !isCorrect && selected !== undefined && (
                  <li className="quiz-panel__correct-hint">
                    Correct answer:{' '}
                    <span className="quiz-panel__correct-hint-text">
                      {q.options[OPTION_LETTERS.indexOf(q.answer)]}
                    </span>
                  </li>
                )}
              </ul>
            </li>
          );
        })}
      </ol>

      <div className="quiz-panel__actions">
        {!submitted ? (
          <button
            type="button"
            className="quiz-panel__submit-btn"
            onClick={handleSubmit}
            disabled={!allAnswered}
          >
            Submit Quiz
          </button>
        ) : (
          <button
            type="button"
            className="quiz-panel__retry-btn"
            onClick={handleRetry}
          >
            Retry
          </button>
        )}
      </div>
    </section>
  );
};

export default QuizPanel;
