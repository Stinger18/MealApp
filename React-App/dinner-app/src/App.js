// import React, { useState } from "react";
import "./App.css";
import TitleBar from "./components/TitleBar";
import Sidebar from "./components/Sidebar";
import RecipeBox from "./components/RecipeBox";

function App() {
  return (
    <div className="background">
      <TitleBar
        logoURL="https://via.placeholder.com/100"
        title="What's For Dinner?"
        chefURL="https://via.placeholder.com/100"
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
