import axios from "axios"


// API基础URL
const API_BASE_URL = "http://localhost:8000";

// 聊天响应接口
export interface ChatResponse {
  type: string;  // "text", "audio", "error", "recognized_text"
  text: string;  // 文本内容
  audio: string; // 音频内容（base64）
  format?: string; // 音频格式
}

// API服务类
export class ApiService {
  // 使用EventSource进行流式通信
  static async streamAudioChatEvents(
    audioBlob: Blob, 
    onTextReceived: (text: string) => void,
    onAudioReceived: (audioData: string, format: string) => void,
    onError: (error: string) => void,
    onRecognizedText: (text: string) => void,
    onComplete: () => void
  ): Promise<EventSource> {
    try {
      // 先上传音频文件
      const formData = new FormData();
      formData.append("audio", audioBlob);
      const response = await axios.post(`${API_BASE_URL}/api/stream_audio_chat`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      
      // 获取会话ID
      const sessionId = response.data.session_id;
      
      // 然后创建EventSource连接
      const eventSource = new EventSource(`${API_BASE_URL}/api/stream_audio_chat/${sessionId}`);

      // 处理事件
      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data) as ChatResponse;
          
          if (data.type === "text") {
            onTextReceived(data.text);
          } else if (data.type === "audio") {
            onAudioReceived(data.audio, data.format || "mp3");
          } else if (data.type === "error") {
            onError(data.text);
            eventSource.close();
          } else if (data.type === "recognized_text") {
            onRecognizedText(data.text);
          } else if (data.type === "end") {
            onComplete();
            eventSource.close();
          }
        } catch (error) {
          console.error("解析事件数据失败:", error);
          onError("解析响应失败");
        }
      };

      eventSource.onerror = (error) => {
        console.error("EventSource错误:", error);
        onError("连接错误");
        eventSource.close();
      };

      return eventSource;
    } catch (error) {
      console.error("上传音频或建立连接失败:", error);
      onError("上传音频或建立连接失败");
      throw error;
    }
  }
}
