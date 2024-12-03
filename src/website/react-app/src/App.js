import React, { useState } from "react";
import "./App.css";
import TitleBar from "./components/TitleBar";
import Sidebar from "./components/Sidebar";
import RecipeBox from "./components/RecipeBox";
import ChefSVG from "./components/ChefSVG";
import Messages from "./components/Messages";
import Pantry from "./components/Pantry";

function App() {
  const [ChefActive, setChefActive] = useState(true);
  const [PantryActive, setPantryActive] = useState(true);

  // Handle chef hat click
  function handleChefClick() {
    setChefActive((curr) => !curr);
  }

  // Handle logo click
  function handleLogoClick() {
    setPantryActive((curr) => !curr);
  }

  return (
    <div className="background">
      <TitleBar
        logoURL="./tempLogo.png"
        handleLogoClick={handleLogoClick}
        title="What's For Dinner?"
        SVG={<ChefSVG state={ChefActive} onClick={handleChefClick} />}
      />
      <div className="main-container">
        <Sidebar title="Pantry" isActive={PantryActive}>
          <Pantry />
        </Sidebar>
        <RecipeBox />
        <Sidebar
          title="Sous-Chef"
          isActive={ChefActive}
          containerStyle={{ width: "30%" }}
        >
          <Messages />
        </Sidebar>
      </div>
    </div>
  );
}

export default App;
