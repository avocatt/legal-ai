// Create new file to centralize API types
export interface SearchResult {
  id: string;
  content: string;
  metadata: {
    type: string;
    number?: string;
    book?: string;
    part?: string;
    chapter?: string;
    hierarchyLevel?: string;
    topics?: string[];
    [key: string]: any;
  };
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