"""TypeScript types for frontend."""

export interface Citation {
  type: string;
  value: string;
  full_match: string;
  url?: string;
  author?: string;
  year?: string;
}

export interface ChatResponse {
  question: string;
  answer: string;
  citations: Citation[];
  summary?: string;
  original_language: string;
  retrieved_documents: number;
}

export interface ChatMessage {
  id: string;
  sender: "user" | "assistant";
  content: string;
  citations?: Citation[];
  summary?: string;
  timestamp: string;
}

export interface DocumentUploadResponse {
  status: string;
  file_name: string;
  chunks_added: number;
  total_documents: number;
  message?: string;
}

export interface ChatbotStats {
  total_documents: number;
  embedding_dim: number;
  chat_history_length: number;
  model_name?: string;
}

export interface LanguageInfo {
  language_code: string;
  language_name: string;
  confidence: number;
}

export interface Language {
  code: string;
  name: string;
}

export interface Settings {
  embedding_model: string;
  llm_model: string;
  device: string;
  supported_languages: string[];
}

export interface IndexStats {
  total_documents: number;
  embedding_dim: number;
  index_size: number;
  model_name: string;
}
