// frontend/src/challenge/ChallengeGenerator.jsx
import "react";
import { useState, useEffect } from "react";
import { MCQChallenge } from "./MCQChallenge.jsx";
import { useApi } from "../utils/api.js";
import "./ChallengeGenerator.css";

export function ChallengeGenerator() {
  const [challenge, setChallenge] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [difficulty, setDifficulty] = useState("easy");
  const [quota, setQuota] = useState(null);
  const { makeRequest } = useApi();

  useEffect(() => {
    fetchQuota();
  }, []);

  const fetchQuota = async () => {
    try {
      const data = await makeRequest("quota");
      setQuota(data);
    } catch (err) {
      console.log(err);
    }
  };

  const generateChallenge = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await makeRequest("generate-challenge", {
        method: "POST",
        body: JSON.stringify({ difficulty }),
      });
      setChallenge(data);
      fetchQuota();
    } catch (err) {
      setError(err.message || "No se pudo generar el reto.");
    } finally {
      setIsLoading(false);
    }
  };

  const getNextResetTime = () => {
    if (!quota?.last_reset_date) return null;
    const resetDate = new Date(quota.last_reset_date);
    resetDate.setHours(resetDate.getHours() + 24);
    return resetDate;
  };

  return (
    <div className="cg-grid">
      <section className="cg-card cg-main">
        <header className="cg-card-header">
          <div>
            <h2>Generador de retos</h2>
            <p>Elige dificultad y deja que la IA te pregunte.</p>
          </div>
          <div className="cg-quota-pill">
            <span>Retos hoy</span>
            <strong>{quota?.quota_remaining ?? 0}</strong>
          </div>
        </header>

        {quota?.quota_remaining === 0 && (
          <div className="cg-alert">
            <span>Has alcanzado el límite diario.</span>
            {getNextResetTime() && (
              <span>
                Próximo reinicio:{" "}
                {getNextResetTime().toLocaleString()}
              </span>
            )}
          </div>
        )}

        <div className="cg-controls">
          <div className="cg-control-group">
            <label htmlFor="difficulty">Dificultad</label>
            <select
              id="difficulty"
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              disabled={isLoading || quota?.quota_remaining === 0}
            >
              <option value="easy">Fácil</option>
              <option value="medium">Media</option>
              <option value="hard">Difícil</option>
            </select>
          </div>

          <button
            onClick={generateChallenge}
            disabled={isLoading || quota?.quota_remaining === 0}
            className="cg-button-primary"
          >
            {isLoading ? "Generando..." : "Generar reto"}
          </button>
        </div>

        {error && (
          <div className="cg-error">
            <p>{error}</p>
          </div>
        )}

        {challenge && <MCQChallenge challenge={challenge} />}
      </section>
    </div>
  );
}
