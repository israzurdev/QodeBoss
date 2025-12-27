import React, { useEffect, useState } from "react";
import { useApi } from "../utils/api.js";
import { MCQChallenge } from "../challenge/MCQChallenge.jsx";
import "../challenge/MCQChallenge.css";

export function HistoryPanel() {
  const { makeRequest } = useApi();
  const [items, setItems] = useState([]);
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState(null);
  const [selectedChallenge, setSelectedChallenge] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await makeRequest("my-history");
        setItems(data.challenges || []);
        setStatus("ready");
      } catch (err) {
        setError(err.message || "No se pudo cargar el historial.");
        setStatus("error");
      }
    };

    load();
  }, [makeRequest]);

  if (status === "loading") {
    return <p>Cargando historial...</p>;
  }

  if (status === "error") {
    return <p>{error}</p>;
  }

  if (!items.length) {
    return <p>No tienes retos en tu historial todavía.</p>;
  }

  return (
    <div className="history-layout">
      <div className="history-list">
        {items.map((ch) => (
          <button
            key={ch.id}
            className={
              selectedChallenge && selectedChallenge.id === ch.id
                ? "history-item history-item-active"
                : "history-item"
            }
            onClick={() => setSelectedChallenge(ch)}
          >
            <div className="mcq-header">
              <span className={`mcq-difficulty mcq-${ch.difficulty}`}>
                {ch.difficulty.toUpperCase()}
              </span>
              <span className="mcq-timestamp">
                {new Date(ch.timestamp).toLocaleString()}
              </span>
            </div>
            <h3 className="mcq-title">{ch.title}</h3>
          </button>
        ))}
      </div>

      <div className="history-detail">
        {selectedChallenge ? (
          <MCQChallenge challenge={selectedChallenge} />
        ) : (
          <p>Selecciona un reto del listado para revisarlo.</p>
        )}
      </div>
    </div>
  );
}
