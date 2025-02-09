/**
 * Domain models for legal terminology
 */

export interface LegalTerm {
  id: string;
  term: string;
  definition: string;
  references: string[];
  relatedTerms: string[];
  metadata: TermMetadata;
}

export interface TermMetadata {
  category: string;
  source: string;
  lastUpdated: string;
  usage: string[];
}

export interface TermSearchResult {
  term: LegalTerm;
  relevance: number;
} 