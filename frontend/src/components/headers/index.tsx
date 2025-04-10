import React from "react";
import {
  Header as StyleHeader,
  LogoContainer,
  StyledVoiceLogo,
  Title,
  Subtitle,
} from "./style";

const Header = () => {
  return (
    <StyleHeader>
      <LogoContainer>
        <StyledVoiceLogo />
        <Title>POLYVOICE.AI</Title>
      </LogoContainer>
      <Subtitle>您的口语教练</Subtitle>
    </StyleHeader>
  );
};
export default Header;
