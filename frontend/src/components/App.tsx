"""Main App component."""
import React, { useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import ChatArea from "./ChatArea";
import DocumentUpload from "./DocumentUpload";
import SettingsPanel from "./SettingsPanel";
import "../styles/App.css";

type AppView = "chat" | "settings";

const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [view, setView] = useState<AppView>("chat");

  useEffect(() => {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
      setDarkMode(true);
      document.documentElement.classList.add("dark");
    }
  }, []);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    if (!darkMode) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  };

  return (
    <div className={`app ${darkMode ? "dark" : "light"}`}>
      <Sidebar
        onViewChange={setView}
        currentView={view}
        darkMode={darkMode}
        onToggleDarkMode={toggleDarkMode}
      />
      <main className="main-content">
        {view === "chat" && (
          <>
            <ChatArea />
            <DocumentUpload />
          </>
        )}
        {view === "settings" && <SettingsPanel />}
      </main>
    </div>
  );
};

export default App;
