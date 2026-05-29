"""Chat Input component."""
import React, { useState } from "react";
import "../styles/ChatInput.css";

interface Props {
  onSendMessage: (message: string, includeSummary: boolean) => void;
  loading: boolean;
}

const ChatInput: React.FC<Props> = ({ onSendMessage, loading }) => {
  const [input, setInput] = useState("");
  const [includeSummary, setIncludeSummary] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !loading) {
      onSendMessage(input, includeSummary);
      setInput("");
    }
  };

  return (
    <form className="chat-input-form" onSubmit={handleSubmit}>
      <div className="input-options">
        <label className="summary-checkbox">
          <input
            type="checkbox"
            checked={includeSummary}
            onChange={(e) => setIncludeSummary(e.target.checked)}
            disabled={loading}
          />
          Include Summary
        </label>
      </div>
      <div className="input-wrapper">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about your documents..."
          disabled={loading}
          className="chat-input"
        />
        <button type="submit" disabled={loading || !input.trim()} className="send-button">
          {loading ? "⏳" : "📤"}
        </button>
      </div>
    </form>
  );
};

export default ChatInput;
