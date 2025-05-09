import React, { useState, useEffect, useRef } from 'react';
import { ApiService, DiagnosisType } from '../services/api';
import {
  DiagnosisContainer,
  DiagnosisHeader,
  DiagnosisTitle,
  AdvancedDiagnosisButton,
  SidebarHeader,
  DiagnosisBackButton,
  KeywordContainer,
  KeywordTag,
  SearchResultsContainer,
  SearchResultItem,
  VideoThumbnail,
  SearchResultTitle,
  SearchLoading,
  LogsContainer,
  LogEntry
} from '../pages/chat/style';

// 箭头图标组件
const ArrowIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M19 12H5M12 19l-7-7 7-7" />
  </svg>
);

interface AdvancedDiagnosisButtonProps {
  diagnosisType: DiagnosisType;
  diagnosisContent: string;
  onAdvancedDiagnosisClick: () => void;
}

// 高级诊断按钮组件
export const AdvancedDiagnosisButtonComponent: React.FC<AdvancedDiagnosisButtonProps> = ({ 
  diagnosisType,
  diagnosisContent,
  onAdvancedDiagnosisClick
}) => {
  return (
    <AdvancedDiagnosisButton onClick={onAdvancedDiagnosisClick}>
      高级诊断
    </AdvancedDiagnosisButton>
  );
};

interface AdvancedDiagnosisSidebarProps {
  diagnosisType: DiagnosisType;
  diagnosisContent: string;
  onBack: () => void;
}

// 高级诊断侧边栏组件
export const AdvancedDiagnosisSidebar: React.FC<AdvancedDiagnosisSidebarProps> = ({
  diagnosisType,
  diagnosisContent,
  onBack
}) => {
  const [logs, setLogs] = useState<string[]>([]);
  const [keywords, setKeywords] = useState<string[]>([]);
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [contentResults, setContentResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const eventSourceRef = useRef<EventSource | null>(null);
  const logsContainerRef = useRef<HTMLDivElement>(null);
  
  // 自动滚动日志到底部
  useEffect(() => {
    if (logsContainerRef.current) {
      logsContainerRef.current.scrollTop = logsContainerRef.current.scrollHeight;
    }
  }, [logs]);
  
  // 开始诊断
  useEffect(() => {
    if (!diagnosisContent) return;
    
    setIsSearching(true);
    setLogs([`开始进行${getDiagnosisTypeName(diagnosisType)}高级诊断...`]);
    setKeywords([]);
    setSearchResults([]);
    setContentResults([]);
    setError(null);
    
    // 设置回调函数
    const onLogEvent = (message: string) => {
      setLogs(prev => [...prev, message]);
    };
    
    const onExtractedEvent = (data: any) => {
      const extractedKeywords = data.search_keywords || [];
      setKeywords(Array.isArray(extractedKeywords) 
        ? extractedKeywords.flat().filter(Boolean) 
        : []);
    };
    
    const onSearchEvent = (results: any[]) => {
      setSearchResults(results || []);
    };
    
    const onContentEvent = (content: any) => {
      setContentResults(prev => [...prev, content]);
    };
    
    const onErrorEvent = (errorMsg: string) => {
      setError(errorMsg);
      setIsSearching(false);
    };
    
    const onCompleteEvent = () => {
      setIsSearching(false);
      setLogs(prev => [...prev, "诊断完成"]);
    };
    
    // 请求高级诊断
    try {
      eventSourceRef.current = ApiService.requestAdvancedDiagnosis(
        diagnosisContent,
        diagnosisType,
        onLogEvent,
        onExtractedEvent,
        onSearchEvent,
        onContentEvent,
        onErrorEvent,
        onCompleteEvent
      );
    } catch (error: any) {
      setError(`启动诊断失败: ${error.message}`);
      setIsSearching(false);
    }
    
    // 清理函数
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, [diagnosisContent, diagnosisType]);
  
  // 获取诊断类型名称
  const getDiagnosisTypeName = (type: DiagnosisType): string => {
    switch (type) {
      case 'pronunciation': return '发音';
      case 'grammar': return '语法';
      case 'userResponse': return '回答';
      default: return '语言';
    }
  };
  
  // 打开URL
  const handleOpenUrl = (url: string) => {
    window.open(url, '_blank');
  };
  
  return (
    <>
      <SidebarHeader>
        <DiagnosisBackButton onClick={onBack}>
          <ArrowIcon /> 返回
        </DiagnosisBackButton>
        <DiagnosisTitle>高级{getDiagnosisTypeName(diagnosisType)}诊断</DiagnosisTitle>
      </SidebarHeader>
      
      {/* 日志区域 */}
      <LogsContainer ref={logsContainerRef}>
        {logs.map((log, index) => (
          <LogEntry key={index}>{log}</LogEntry>
        ))}
        {isSearching && <LogEntry>正在处理...</LogEntry>}
      </LogsContainer>
      
      {/* 关键词区域 */}
      {keywords.length > 0 && (
        <>
          <DiagnosisTitle>关键问题</DiagnosisTitle>
          <KeywordContainer>
            {keywords.map((keyword, index) => (
              <KeywordTag key={index}>{keyword}</KeywordTag>
            ))}
          </KeywordContainer>
        </>
      )}
      
      {/* 搜索结果区域 */}
      {searchResults.length > 0 && (
        <>
          <DiagnosisTitle>推荐资源</DiagnosisTitle>
          <SearchResultsContainer>
            {searchResults.map((result, index) => (
              <SearchResultItem 
                key={index} 
                onClick={() => handleOpenUrl(result.url)}
              >
                <SearchResultTitle>{result.title}</SearchResultTitle>
                <div style={{ padding: '0 10px 10px', fontSize: '12px', color: '#666' }}>
                  {result.snippet}
                </div>
              </SearchResultItem>
            ))}
          </SearchResultsContainer>
        </>
      )}
      
      {/* 内容结果区域 */}
      {contentResults.length > 0 && (
        <>
          <DiagnosisTitle>内容预览</DiagnosisTitle>
          <SearchResultsContainer>
            {contentResults.map((content, index) => (
              <SearchResultItem 
                key={index} 
                onClick={() => handleOpenUrl(content.url)}
              >
                <SearchResultTitle>{content.title}</SearchResultTitle>
                <div style={{ padding: '0 10px 10px', fontSize: '12px', color: '#666' }}>
                  {content.content.substring(0, 150)}...
                </div>
              </SearchResultItem>
            ))}
          </SearchResultsContainer>
        </>
      )}
      
      {/* 加载中状态 */}
      {isSearching && searchResults.length === 0 && (
        <SearchLoading>
          正在搜索相关教学资源...
        </SearchLoading>
      )}
      
      {/* 错误信息 */}
      {error && (
        <div style={{ color: '#ef4444', padding: '10px', textAlign: 'center' }}>
          {error}
        </div>
      )}
    </>
  );
}; 