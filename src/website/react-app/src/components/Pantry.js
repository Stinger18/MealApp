import "./Pantry.css";
import { useState } from "react";

const tempPantry = [
  { item: "flour", qty: 5 },
  { item: "eggs", qty: 11 },
  { item: "butter", qty: 1 },
  { item: "sugar", qty: 3 },
  { item: "milk", qty: 2 },
];

const BACKEND_URL = "http://127.0.0.1:8000";

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
    <ul className="pantry-list">
      {tasks.map((task, index) => (
        <li key={index} className="pantry-item">
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
      <label htmlFor="file_upload" className="pic-btn">
        Upload Picture
      </label>
      <input
        type="file"
        onChange={uploadPicture}
        className="pic-input"
        accept="image/*"
        id="file_upload"
      />
    </div>
  );
}

function Pantry() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");
  const [pantry, setPantry] = useState(tempPantry); //setting pantry to initial dummy pantry
  const [fileName, setFileName] = useState("");

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

  async function uploadPicture(file) {
    console.log(`uploaded: ${file.name}`);

    try {
      const response = await fetch(`http://localhost:8000/image/${file.name}`);
      const data = await response.json();
      console.log(data);
      for (const dic in data) {
        console.log(dic);
      }

      // for ( data.keys()) {
      //   // setTasks((prevItems) => [`${key}, ${data[key]}`, ...prevItems]);      }
      // }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  async function getDB() {
    //TODO: add pantryId
    console.log("Get DB");
    pantry.forEach((dict) =>
      setTasks((prevItems) => [`${dict.item}, ${dict.qty}`, ...prevItems])
    );
    // const pantryId = 1;
    // fetch(`${BACKEND_URL}/pantry/${pantryId}`)
    //   .then((response) => response.json())
    //   .then((data) => {
    //     console.log(`Data: ` + data);
    //     data.forEach((item) => {
    //       console.log(item);
    //       setTasks((prevItems) => [`${item.item}, ${item.qty}`, ...prevItems]);
    //     });
    //   })
    //   .catch((error) => console.error("Error fetching users pantry: ", error));
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

  const handleFileChange = (event) => {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      setFileName(file.name);
      uploadPicture(file);
    }
  };

  return (
    <>
      <UploadPicture uploadPicture={handleFileChange} />
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
