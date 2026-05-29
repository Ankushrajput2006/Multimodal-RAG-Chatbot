"""API client for frontend."""
import axios, { AxiosInstance } from "axios";
import * as Types from "../types/api";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  // Health & Status
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response = await this.client.get("/health");
    return response.data;
  }

  async getStats(): Promise<Types.ChatbotStats> {
    const response = await this.client.get("/stats");
    return response.data;
  }

  // Chat
  async sendMessage(
    question: string,
    includeSummary: boolean = false,
    language?: string
  ): Promise<Types.ChatResponse> {
    const response = await this.client.post("/chat", null, {
      params: {
        question,
        include_summary: includeSummary,
        language,
      },
    });
    return response.data;
  }

  async getChatHistory(): Promise<{ messages: Types.ChatMessage[] }> {
    const response = await this.client.get("/chat-history");
    return response.data;
  }

  async clearChatHistory(): Promise<{ status: string; message: string }> {
    const response = await this.client.delete("/chat-history");
    return response.data;
  }

  // Documents
  async uploadDocument(file: File): Promise<Types.DocumentUploadResponse> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await this.client.post("/documents/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  }

  // Languages
  async getSupportedLanguages(): Promise<{ languages: Types.Language[] }> {
    const response = await this.client.get("/languages");
    return response.data;
  }

  async detectLanguage(text: string): Promise<Types.LanguageInfo> {
    const response = await this.client.post("/detect-language", null, {
      params: { text },
    });
    return response.data;
  }

  // Settings
  async getSettings(): Promise<Types.Settings> {
    const response = await this.client.get("/settings");
    return response.data;
  }

  // Index Management
  async saveIndex(): Promise<{ status: string; message: string }> {
    const response = await this.client.post("/index/save");
    return response.data;
  }

  async getIndexStats(): Promise<Types.IndexStats> {
    const response = await this.client.get("/index/stats");
    return response.data;
  }
}

export default new APIClient();
