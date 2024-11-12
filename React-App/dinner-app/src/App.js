// import React, { useState } from "react";
import "./App.css";
import TitleBar from "./TitleBar";
import Sidebar from "./Sidebar";
import RecipeBox from "./RecipeBox";

function App() {
  return (
    <div className="background">
      <TitleBar
        logoUrl="https://via.placeholder.com/100"
        title="What's For Dinner?"
      />
      <div className="main-container">
        <Sidebar title="Pantry" />
        <RecipeBox />
        <Sidebar title="Sous-Chef" />
      </div>
    </div>
  );
}

export default App;
