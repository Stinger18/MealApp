import "./Pantry.css";
import { useState } from "react";

function EntryForm({ newTask, setNewTask, handleSubmit }) {
  return (
    <form className="input-form" onSubmit={handleSubmit}>
      {/* Input field for a new task */}
      <input
        type="text"
        placeholder="ingredient, qty"
        value={newTask}
        onChange={(e) => setNewTask(e.target.value)}
        className="input-field"
      />
      {/* Button to add task */}
      <button onClick={handleSubmit} className="submit-btn">
        Add
      </button>
    </form>
  );
}

function PantryList({ tasks, handleRemoveItem }) {
  return (
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
  );
}

function UpdateDatabase() {
  return (
    <div className="update-db">
      <button className="db-btn" onClick={() => console.log("Get Pantry")}>
        Get Current Pantry
      </button>
      <button className="db-btn" onClick={() => console.log("Confirm Pantry")}>
        Confirm Pantry
      </button>
    </div>
  );
}

function UploadPicture({ uploadPicture }) {
  return (
    <div className="upload-pic">
      <button className="pic-btn" onClick={uploadPicture}>
        Upload Picture
      </button>
    </div>
  );
}

function Pantry() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");

  function uploadPicture() {
    console.log("upload Picture");
  }

  // Handle pantry submission
  const handlePantrySubmit = (e) => {
    e.preventDefault();
    if (newTask.trim() !== "") {
      setTasks([...tasks, newTask]);
      setNewTask("");
    }
  };

  const handleRemoveItem = (index) => {
    setTasks(tasks.filter((_, i) => i !== index));
  };

  return (
    <>
      <UploadPicture uploadPicture={uploadPicture} />
      <UpdateDatabase />
      <EntryForm
        newTask={newTask}
        setNewTask={setNewTask}
        handleSubmit={handlePantrySubmit}
      />
      <PantryList tasks={tasks} handleRemoveItem={handleRemoveItem} />
    </>
  );
}

export default Pantry;
