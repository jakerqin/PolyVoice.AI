import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ApiService } from '../../services/api';
import { ReactComponent as VoiceLogoSVG } from '../../assets/aiVoice.svg';
import {
  ChatContainer,
  ChatContent,
  ChatLogo,
  Logo,
  LogoText,
  MessageBubble,
  UserMessage,
  CoachMessage,
  ChatSidebar,
  AudioPlayer,
  ChatMainArea,
  ChatMessagesContainer,
  InputBar,
  InputField,
  SendButton
} from './style';
import styled from 'styled-components';
import ReactMarkdown from 'react-markdown';

// 错误提示样式
const ErrorContainer = styled.div`
  background-color: rgba(220, 38, 38, 0.2);
  border: 1px solid rgba(248, 113, 113, 0.5);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  color: #fecaca;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const ErrorMessage = styled.p`
  margin: 0 0 10px 0;
  font-size: 14px;
  text-align: center;
`;

const RetryButton = styled.button`
  background-color: #dc2626;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  
  &:hover {
    background-color: #b91c1c;
  }
`;

// 右侧边栏样式
const SidebarTitle = styled.h2`
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 16px 0;
  color: #333;
`;

const HistoryItem = styled.div`
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  background-color: white;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  
  &:hover {
    background-color: #f0f0f0;
  }
  
  h3 {
    font-size: 14px;
    margin: 0 0 4px 0;
    color: #333;
  }
  
  p {
    font-size: 12px;
    margin: 0;
    color: #666;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
`;

const InfoBox = styled.div`
  margin-top: 24px;
  padding: 16px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  
  h3 {
    font-size: 14px;
    margin: 0 0 8px 0;
    color: #333;
  }
  
  p {
    font-size: 12px;
    margin: 0 0 8px 0;
    color: #666;
    line-height: 1.5;
  }
`;

// 发送图标组件
const SendIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
    <path d="M0 0h24v24H0z" fill="none" />
    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
  </svg>
);

interface ChatViewProps {
  userText: string;
  coachText: string;
  audioUrl: string;
  errorMessage?: string;
}

export const ChatView: React.FC<ChatViewProps> = ({ userText, coachText, audioUrl, errorMessage }) => {
  const [isTyping, setIsTyping] = useState<boolean>(false);
  const [displayedText, setDisplayedText] = useState<string>("");
  const [typingSpeed] = useState<number>(30); // 打字速度（毫秒/字符）

  // 每当coachText变化时重新开始打字
  useEffect(() => {
    if (coachText && coachText !== displayedText) {
      setIsTyping(true);

      // 如果displayedText是coachText的开头部分，就从当前位置继续
      if (coachText.startsWith(displayedText)) {
        // 不需要重置displayedText
      } else {
        // 重置显示文本
        setDisplayedText("");
      }
    }
  }, [coachText, displayedText]);

  // 实现打字机效果
  useEffect(() => {
    if (isTyping && coachText) {
      if (displayedText.length < coachText.length) {
        const timeout = setTimeout(() => {
          setDisplayedText(coachText.substring(0, displayedText.length + 1));
        }, typingSpeed);
        return () => clearTimeout(timeout);
      } else {
        setIsTyping(false);
      }
    }
  }, [isTyping, coachText, displayedText, typingSpeed]);

  useEffect(() => {
    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  return (
    <>
      {/* 显示错误信息 */}
      {errorMessage && (
        <ErrorContainer>
          <ErrorMessage>{errorMessage}</ErrorMessage>
        </ErrorContainer>
      )}
      
      {userText && (
        <UserMessage>
          <MessageBubble>{userText}</MessageBubble>
        </UserMessage>
      )}
      
      {coachText && (
        <CoachMessage>
          <MessageBubble>
            <ReactMarkdown>{displayedText}</ReactMarkdown>
            {isTyping && <span className="typing-cursor"></span>}
          </MessageBubble>
          
          {audioUrl && (
            <AudioPlayer>
              <audio controls src={audioUrl}></audio>
            </AudioPlayer>
          )}
        </CoachMessage>
      )}
      
      {/* 当没有任何内容时显示默认欢迎消息 */}
      {!userText && !coachText && !errorMessage && (
        <CoachMessage>
          <MessageBubble>
            欢迎使用聊天功能，请开始对话...
          </MessageBubble>
        </CoachMessage>
      )}
    </>
  );
};

// 输入栏组件
const InputBarComponent = ({ onSendMessage }: { onSendMessage: (message: string) => void }) => {
  const [message, setMessage] = useState<string>("");
  
  const handleSend = () => {
    if (message.trim()) {
      onSendMessage(message);
      setMessage("");
    }
  };
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };
  
  return (
    <InputBar>
      <InputField
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="输入消息..."
      />
      <SendButton onClick={handleSend}>
        <SendIcon />
      </SendButton>
    </InputBar>
  );
};

// 添加类型定义，这样TypeScript能识别EventSource
interface MyEventSource {
  close: () => void;
}

// 主聊天页面组件
const ChatPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // 获取从HomePage传递的状态
  const audioBlob = location.state?.audioBlob;
  const initialAudioUrl = location.state?.audioUrl;
  
  // 聊天状态
  const [userText, setUserText] = useState<string>("");
  const [coachText, setCoachText] = useState<string>("");
  const [audioUrl, setAudioUrl] = useState<string | null>(initialAudioUrl || null);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [audioQueue, setAudioQueue] = useState<string[]>([]);
  const [isPlaying, setIsPlaying] = useState(false);
  
  // 模拟历史对话数据
  const chatHistory = [
    { id: 1, date: '2023-10-15', title: '英语口语练习', preview: '你好，今天我们来练习日常对话...' },
    { id: 2, date: '2023-10-12', title: '商务会议对话', preview: '请介绍一下你的项目计划...' },
    { id: 3, date: '2023-10-10', title: '旅游场景对话', preview: '我想预订一间酒店房间...' },
  ];
  
  // 处理用户直接访问聊天页面的情况
  useEffect(() => {
    if (!audioBlob && !location.state) {
      // 不再重定向，只显示一个欢迎消息
      setIsProcessing(false);
    } else if (audioBlob) {
      // 如果有音频数据，处理录音
      processRecording(audioBlob);
    } else {
      setIsProcessing(false);
    }
  }, []);
  
  // 处理录音数据
  const processRecording = async (audioBlob: Blob) => {
    setIsProcessing(true);
    setErrorMessage(""); // 清除之前的错误
    
    let eventSource: MyEventSource | null = null;
    
    try {
      let accumulatedText = "";
      
      // 添加超时处理
      const timeoutPromise = new Promise<never>((_, reject) => {
        setTimeout(() => reject(new Error("请求超时，请检查网络连接")), 30000); // 30秒超时
      });
      
      // 使用EventSource流式处理响应
      let eventSourcePromise = ApiService.streamAudioChatEvents(
        audioBlob,
        
        // 文本回调 (教练回答)
        (text: string) => {
          accumulatedText += text;
          setCoachText(accumulatedText);
        },
        
        // 音频回调
        (audioData: string, format: string) => {
          try {
            const byteCharacters = atob(audioData);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {
              byteNumbers[i] = byteCharacters.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);
            const blob = new Blob([byteArray], { type: `audio/${format}` });
            const url = URL.createObjectURL(blob);

            setAudioQueue(prev => [...prev, url]);
          } catch (e) {
            console.error("处理音频数据出错:", e);
          }
        },
        
        // 错误回调
        (error: string) => {
          console.error("处理录音出错:", error);
          setErrorMessage(`处理录音时出错: ${error}，请重试或联系客服`);
          setIsProcessing(false);
        },
        
        // 识别文本回调 (用户输入)
        (text: string) => {
          setUserText(text);
        },
        
        // 完成回调
        () => {
          setIsProcessing(false);
        }
      );
      
      // 使用Promise.race处理超时，并明确类型
      eventSource = await Promise.race([eventSourcePromise, timeoutPromise]) as MyEventSource;
      
      // 组件卸载时关闭事件源
      return () => {
        if (eventSource) {
          eventSource.close();
        }
      };
    } catch (error: any) {
      console.error("处理录音失败:", error);
      setErrorMessage(`处理录音失败: ${error?.message || "未知错误"}，请重试`);
      setIsProcessing(false);
      return () => {}; // 返回空函数以满足useEffect要求
    }
  };
  
  // 重试处理录音
  const handleRetry = () => {
    if (audioBlob) {
      processRecording(audioBlob);
    }
  };
  
  // 处理发送消息
  const handleSendMessage = (message: string) => {
    // 保存用户消息
    setUserText(message);
    // 这里可以实现文本消息的处理逻辑
    console.log("发送消息:", message);
    
    // 模拟API调用
    setIsProcessing(true);
    
    // 模拟API调用延迟
    setTimeout(() => {
      try {
        // 模拟API回复
        setCoachText("这是模拟的回复消息。实际项目中，这里应该调用后端API获取回复。");
        setIsProcessing(false);
      } catch (error: any) {
        console.error("消息处理失败:", error);
        setErrorMessage(`消息处理失败: ${error?.message || "未知错误"}`);
        setIsProcessing(false);
      }
    }, 1500);
  };
  
  useEffect(() => {
    if (!isPlaying && audioQueue.length > 0) {
      const url = audioQueue[0];
      const audioObj = new Audio(url);
      setIsPlaying(true);
      setAudioUrl(url);

      audioObj.play();
      audioObj.onended = () => {
        setIsPlaying(false);
        setAudioQueue(prev => prev.slice(1));
        URL.revokeObjectURL(url);
      };
      audioObj.onerror = () => {
        setIsPlaying(false);
        setAudioQueue(prev => prev.slice(1));
        URL.revokeObjectURL(url);
      };
    }
  }, [audioQueue, isPlaying]);
  
  return (
    <ChatContainer>
      <ChatContent>
        <ChatMainArea>
          <ChatLogo>
            <Logo>
              <VoiceLogoSVG />
            </Logo>
            <LogoText>PolyVoice.AI</LogoText>
          </ChatLogo>
          
          <ChatMessagesContainer>
            {isProcessing && (
              <div style={{ 
                textAlign: 'center', 
                padding: '10px', 
                color: 'rgba(255, 255, 255, 0.8)'
              }}>
                正在处理，请稍候...
              </div>
            )}
            
            <ChatView 
              userText={userText}
              coachText={coachText}
              audioUrl={audioUrl || ""}
              errorMessage={errorMessage}
            />
            
            {errorMessage && (
              <div style={{ 
                textAlign: 'center', 
                margin: '10px 0'
              }}>
                <RetryButton onClick={handleRetry}>
                  重试
                </RetryButton>
              </div>
            )}
          </ChatMessagesContainer>
          
          <InputBarComponent onSendMessage={handleSendMessage} />
        </ChatMainArea>
        <ChatSidebar>
          <SidebarTitle>对话历史</SidebarTitle>
          
          {chatHistory.map(chat => (
            <HistoryItem key={chat.id}>
              <h3>{chat.title}</h3>
              <p>{chat.date}</p>
              <p>{chat.preview}</p>
            </HistoryItem>
          ))}
          
          <InfoBox>
            <h3>PolyVoice.AI 语音助手</h3>
            <p>
              我们的AI语音教练可以帮助您提高口语能力，纠正发音，提供实时反馈。
              通过日常练习，您将快速提升语言技能。
            </p>
            <p>
              提示：点击左侧麦克风图标开始录音，或直接在输入框中键入文字进行对话。
            </p>
          </InfoBox>
        </ChatSidebar>
      </ChatContent>
    </ChatContainer>
  );
};

export default ChatPage; 