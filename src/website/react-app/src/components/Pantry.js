import "./Pantry.css";

function Pantry({
  tasks,
  newTask,
  setNewTask,
  handleSubmit,
  handleRemoveItem,
}) {
  // Add a new task
  return (
    <>
      <form className="input-form" onSubmit={handleSubmit}>
        {/* Input field for a new task */}
        <input
          type="text"
          placeholder="Enter an ingredient..."
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          className="input-field"
        />
        {/* Button to add task */}
        <button onClick={handleSubmit} className="submit-btn">
          Add
        </button>
      </form>

      {/* List of tasks */}
      <ul>
        {tasks.map((task, index) => (
          <li key={index}>
            {task}
            <button onClick={() => handleRemoveItem(index)} className="del-btn">
              Delete
            </button>
          </li>
        ))}
      </ul>
    </>
  );
}

export default Pantry;
