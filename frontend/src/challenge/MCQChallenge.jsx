// MCQChallenge.jsx
import React, { useEffect, useState } from "react";
import "./MCQChallenge.css";

export function MCQChallenge({ challenge }) {
  const [selectedOption, setSelectedOption] = useState(null);
  const [isSubmitted, setIsSubmitted] = useState(false);

  useEffect(() => {
    setSelectedOption(null);
    setIsSubmitted(false);
  }, [challenge?.id]);

  if (!challenge) return null;

  const handleOptionClick = (index) => {
    if (isSubmitted) return;
    setSelectedOption(index);
  };

  const handleSubmit = () => {
    if (selectedOption === null) return;
    setIsSubmitted(true);
  };

  const isCorrect =
    isSubmitted && selectedOption === challenge.correct_answer_id;

  return (
    <div className="mcq-card">
      <div className="mcq-header">
        <span className={`mcq-difficulty mcq-${challenge.difficulty}`}>
          {challenge.difficulty.toUpperCase()}
        </span>
        <span className="mcq-timestamp">
          {challenge.timestamp &&
            new Date(challenge.timestamp).toLocaleString()}
        </span>
      </div>

      <h3 className="mcq-title">{challenge.title}</h3>

      {/* Bloque de código, si existe */}
      {challenge.code && challenge.code.trim() !== "" && (
        <div className="mcq-code-block">
          <pre>
            <code>{challenge.code}</code>
          </pre>
        </div>
      )}

      <ul className="mcq-options">
        {challenge.options.map((option, index) => {
          const isSelected = selectedOption === index;
          const isCorrectOption =
            isSubmitted && index === challenge.correct_answer_id;
          const isWrongSelected =
            isSubmitted && isSelected && !isCorrectOption;

          let className = "mcq-option";
          if (isSelected) className += " mcq-option-selected";
          if (isCorrectOption) className += " mcq-option-correct";
          if (isWrongSelected) className += " mcq-option-wrong";

          return (
            <li
              key={index}
              className={className}
              onClick={() => handleOptionClick(index)}
            >
              {option}
            </li>
          );
        })}
      </ul>

      <div className="mcq-actions">
        <button
          className="mcq-submit-button"
          onClick={handleSubmit}
          disabled={isSubmitted || selectedOption === null}
        >
          {isSubmitted ? "Respuesta enviada" : "Comprobar respuesta"}
        </button>
      </div>

      {isSubmitted && (
        <div className="mcq-explanation">
          <p>{isCorrect ? "✅ ¡Correcto!" : "❌ Respuesta incorrecta."}</p>
          <p>{challenge.explanation}</p>
        </div>
      )}
    </div>
  );
}
