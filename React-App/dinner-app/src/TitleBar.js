function TitleBar({ logoUrl, title }) {
  return (
    <div className="banner-container">
      <img src={logoUrl} alt="Logo" className="logo" />
      <h1 className="title">{title}</h1>
    </div>
  );
}

export default TitleBar;
