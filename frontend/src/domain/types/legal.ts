// Update legal types for consistency
export interface LegalArticle {
  id: string;
  articleNumber: string;
  content: string;
  book: string;
  part: string;
  chapter: string;
  metadata: ArticleMetadata;
}

export interface ArticleMetadata {
  hierarchyLevel: string;
  tckReferences?: string[];
  legalTerms?: string[];
  topics: string[];
}

// Remove duplicate SearchResult interface since it's now in api.ts 