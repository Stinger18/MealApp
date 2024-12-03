import "./Pantry.css";

function Pantry({ tasks, setTasks, newTask, setNewTask }) {
  // Add a new task
  function addTask() {
    if (newTask.trim() !== "") {
      setTasks([...tasks, newTask]);
      setNewTask("");
    }
  }

  // Remove a task by index
  function removeTask(index) {
    setTasks(tasks.filter((_, i) => i !== index));
  }

  return (
    <>
      <div>
        {/* Input field for a new task */}
        <input
          type="text"
          placeholder="Enter an ingredient..."
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
        />
        {/* Button to add task */}
        <button onClick={addTask}>Add ingredient</button>
      </div>

      {/* List of tasks */}
      <ul>
        {tasks.map((task, index) => (
          <li key={index}>
            {task}
            <button onClick={() => removeTask(index)}>Delete</button>
          </li>
        ))}
      </ul>

      {/* <form onSubmit={handleSubmit} className="message-form">
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
      </form> */}
    </>
  );
}

export default Pantry;
