import React, { useState } from "react";
import "./App.css";
import TitleBar from "./components/TitleBar";
import Sidebar from "./components/Sidebar";
import RecipeBox from "./components/RecipeBox";
import ChefSVG from "./components/ChefSVG";

function App() {
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
        <Sidebar title="Sous-Chef" isActive={ChefActive} />
      </div>
    </div>
  );
}

export default App;
