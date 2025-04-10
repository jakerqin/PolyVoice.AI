import styled from "styled-components";
import { ReactComponent as VoiceLogo } from "../../assets/aiVoice.svg";

export const AppContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
`;

export const Header = styled.header`
  text-align: center;
  margin-bottom: 3rem;
  padding-top: 2rem;
`;

export const LogoContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
`;

export const StyledVoiceLogo = styled(VoiceLogo)`
  width: 60px;
  height: 60px;
  margin-right: 0rem;
`;

export const Title = styled.h1`
  font-size: 3rem;
  font-weight: 700;
  color: #1fe05d;
  letter-spacing: 1px;

  @media (max-width: 768px) {
    font-size: 2rem;
  }
`;

export const Subtitle = styled.p`
  font-size: 1.2rem;
  color: #999;
  margin-top: 0.5rem;
`;
