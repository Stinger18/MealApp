import "./Messages.css";

function Messages({ message, messages, handleInputChange, handleSubmit }) {
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
        className={"message-form"} //form-inactive class
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
