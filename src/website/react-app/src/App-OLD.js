import React, { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState(""); // Store current input message
  const [messages, setMessages] = useState([]); // Store the list of messages
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // Track if sidebar is open
  const [image, setImage] = useState(null); // Store the uploaded image
  const [todoItems, setTodoItems] = useState([]); // Store the to-do list items
  const [newTodo, setNewTodo] = useState(""); // New to-do item input

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

  // Toggle sidebar visibility
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  // Handle image upload
  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result); // Store the uploaded image in state
      };
      reader.readAsDataURL(file); // Read the file as a data URL
    }
  };

  // Handle to-do item input change
  const handleTodoChange = (e) => {
    setNewTodo(e.target.value);
  };

  // Handle to-do item submission
  const handleAddTodo = (e) => {
    e.preventDefault();
    if (newTodo.trim() !== "") {
      setTodoItems([...todoItems, newTodo]); // Add new item to the to-do list
      setNewTodo(""); // Clear input field
    }
  };

  // Handle to-do item deletion
  const handleDeleteTodo = (index) => {
    setTodoItems(todoItems.filter((_, i) => i !== index)); // Remove item by index
  };

  return (
    <div className="App">
      <h1>React Messaging System</h1>

      {/* Sidebar */}
      <div className={`sidebar ${isSidebarOpen ? "open" : ""}`}>
        <h2>Sidebar Content</h2>
        <p>Here you can add additional features, settings, etc.</p>

        {/* Image upload section */}
        <div className="image-upload">
          <label htmlFor="image-upload" className="upload-btn">
            Upload Image
          </label>
          <input
            type="file"
            id="image-upload"
            accept="image/*"
            onChange={handleImageUpload}
            style={{ display: "none" }} // Hide the default file input
          />
        </div>

        {/* To-Do List */}
        <div className="todo-list">
          <h3>To-Do List</h3>
          <form onSubmit={handleAddTodo} className="todo-form">
            <input
              type="text"
              value={newTodo}
              onChange={handleTodoChange}
              placeholder="Add a new task..."
              className="todo-input"
            />
            <button type="submit" className="todo-submit-btn">
              Add
            </button>
          </form>
          <ul className="todo-items">
            {todoItems.map((item, index) => (
              <li key={index} className="todo-item">
                {item}
                <button
                  className="delete-todo-btn"
                  onClick={() => handleDeleteTodo(index)}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Hamburger Menu Button */}
      <button
        className="hamburger-btn"
        onClick={toggleSidebar}
        aria-label={isSidebarOpen ? "Close Sidebar" : "Open Sidebar"}
      >
        <span className={`bar ${isSidebarOpen ? "bar-open" : ""}`}></span>
        <span className={`bar ${isSidebarOpen ? "bar-open" : ""}`}></span>
        <span className={`bar ${isSidebarOpen ? "bar-open" : ""}`}></span>
      </button>

      {/* Chat Box */}
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

      {/* Display uploaded image */}
      {image && <img src={image} alt="Uploaded" className="uploaded-image" />}

      {/* Message Input Form */}
      <form onSubmit={handleSubmit} className="message-form">
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
    </div>
  );
}

export default App;
