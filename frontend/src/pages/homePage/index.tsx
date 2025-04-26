import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../../components/headers";
import AppFooter from "../../components/footer";
import {
  Main,
  MicrophoneButton,
  RecordingControlsContainer,
  RecordingWaveContainer,
  RecordingWaveLine,
  RecordingTime,
  RecordingStatus,
  RecordingActionButton,
  LoadingIndicator,
  LoadingDot
} from "./style";

// SVG图标组件
const MicrophoneIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 15c2.21 0 4-1.79 4-4V5c0-2.21-1.79-4-4-4S8 2.79 8 5v6c0 2.21 1.79 4 4 4zm0-2c-1.1 0-2-.9-2-2V5c0-1.1.9-2 2-2s2 .9 2 2v6c0 1.1-.9 2-2 2z" />
    <path d="M19 10h-1c0 3.31-2.69 6-6 6s-6-2.69-6-6H5c0 3.82 2.78 7.01 6.44 7.62v2.38h-3v2h7v-2h-3v-2.38c3.66-.61 6.44-3.8 6.44-7.62h-1.06.06z" />
  </svg>
);

const CloseIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
    <path d="M0 0h24v24H0z" fill="none" />
    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
  </svg>
);

const CheckIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
    <path d="M0 0h24v24H0z" fill="none" />
    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
  </svg>
);

const PageMain = () => {
  // 用于导航的hook
  const navigate = useNavigate();
  
  // 状态
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [recordingTime, setRecordingTime] = useState<number>(0);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  
  // 录音相关的引用
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<number | null>(null);
  
  // 用于波形动画的数组
  const waveLines = Array.from({ length: 30 }, (_, i) => ({
    id: i,
    delay: i * 30,
  }));

  // 格式化录音时间
  const formatTime = (timeInSeconds: number): string => {
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = timeInSeconds % 60;
    return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
  };

  // 开始录音
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.start();
      setIsRecording(true);
      
      let seconds = 0;
      timerRef.current = window.setInterval(() => {
        seconds += 1;
        setRecordingTime(seconds);
      }, 1000);
      
    } catch (error) {
      console.error("无法访问麦克风:", error);
      alert("无法访问麦克风，请确保已授权或检查您的设备。");
    }
  };

  // 停止录音并处理
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
      
      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        navigateToChatPage(audioBlob);
      };
      
      if (mediaRecorderRef.current.stream) {
        mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      }
    }
  };

  // 取消录音
  const cancelRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
      
      audioChunksRef.current = [];
      setRecordingTime(0);
      
      if (mediaRecorderRef.current.stream) {
        mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      }
    }
  };

  // 导航到聊天页面，传递音频Blob
  const navigateToChatPage = (audioBlob: Blob) => {
    setIsProcessing(true);
    const audioUrl = URL.createObjectURL(audioBlob);
    
    navigate('/chat', {
      state: {
        audioBlob: audioBlob,
        audioUrl: audioUrl
      }
    });
  };

  // 组件卸载时清理资源
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
        mediaRecorderRef.current.stop();
        if (mediaRecorderRef.current.stream) {
          mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
        }
      }
    };
  }, []);

  return (
    <Main>
      {!isRecording ? (
        <>
          <MicrophoneButton 
            isRecording={false} 
            onClick={startRecording}
            aria-label="开始录音"
          >
            <MicrophoneIcon />
          </MicrophoneButton>
          <RecordingStatus>开始对话</RecordingStatus>
        </>
      ) : (
        <>
          <RecordingTime>{formatTime(recordingTime)}</RecordingTime>
          <RecordingStatus>正在录音...</RecordingStatus>
          
          <RecordingWaveContainer>
            {waveLines.map((line) => (
              <RecordingWaveLine key={line.id} delay={line.delay} />
            ))}
          </RecordingWaveContainer>
          
          <RecordingControlsContainer>
            <RecordingActionButton 
              onClick={cancelRecording}
              aria-label="取消录音"
            >
              <CloseIcon />
            </RecordingActionButton>
            
            <RecordingActionButton 
              onClick={stopRecording}
              aria-label="停止录音"
              style={{ backgroundColor: "#ff4b4b" }}
            >
              <CheckIcon />
            </RecordingActionButton>
          </RecordingControlsContainer>
        </>
      )}

      {isProcessing && (
        <LoadingIndicator>
          处理中
          <LoadingDot delay={0}>.</LoadingDot>
          <LoadingDot delay={0.2}>.</LoadingDot>
          <LoadingDot delay={0.4}>.</LoadingDot>
        </LoadingIndicator>
      )}
    </Main>
  );
};

function HomePage() {
  return (
    <div className="App">
      <Header />
      <PageMain/>
      <AppFooter />
    </div>
  );
}

export default HomePage;
