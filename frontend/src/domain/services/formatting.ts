/**
 * Formatting services for domain entities
 */

import { LegalArticle, SearchResult } from '../models/legal';
import { LegalTerm } from '../models/terminology';

export function formatArticleReference(article: LegalArticle): string {
  return `Article ${article.articleNumber} - ${article.book}, ${article.part}, ${article.chapter}`;
}

export function formatSearchResult(result: SearchResult): string {
  const metadata = result.metadata;
  return `${result.content}\n\nSource: ${metadata.hierarchyLevel}\nTopics: ${metadata.topics.join(', ')}`;
}

export function formatLegalTerm(term: LegalTerm): string {
  return `${term.term}: ${term.definition}\n\nRelated Terms: ${term.relatedTerms.join(', ')}`;
}

export function formatConfidenceScore(score: number): string {
  return `${(score * 100).toFixed(1)}%`;
}

export function formatProcessingTime(time: number): string {
  return `${time.toFixed(2)} seconds`;
} 