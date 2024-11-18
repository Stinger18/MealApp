import React, { useState } from "react";
import "./App.css";
import TitleBar from "./components/TitleBar";
import Sidebar from "./components/Sidebar";
import RecipeBox from "./components/RecipeBox";
import ChefSVG from "./components/ChefSVG";
import Messages from "./components/Messages";

function App() {
  const [message, setMessage] = useState(""); // Store current input message
  const [messages, setMessages] = useState([]); // Store the list of messages

  // Handle input change for message
  const handleInputChange = (e) => {
    setMessage(e.target.value);
  };

  // Handle message submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() !== "") {
      // Add current user's message
      setMessages([...messages, { text: message, sender: "You" }]);
      setMessage(""); // Clear input field

      // Simulate "Other" user response with delay
      setTimeout(() => {
        const response = `Response to: "${message}"`; // Automatic response logic
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: response, sender: "Other" },
        ]);
      }, 1000); // Simulate a delay of 1 second for the "Other" user to respond
    }
  };

  //##############################################
  const [ChefActive, setChefActive] = useState(true);

  function handleChefClick() {
    setChefActive((curr) => !curr);
  }

  return (
    <div className="background">
      <TitleBar
        logoURL="./tempLogo.png"
        title="What's For Dinner?"
        SVG={<ChefSVG state={ChefActive} onClick={handleChefClick} />}
      />
      <div className="main-container">
        <Sidebar title="Pantry" />
        <RecipeBox />
        <Sidebar title="Sous-Chef" isActive={ChefActive}>
          <Messages
            message={message}
            messages={messages}
            handleInputChange={handleInputChange}
            handleSubmit={handleSubmit}
          />
        </Sidebar>
      </div>
    </div>
  );
}

export default App;
