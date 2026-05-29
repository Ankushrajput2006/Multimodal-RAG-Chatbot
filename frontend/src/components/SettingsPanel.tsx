"""Settings Panel component."""
import React, { useEffect, useState } from "react";
import * as Types from "../types/api";
import apiClient from "../utils/apiClient";
import "../styles/SettingsPanel.css";

const SettingsPanel: React.FC = () => {
  const [settings, setSettings] = useState<Types.Settings | null>(null);
  const [languages, setLanguages] = useState<Types.Language[]>([]);
  const [indexStats, setIndexStats] = useState<Types.IndexStats | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [settingsData, languagesData, indexStatsData] = await Promise.all([
          apiClient.getSettings(),
          apiClient.getSupportedLanguages(),
          apiClient.getIndexStats(),
        ]);
        setSettings(settingsData);
        setLanguages(languagesData.languages);
        setIndexStats(indexStatsData);
      } catch (error) {
        console.error("Failed to fetch settings:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="settings-panel">
      <h2>⚙️ Settings</h2>

      {settings && (
        <div className="settings-section">
          <h3>Model Configuration</h3>
          <div className="setting-item">
            <label>Embedding Model</label>
            <p>{settings.embedding_model}</p>
          </div>
          <div className="setting-item">
            <label>LLM Model</label>
            <p>{settings.llm_model}</p>
          </div>
          <div className="setting-item">
            <label>Device</label>
            <p>{settings.device}</p>
          </div>
        </div>
      )}

      {languages.length > 0 && (
        <div className="settings-section">
          <h3>🌍 Supported Languages</h3>
          <div className="languages-grid">
            {languages.map((lang) => (
              <div key={lang.code} className="language-item">
                <code>{lang.code}</code> - {lang.name}
              </div>
            ))}
          </div>
        </div>
      )}

      {indexStats && (
        <div className="settings-section">
          <h3>📊 Index Statistics</h3>
          <div className="setting-item">
            <label>Total Documents</label>
            <p>{indexStats.total_documents}</p>
          </div>
          <div className="setting-item">
            <label>Embedding Dimension</label>
            <p>{indexStats.embedding_dim}</p>
          </div>
          <div className="setting-item">
            <label>Index Size</label>
            <p>{indexStats.index_size}</p>
          </div>
          <div className="setting-item">
            <label>Model</label>
            <p>{indexStats.model_name}</p>
          </div>
        </div>
      )}

      <div className="settings-section">
        <h3>About</h3>
        <p>Multimodal RAG Chatbot v1.0.0</p>
        <p>A powerful retrieval-augmented generation chatbot with multimodal support.</p>
      </div>
    </div>
  );
};

export default SettingsPanel;
