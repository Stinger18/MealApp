import "./SideBar.css";

function Sidebar({ title, isActive = true, containerStyle, children }) {
  return (
    isActive && (
      <div className="sidebar-container" style={containerStyle}>
        <div className="sidebar-title">{title}</div>
        <div className="sidebar-body">{children}</div>
      </div>
    )
  );
}

export default Sidebar;
