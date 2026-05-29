"""Chat Message component."""
import React, { useState } from "react";
import * as Types from "../types/api";
import CitationViewer from "./CitationViewer";
import "../styles/ChatMessage.css";

interface Props {
  message: Types.ChatMessage;
}

const ChatMessage: React.FC<Props> = ({ message }) => {
  const [showSummary, setShowSummary] = useState(false);

  return (
    <div className={`chat-message ${message.sender}`}>
      <div className="message-header">
        <span className="sender">{message.sender === "user" ? "👤 You" : "🤖 Assistant"}</span>
        <span className="timestamp">{new Date(message.timestamp).toLocaleTimeString()}</span>
      </div>
      <div className="message-content">{message.content}</div>

      {message.citations && message.citations.length > 0 && (
        <CitationViewer citations={message.citations} />
      )}

      {message.summary && (
        <div className="summary-section">
          <button onClick={() => setShowSummary(!showSummary)} className="summary-toggle">
            📝 {showSummary ? "Hide" : "Show"} Summary
          </button>
          {showSummary && <div className="summary-content">{message.summary}</div>}
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
