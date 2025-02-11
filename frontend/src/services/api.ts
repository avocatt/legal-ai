import axios from "axios";
import type { QuestionRequest, QuestionResponse } from "@/types/api";

declare global {
  interface ImportMeta {
    env: {
      VITE_API_URL?: string;
    };
  }
}

const API_BASE_URL = import.meta.env.VITE_API_URL || "";

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000, // 30 seconds timeout
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log("Request:", config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error("Request Error:", error);
    return Promise.reject(error);
  },
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log("Response:", response.status, response.data);
    return response;
  },
  (error) => {
    console.error(
      "Response Error:",
      error.response?.status,
      error.response?.data || error.message,
    );
    return Promise.reject(error);
  },
);

export const askQuestion = async (
  request: QuestionRequest,
): Promise<QuestionResponse> => {
  const response = await api.post<QuestionResponse>("/qa/ask", request);
  return response.data;
};
