export interface SearchResult {
  id: string;
  content: string;
  metadata: Record<string, any>;
  distance?: number;
}

export interface QuestionRequest {
  text: string;
  metadata_filter?: Record<string, string>;
  n_results?: number;
}

export interface QuestionResponse {
  answer: string;
  sources: SearchResult[];
  processing_time: number;
  confidence_score?: number;
}
