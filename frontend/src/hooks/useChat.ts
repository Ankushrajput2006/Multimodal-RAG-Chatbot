"""Hook for managing chat state."""
import { useState, useCallback } from "react";
import * as Types from "../types/api";
import apiClient from "../utils/apiClient";

export const useChat = () => {
  const [messages, setMessages] = useState<Types.ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (
      question: string,
      includeSummary: boolean = false,
      language?: string
    ) => {
      setLoading(true);
      setError(null);

      try {
        // Add user message
        const userMessage: Types.ChatMessage = {
          id: Date.now().toString(),
          sender: "user",
          content: question,
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, userMessage]);

        // Get response
        const response = await apiClient.sendMessage(
          question,
          includeSummary,
          language
        );

        // Add assistant message
        const assistantMessage: Types.ChatMessage = {
          id: (Date.now() + 1).toString(),
          sender: "assistant",
          content: response.answer,
          citations: response.citations,
          summary: response.summary,
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Failed to send message";
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  const loadHistory = useCallback(async () => {
    try {
      const history = await apiClient.getChatHistory();
      setMessages(history.messages);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to load history";
      setError(errorMessage);
    }
  }, []);

  return {
    messages,
    loading,
    error,
    sendMessage,
    clearMessages,
    loadHistory,
  };
};
