import "./Messages.css";
import { useState } from "react";

function Messages() {
  const [message, setMessage] = useState(""); // Store current input message
  const [messages, setMessages] = useState([]); // Store the list of messages

  // Handle input change for message
  const handleInputChange = (e) => {
    setMessage(e.target.value);
  };

  // Handle message submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (message.trim() !== "") {
      // Add current user's message
      setMessages([...messages, { text: message, sender: "You" }]);
      setMessage(""); // Clear input field

      const query = message;
      const simple = true;

      try {
        const response = await fetch(
          `http://localhost:8000/agent/${query}?simple=${simple}`
        );
        const data = await response.json();
        console.log(data.messages[data.messages.length - 1].content);

        const last_message = data.messages[data.messages.length - 1].content;
        // Add the response message
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: last_message, sender: "Chef" },
        ]);
      } catch (error) {
        console.error("Error:", error);
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: error, sender: "Error" },
        ]);
      }
    }
  };

  return (
    <>
      <div className="chat-box">
        <ul>
          {messages.map((msg, index) => (
            <li key={index} className={`message ${msg.sender.toLowerCase()}`}>
              <strong>{msg.sender}: </strong>
              {msg.text}
            </li>
          ))}
        </ul>
      </div>

      <form
        onSubmit={handleSubmit}
        className="message-form" //form-inactive class
      >
        <input
          type="text"
          value={message}
          onChange={handleInputChange}
          placeholder="Type a message..."
          className="input-field"
        />
        <button type="submit" className="submit-btn" aria-label="Send message">
          Send
        </button>
      </form>
    </>
  );
}

export default Messages;
