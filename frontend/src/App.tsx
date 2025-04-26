import React from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import HomePage from "./pages/homePage";
import ChatPage from "./pages/chat";

// 路由容器组件，根据路径应用不同的容器类
const AppContainer = ({ children }: { children: React.ReactNode }) => {
  const location = useLocation();
  const isChat = location.pathname === "/chat";
  
  return (
    <div className={isChat ? "App-fullscreen" : "App"}>
      {children}
    </div>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <div className="App">
            <HomePage />
          </div>
        } />
        <Route path="/chat" element={
          <div className="App-fullscreen">
            <ChatPage />
          </div>
        } />
      </Routes>
    </Router>
  );
}

export default App;
