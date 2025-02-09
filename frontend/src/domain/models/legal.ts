/**
 * Domain models for legal entities
 */

export interface LegalArticle {
  id: string;
  articleNumber: number;
  content: string;
  book: string;
  part: string;
  chapter: string;
  metadata: ArticleMetadata;
}

export interface ArticleMetadata {
  hierarchyLevel: string;
  tckReferences: number[];
  legalTerms: string[];
  topics: string[];
}

export interface SearchResult {
  id: string;
  content: string;
  metadata: ArticleMetadata;
  distance?: number;
}

export interface QuestionRequest {
  question: string;
  metadataFilter?: Record<string, string>;
  numResults?: number;
}

export interface QuestionResponse {
  answer: string;
  confidenceScore: number;
  sources: SearchResult[];
  processingTime: number;
} 