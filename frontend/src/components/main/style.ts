import styled from "styled-components";

export const Main = styled.main`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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
  background-color: #1a1a1a;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  border: 1px solid #333333;

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
