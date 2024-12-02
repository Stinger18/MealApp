import "./TitleBar.css";
function TitleBar({ logoURL, title, SVG }) {
  return (
    <div className="banner-container">
      <img src={logoURL} alt="Logo" className="logo" />
      <h1 className="title">{title}</h1>
      {SVG}
    </div>
  );
}

export default TitleBar;
