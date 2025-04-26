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