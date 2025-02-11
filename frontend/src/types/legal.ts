export interface LegalArticle {
  articleNumber: string;
  book: string;
  part: string;
  chapter: string;
  content: string;
}

export interface SearchResult {
  content: string;
  metadata: {
    hierarchyLevel: string;
    topics: string[];
  };
  confidence: number;
} 