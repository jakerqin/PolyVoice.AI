import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/homePage";
import ChatPage from "./pages/chat";

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
