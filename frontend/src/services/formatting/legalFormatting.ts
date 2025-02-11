import { LegalArticle, SearchResult } from '../../types/legal';
import { LegalTerm } from '../../types/terminology';

export class LegalFormattingService {
  static formatArticleReference(article: LegalArticle): string {
    return `Article ${article.articleNumber} - ${article.book}, ${article.part}, ${article.chapter}`;
  }

  static formatSearchResult(result: SearchResult): string {
    const metadata = result.metadata;
    return `${result.content}\n\nSource: ${metadata.hierarchyLevel}\nTopics: ${metadata.topics.join(', ')}`;
  }

  static formatLegalTerm(term: LegalTerm): string {
    return `${term.term}: ${term.definition}\n\nRelated Terms: ${term.relatedTerms.join(', ')}`;
  }

  static formatConfidenceScore(score: number): string {
    return `${(score * 100).toFixed(1)}%`;
  }

  static formatProcessingTime(time: number): string {
    return `${time.toFixed(2)} seconds`;
  }
} 