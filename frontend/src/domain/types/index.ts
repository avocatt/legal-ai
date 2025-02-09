/**
 * Re-exports of all domain types
 */

export * from '../models/legal';
export * from '../models/terminology';

export type HierarchyLevel = 'book' | 'part' | 'chapter' | 'article' | 'provision';
export type DocumentType = 'law' | 'regulation' | 'decree' | 'circular';
export type LegalCategory = 'criminal' | 'civil' | 'administrative' | 'commercial' | 'constitutional';

export type ValidationResult = {
  isValid: boolean;
  errors?: string[];
};

export type FormattingOptions = {
  includeMetadata?: boolean;
  includeReferences?: boolean;
  format?: 'short' | 'full';
}; 