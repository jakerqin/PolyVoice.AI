import React, { useState } from "react";
// 导入API服务
import { ApiService } from "../../services/api";
import {
  Main,
  InputContainer,
  TextArea,
  Controls,
  ModelSelector,
  GenerateButton,
  ResultContainer,
  ResultTitle,
  AudioPlayer,
  DownloadButton,
} from "./style";

const AppMain = () => {
  const [text, setText] = useState<string>("");
  const [model, setModel] = useState<string>("模型1");
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [audioUrl, setAudioUrl] = useState<string>("");
  const [showResult, setShowResult] = useState<boolean>(false);

  const handleGenerate = async (): Promise<void> => {
    if (!text.trim()) {
      alert("请输入要转换的文本");
      return;
    }

    setIsGenerating(true);

    try {
      // 使用API服务调用后端
      const response = await ApiService.generateVoice({ text, model });

      if (response.success) {
        setAudioUrl(response.audioUrl);
        setShowResult(true);
      } else {
        alert("生成失败: " + response.message);
      }
    } catch (error) {
      console.error("生成语音失败:", error);
      alert("生成语音失败，请重试");
    } finally {
      setIsGenerating(false);
    }
  };
  return (
    <Main>
      <InputContainer>
        <TextArea
          placeholder="请输入场景开始跟教练一起练习口语吧！"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <Controls>
          <ModelSelector
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="模型1">模型1</option>
            <option value="模型2">模型2</option>
            <option value="模型3">模型3</option>
          </ModelSelector>

          <GenerateButton onClick={handleGenerate} disabled={isGenerating}>
            <span>{"练习"}</span>
          </GenerateButton>
        </Controls>
      </InputContainer>

      {showResult && (
        <ResultContainer>
          <ResultTitle>生成结果</ResultTitle>
          <AudioPlayer>
            <audio controls src={audioUrl}></audio>
          </AudioPlayer>
        </ResultContainer>
      )}
    </Main>
  );
};
export default AppMain;
