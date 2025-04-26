import styled, { keyframes } from "styled-components";

export const Main = styled.main`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
`;

export const InputContainer = styled.div`
  width: 100%;
  max-width: 800px;
  background-color: #1a1a1a;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #333333;
  margin-bottom: 2rem;
`;

export const TextArea = styled.textarea`
  width: 100%;
  min-height: 150px;
  padding: 1.5rem;
  background-color: transparent;
  border: none;
  color: #ffffff;
  font-size: 1rem;
  resize: none;
  outline: none;
  font-family: inherit;

  &::placeholder {
    color: #666;
  }
`;

export const Controls = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-top: 1px solid #333333;

  @media (max-width: 768px) {
    flex-direction: column;
    gap: 1rem;
  }
`;

export const ModelSelector = styled.select`
  background-color: transparent;
  color: #ffffff;
  border: 1px solid #1fe05d;
  padding: 0.5rem 2rem 0.5rem 1rem;
  border-radius: 4px;
  font-size: 1rem;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12' fill='none'%3E%3Cpath d='M2 4L6 8L10 4' stroke='%231FE05D' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  cursor: pointer;

  @media (max-width: 768px) {
    width: 100%;
  }
`;

export const GenerateButton = styled.button`
  background-color: #1fe05d;
  color: #111111;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.2s ease;

  &:hover {
    background-color: #19c04e;
  }

  &:disabled {
    background-color: #666;
    cursor: not-allowed;
  }

  span {
    margin-right: 0.5rem;
  }

  @media (max-width: 768px) {
    width: 100%;
    justify-content: center;
  }
`;

export const ResultContainer = styled.div`
  width: 100%;
  max-width: 800px;
  margin-top: 2rem;
`;

export const ResultTitle = styled.h2`
  margin-bottom: 1rem;
  color: #1fe05d;
`;

export const AudioPlayer = styled.div`
  margin: 1.5rem 0;

  audio {
    width: 100%;
  }
`;

export const DownloadButton = styled.button`
  background-color: #1fe05d;
  color: #111111;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  align-self: flex-end;

  &:hover {
    background-color: #19c04e;
  }
`;

// 新增录音界面相关样式

export const RecordingContainer = styled.div`
  width: 100%;
  max-width: 800px;
  background-color: #1a1a1a;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #333333;
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
`;

// 话筒按钮的呼吸动画
const breathe = keyframes`
  0% {
    box-shadow: 0 0 0 0 rgba(31, 224, 93, 0.7);
  }
  
  70% {
    box-shadow: 0 0 0 10px rgba(31, 224, 93, 0);
  }
  
  100% {
    box-shadow: 0 0 0 0 rgba(31, 224, 93, 0);
  }
`;

// 录音波形动画
const waveAnimation = keyframes`
  0% {
    height: 10px;
  }
  50% {
    height: 30px;
  }
  100% {
    height: 10px;
  }
`;

export const MicrophoneButton = styled.button<{ isRecording: boolean }>`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: ${(props) => (props.isRecording ? "#ff4b4b" : "#1fe05d")};
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  animation: ${(props) => (props.isRecording ? breathe : "none")} 1.5s infinite;
  margin: 0.2rem 0;

  &:hover {
    transform: scale(1.05);
  }

  svg {
    width: 30px;
    height: 30px;
    color: #111;
  }
`;

export const RecordingControlsContainer = styled.div`
  width: 100%;
  max-width: 300px;
  display: flex;
  justify-content: space-around;
  margin-top: 2rem;
`;

export const RecordingWaveContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  width: 100%;
  max-width: 300px;
  margin: 1.5rem 0;
`;

export const RecordingWaveLine = styled.div<{ delay: number }>`
  width: 3px;
  height: 10px;
  margin: 0 2px;
  background-color: #1fe05d;
  animation: ${waveAnimation} 1s infinite;
  animation-delay: ${(props) => props.delay}ms;
`;

export const RecordingTime = styled.div`
  margin-top: 2rem;
  font-size: 1.5rem;
  color: #ffffff;
`;

export const RecordingStatus = styled.div`
  margin-top: 0.5rem;
  font-size: 1.5rem;
  color: #1fe05d;
`;

export const RecordingActionButton = styled.button`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #ffffff;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;

  &:hover {
    transform: scale(1.05);
  }

  svg {
    width: 30px;
    height: 30px;
    color: #111;
  }
`;

export const ResponseContainer = styled.div`
  width: 100%;
  max-width: 600px;
  margin-top: 2rem;
  text-align: center;
`;

export const ResponseText = styled.div`
  color: #ffffff;
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 1rem;
  white-space: pre-wrap;
  text-align: left;
`;

export const LoadingIndicator = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 2rem 0;
  color: #1fe05d;
  font-size: 1rem;
`;

export const DotAnimation = keyframes`
  0%, 20% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
`;

export const LoadingDot = styled.span<{ delay: number }>`
  font-size: 2rem;
  margin: 0 0.2rem;
  animation: ${DotAnimation} 1.4s infinite;
  animation-delay: ${(props) => props.delay}s;
`;
