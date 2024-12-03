import "./TitleBar.css";
function TitleBar({ logoURL, handleLogoClick, title, SVG }) {
  return (
    <div className="banner-container">
      <img
        src={logoURL}
        alt="Logo"
        onClick={handleLogoClick}
        className="logo"
      />
      <h1 className="title">{title}</h1>
      {SVG}
    </div>
  );
}

export default TitleBar;
