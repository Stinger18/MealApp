import "./TitleBar.css";
function TitleBar({ logoURL, title, chefURL }) {
  return (
    <div className="banner-container">
      <img src={logoURL} alt="Logo" className="logo" />
      <h1 className="title">{title}</h1>
      <img src={chefURL} alt="ChefHat" className="logo" />
    </div>
  );
}

export default TitleBar;
