export interface SearchResult {
  id: string;
  content: string;
  metadata: Record<string, any>;
  distance?: number;
}

export interface QuestionRequest {
  question: string;
  metadata_filter?: Record<string, string>;
  n_results?: number;
}

export interface QuestionResponse {
  answer: string;
  confidence_score?: number;
  sources: SearchResult[];
  processing_time: number;
} 