import axios from "axios";

// API基础URL
const API_BASE_URL = "http://localhost:8000";

// 响应类型定义
export interface GenerateVoiceResponse {
  success: boolean;
  audioUrl: string;
  message: string;
}

// 请求类型定义
export interface GenerateVoiceRequest {
  text: string;
  model: string;
}

// API服务类
export class ApiService {
  // 生成语音API
  static async generateVoice(
    data: GenerateVoiceRequest
  ): Promise<GenerateVoiceResponse> {
    try {
      const response = await axios.post<GenerateVoiceResponse>(
        `${API_BASE_URL}/api/generate-voice`,
        data
      );
      return response.data;
    } catch (error) {
      console.error("API调用失败:", error);
      throw error;
    }
  }
}
