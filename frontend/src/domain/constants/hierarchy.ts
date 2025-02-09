/**
 * Constants defining the legal document hierarchy
 */

export const HIERARCHY_LEVELS = {
  BOOK: 'book',
  PART: 'part',
  CHAPTER: 'chapter',
  ARTICLE: 'article',
  PROVISION: 'provision',
} as const;

export const DOCUMENT_TYPES = {
  LAW: 'law',
  REGULATION: 'regulation',
  DECREE: 'decree',
  CIRCULAR: 'circular',
} as const;

export const LEGAL_CATEGORIES = {
  CRIMINAL: 'criminal',
  CIVIL: 'civil',
  ADMINISTRATIVE: 'administrative',
  COMMERCIAL: 'commercial',
  CONSTITUTIONAL: 'constitutional',
} as const;

export const METADATA_FIELDS = {
  HIERARCHY_LEVEL: 'hierarchyLevel',
  TCK_REFERENCES: 'tckReferences',
  LEGAL_TERMS: 'legalTerms',
  TOPICS: 'topics',
} as const; 