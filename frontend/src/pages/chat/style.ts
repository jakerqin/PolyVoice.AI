import styled, { keyframes } from "styled-components";

export const AudioPlayer = styled.div`
  margin-top: 8px;
  audio {
    width: 100%;
    height: 30px;
  }
`;

export const ChatLogo = styled.div`
  display: flex;
  align-items: center;
  padding: 10px 10px;
  color: white;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
`;

export const Logo = styled.div`
  width: 30px;
  height: 30px;
  margin-right: 10px;
  
  svg {
    width: 100%;
    height: 100%;
  }
`;

export const LogoText = styled.h1`
  font-size: 18px;
  font-weight: 500;
  margin: 0;
  letter-spacing: 0.5px;
  color: #1fe05d;
`;

export const ChatHeader = styled.div`
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  background-color: #1a1a2e;
  color: white;
  justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
`;

export const ChatTitle = styled.h1`
  font-size: 18px;
  font-weight: 500;
  margin: 0;
`;

export const BackButton = styled.button`
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 14px;
  
  svg {
    margin-right: 5px;
    width: 20px;
    height: 20px;
  }
  
  &:hover {
    color: #93c5fd;
  }
`;

export const ChatContainer = styled.div`
  display: flex;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  background-color: #f9f9f9;
  flex-direction: column;
`;

export const ChatContent = styled.div`
  flex: 1;
  display: flex;
  width: 100%;
  overflow: hidden;
`;

export const ChatMainArea = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
  background-color: #2a2a42;
  color: white;
`;

export const ChatMessagesContainer = styled.div`
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

export const ChatSidebar = styled.div`
  flex: 1;
  padding: 20px;
  background-color: #f0f2f5;
  overflow-y: auto;
`;

export const InputBar = styled.div`
  display: flex;
  align-items: center;
  background-color: #3a3a52;
  border-radius: 24px;
  padding: 8px 16px;
  margin: 10px 20px 20px 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
`;

export const InputField = styled.textarea`
  flex: 1;
  border: none;
  background: transparent;
  padding: 8px 0;
  resize: none;
  font-family: inherit;
  font-size: 14px;
  outline: none;
  max-height: 120px;
  min-height: 24px;
  color: white;
  
  &::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }
`;

export const SendButton = styled.button`
  background: none;
  border: none;
  color: #60a5fa;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  
  svg {
    width: 24px;
    height: 24px;
  }
  
  &:hover {
    color: #93c5fd;
  }
  
  &:disabled {
    color: #6b7280;
    cursor: not-allowed;
  }
`;

export const MessageBubble = styled.div`
  padding: 12px 16px;
  border-radius: 18px;
  max-width: 70%;
  word-wrap: break-word;
  position: relative;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  line-height: 1.5;
`;

export const UserMessage = styled.div`
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
  
  ${MessageBubble} {
    background-color: #4f46e5;
    color: white;
    border-bottom-right-radius: 4px;
  }
`;

const blink = keyframes`
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
`;

export const CoachMessage = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 16px;
  
  ${MessageBubble} {
    background-color: #3a3a52;
    color: white;
    border-bottom-left-radius: 4px;
  }
  
  .typing-cursor {
    display: inline-block;
    width: 2px;
    height: 16px;
    background-color: white;
    margin-left: 2px;
    animation: ${blink} 0.7s infinite;
  }
`; 

// 错误提示样式
export const ErrorContainer = styled.div`
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

export const ErrorMessage = styled.p`
  margin: 0 0 10px 0;
  font-size: 14px;
  text-align: center;
`;

export const RetryButton = styled.button`
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
export const SidebarTitle = styled.h2`
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 16px 0;
  color: #333;
`;

export const HistoryItem = styled.div`
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

export const InfoBox = styled.div`
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

// 添加诊断和建议的样式组件
export const DiagnosisContainer = styled.div`
  background-color: rgba(30, 224, 93, 0.1);
  border: 1px solid rgba(30, 224, 93, 0.3);
  border-radius: 12px;
  padding: 12px 16px;
  margin-top: 10px;
  max-width: 90%;
`;

export const DiagnosisTitle = styled.h3`
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #1fe05d;
`;

export const DiagnosisContent = styled.div`
  font-size: 14px;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.9);
`;

export const SuggestionItem = styled.div`
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: background-color 0.2s;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:hover {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    padding-left: 8px;
  }
`;

// 高级诊断区域样式
export const AdvancedDiagnosisButton = styled.button`
  background-color: rgba(30, 224, 93, 0.2);
  color: #1fe05d;
  border: 1px solid rgba(30, 224, 93, 0.4);
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    background-color: rgba(30, 224, 93, 0.3);
  }
`;

export const DiagnosisHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
`;

export const DiagnosisBackButton = styled.button`
  background: none;
  border: none;
  color: #333;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 14px;
  padding: 0;
  margin-right: 10px;
  
  svg {
    margin-right: 5px;
    width: 16px;
    height: 16px;
  }
  
  &:hover {
    color: #4f46e5;
  }
`;

export const SidebarHeader = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 16px;
`;

export const KeywordContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
`;

export const KeywordTag = styled.div`
  background-color: #e5e7eb;
  color: #4b5563;
  border-radius: 16px;
  padding: 4px 12px;
  font-size: 12px;
`;

export const SearchResultsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
`;

export const SearchResultItem = styled.div`
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  }
`;

export const VideoThumbnail = styled.img`
  width: 100%;
  height: 120px;
  object-fit: cover;
`;

export const SearchResultTitle = styled.h3`
  font-size: 14px;
  margin: 0;
  padding: 10px;
  color: #333;
`;

export const SearchLoading = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  color: #6b7280;
  font-size: 14px;
`;

export const LogsContainer = styled.div`
  background-color: #1e293b;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
  max-height: 200px;
  overflow-y: auto;
  font-family: monospace;
  font-size: 12px;
  color: #94a3b8;
  line-height: 1.5;
`;

export const LogEntry = styled.div`
  margin-bottom: 4px;
  
  &:last-child {
    margin-bottom: 0;
  }
`;