import "./SideBar.css";

function Sidebar({ title, isActive = true, styles, children }) {
  return (
    isActive && (
      <div className="sidebar-container" style={styles?.container}>
        <div className="sidebar-title" style={styles?.title}>
          {title}
        </div>
        <div className="sidebar-body" style={styles?.body}>
          {children}
        </div>
      </div>
    )
  );
}

export default Sidebar;
