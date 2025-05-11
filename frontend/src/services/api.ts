import axios from "axios"


// API基础URL
const API_BASE_URL = "http://localhost:8000";

// 聊天响应接口
export interface ChatResponse {
  type: string;  // "response", "pronunciationSuggestion", "grammarSuggestion", "userResponseSuggestion", "audio", "text", "error", "recognized_text", "end"
  data: string | string[];  // 响应内容，可能是文本或者用户响应建议数组
  text?: string;  // 兼容旧版API
  audio?: string; // 音频内容（base64）
  format?: string; // 音频格式
}

// 高级诊断类型
export type DiagnosisType = "pronunciation" | "grammar" | "userResponse";

// 高级诊断事件类型
export type DiagnosisEvent = {
  status?: string;
  type?: string;
  message?: string;
  data?: any;
  results?: Array<{
    title: string;
    url: string;
    snippet: string;
  }>;
  title?: string;
  url?: string;
  content?: string;
};

// API服务类
export class ApiService {
  // 使用EventSource进行流式通信
  static async streamAudioChatEvents(
    audioBlob: Blob, 
    onTextReceived: (text: string) => void,
    onAudioReceived: (audioData: string, format: string) => void,
    onError: (error: string) => void,
    onRecognizedText: (text: string) => void,
    onComplete: () => void,
    onPronunciationSuggestion?: (text: string) => void,
    onGrammarSuggestion?: (text: string) => void,
    onUserResponseSuggestion?: (text: string) => void
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
          
          switch (data.type) {
            case "response":
              // 处理响应文本，与旧版的text处理相同
              onTextReceived(data.data as string);
              break;
            case "audio":
              onAudioReceived(data.audio || data.data as string, data.format || "mp3");
              break;
            case "error":
              onError(data.text || data.data as string);
              eventSource.close();
              break;
            case "recognized_text":
              onRecognizedText(data.text || data.data as string);
              break;
            case "pronunciationSuggestion":
              if (onPronunciationSuggestion && data.data) {
                onPronunciationSuggestion(data.data as string);
              }
              break;
            case "grammarSuggestion":
              if (onGrammarSuggestion && data.data) {
                onGrammarSuggestion(data.data as string);
              }
              break;
            case "userResponseSuggestion":
              if (onUserResponseSuggestion && data.data) {
                onUserResponseSuggestion(data.data as string);
              }
              break;
            case "end":
              onComplete();
              eventSource.close();
              break;
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

  /**
   * 请求高级诊断并流式返回结果
   * 
   * @param content 诊断内容
   * @param type 诊断类型
   * @param onLogEvent 日志事件回调
   * @param onExtractedEvent 内容提取事件回调
   * @param onSearchEvent 搜索结果事件回调
   * @param onContentEvent 内容结果事件回调
   * @param onErrorEvent 错误事件回调
   * @param onCompleteEvent 完成事件回调
   * @returns 事件源对象
   */
  static requestAdvancedDiagnosis(
    content: string,
    type: DiagnosisType,
    onLogEvent: (message: string) => void,
    onExtractedEvent: (data: any) => void,
    onSearchEvent: (results: any[]) => void,
    onContentEvent: (content: any) => void,
    onErrorEvent: (error: string) => void,
    onCompleteEvent: () => void
  ): void {
    // 首先发送内容到后端
    fetch(`${API_BASE_URL}/api/advanced_diagnosis/${type}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content }),
    })
      .then(async response => {
        if (!response.ok) throw new Error('请求失败');
        const data = await response.json();
        const sessionId = data.session_id;
        if (!sessionId) throw new Error('未获取到会话ID');
        // 然后创建EventSource连接
        const eventSource = new EventSource(`${API_BASE_URL}/api/advanced_diagnosis/${type}/${sessionId}`);
        // 处理事件
        eventSource.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data) as DiagnosisEvent;
            if (data.type === 'log' && data.data) {
              onLogEvent(data.data);
            } else if (data.status === 'extracted' && data.data) {
              onExtractedEvent(data.data);
            } else if (data.status === 'complete' && data.results) {
              onSearchEvent(data.results);
              eventSource.close();
            } else if (data.status === 'content') {
              onContentEvent({
                title: data.title || '',
                url: data.url || '',
                content: data.content || ''
              });
            } else if (data.status === 'error') {
              onErrorEvent(data.message || '未知错误');
              eventSource.close();
            }
          } catch (error) {
            console.error("解析事件数据失败:", error);
            onErrorEvent("解析响应失败");
          }
        };
        eventSource.onerror = (error) => {
          console.error("EventSource错误:", error);
          onErrorEvent("连接错误");
          eventSource.close();
        };
      })
      .catch(error => {
        onErrorEvent(`请求失败: ${error.message}`);
      });
  }
}
