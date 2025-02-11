import { api, ApiException } from '../config/axios';
import { QuestionRequest, QuestionResponse } from '../../types/api';

export class QAService {
  static async askQuestion(request: QuestionRequest): Promise<QuestionResponse> {
    try {
      const response = await api.post<QuestionResponse>('/qa/ask', request);
      return response.data;
    } catch (error: any) {
      throw new ApiException({
        message: error.response?.data?.message || 'Failed to process question',
        status: error.response?.status || 500,
        data: error.response?.data
      });
    }
  }
} 