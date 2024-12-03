import "./Pantry.css";
import { useState } from "react";

const tempPantry = [
  { item: "flour", qty: 5 },
  { item: "eggs", qty: 11 },
  { item: "butter", qty: 1 },
  { item: "sugar", qty: 3 },
  { item: "milk", qty: 2 },
];

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

function UpdateDatabase({ getDB, confirmDB }) {
  return (
    <div className="update-db">
      <button className="db-btn" onClick={getDB}>
        Get Current Pantry
      </button>
      <button className="db-btn" onClick={confirmDB}>
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
  const [pantry, setPantry] = useState(tempPantry); //setting pantry to initial dummy pantry

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

  function uploadPicture() {
    console.log("upload Picture");
  }

  function getDB() {
    console.log("Get DB");
    pantry.forEach((dict) =>
      setTasks((prevItems) => [`${dict.item}, ${dict.qty}`, ...prevItems])
    );
  }

  function confirmDB() {
    console.log("Confirm DB");
    setPantry(
      tasks.map((item) => {
        const [ingredient, qty] = item.split(", ");
        return { item: ingredient, qty: parseInt(qty) };
      })
    );
    setTasks([]);
  }

  return (
    <>
      <UploadPicture uploadPicture={uploadPicture} />
      <UpdateDatabase getDB={getDB} confirmDB={confirmDB} />
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
