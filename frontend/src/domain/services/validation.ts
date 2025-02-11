/**
 * Validation services for domain entities
 */

import { LegalArticle, ArticleMetadata } from '@domain/models/legal';
import { LegalTerm } from '@domain/models/terminology';

export function isValidArticle(article: LegalArticle): boolean {
  return (
    article.id !== undefined &&
    article.articleNumber > 0 &&
    article.content.trim() !== '' &&
    article.book.trim() !== '' &&
    article.part.trim() !== '' &&
    article.chapter.trim() !== '' &&
    isValidArticleMetadata(article.metadata)
  );
}

export function isValidArticleMetadata(metadata: ArticleMetadata): boolean {
  return (
    metadata.hierarchyLevel !== undefined &&
    Array.isArray(metadata.tckReferences) &&
    Array.isArray(metadata.legalTerms) &&
    Array.isArray(metadata.topics)
  );
}

export function isValidTerm(term: LegalTerm): boolean {
  return (
    term.id !== undefined &&
    term.term.trim() !== '' &&
    term.definition.trim() !== '' &&
    Array.isArray(term.references) &&
    Array.isArray(term.relatedTerms) &&
    term.metadata !== undefined
  );
}

export function validateQuestion(question: string): string | null {
  if (!question.trim()) {
    return 'Question cannot be empty';
  }
  if (question.length < 10) {
    return 'Question is too short';
  }
  if (question.length > 500) {
    return 'Question is too long';
  }
  return null;
} 