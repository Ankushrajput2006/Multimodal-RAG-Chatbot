"""Sidebar component."""
import React, { useEffect, useState } from "react";
import * as Types from "../types/api";
import apiClient from "../utils/apiClient";
import "../styles/Sidebar.css";

interface Props {
  onViewChange: (view: "chat" | "settings") => void;
  currentView: "chat" | "settings";
  darkMode: boolean;
  onToggleDarkMode: () => void;
}

const Sidebar: React.FC<Props> = ({
  onViewChange,
  currentView,
  darkMode,
  onToggleDarkMode,
}) => {
  const [stats, setStats] = useState<Types.ChatbotStats | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await apiClient.getStats();
        setStats(data);
      } catch (error) {
        console.error("Failed to fetch stats:", error);
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleClearHistory = async () => {
    if (window.confirm("Are you sure you want to clear chat history?")) {
      try {
        await apiClient.clearChatHistory();
        window.location.reload();
      } catch (error) {
        console.error("Failed to clear history:", error);
      }
    }
  };

  const handleSaveIndex = async () => {
    try {
      await apiClient.saveIndex();
      alert("Index saved successfully!");
    } catch (error) {
      console.error("Failed to save index:", error);
    }
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1>🤖 RAG Chatbot</h1>
        <button
          className="theme-toggle"
          onClick={onToggleDarkMode}
          title={darkMode ? "Light mode" : "Dark mode"}
        >
          {darkMode ? "☀️" : "🌙"}
        </button>
      </div>

      <nav className="sidebar-nav">
        <button
          className={`nav-item ${currentView === "chat" ? "active" : ""}`}
          onClick={() => onViewChange("chat")}
        >
          💬 Chat
        </button>
        <button
          className={`nav-item ${currentView === "settings" ? "active" : ""}`}
          onClick={() => onViewChange("settings")}
        >
          ⚙️ Settings
        </button>
      </nav>

      {stats && (
        <div className="stats-panel">
          <h3>📊 Statistics</h3>
          <div className="stat-item">
            <span>Documents</span>
            <strong>{stats.total_documents}</strong>
          </div>
          <div className="stat-item">
            <span>Chat History</span>
            <strong>{stats.chat_history_length}</strong>
          </div>
          <div className="stat-item">
            <span>Embedding Dim</span>
            <strong>{stats.embedding_dim}</strong>
          </div>
        </div>
      )}

      <div className="sidebar-actions">
        <button onClick={handleClearHistory} className="action-button danger">
          🗑️ Clear History
        </button>
        <button onClick={handleSaveIndex} className="action-button">
          💾 Save Index
        </button>
      </div>

      <div className="sidebar-footer">
        <p>Built with React & TypeScript</p>
      </div>
    </aside>
  );
};

export default Sidebar;
