"""Chat Area component."""
import React, { useRef, useEffect } from "react";
import { useChat } from "../hooks/useChat";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import "../styles/ChatArea.css";

const ChatArea: React.FC = () => {
  const { messages, loading, error, sendMessage } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (message: string, includeSummary: boolean) => {
    await sendMessage(message, includeSummary);
  };

  return (
    <div className="chat-area">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h2>🤖 Welcome to Multimodal RAG Chatbot</h2>
            <p>Upload documents to get started and ask questions!</p>
          </div>
        ) : (
          messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))
        )}
        {error && <div className="error-message">{error}</div>}
        <div ref={messagesEndRef} />
      </div>
      <ChatInput onSendMessage={handleSendMessage} loading={loading} />
    </div>
  );
};

export default ChatArea;
