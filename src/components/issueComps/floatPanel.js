export const FloatingPanel = ({
  currentPage
}) => {
  return (
    <div
      style={{
        position: "absolute",
        top: "10px",
        right: "10px",
        width: "200px",
        padding: "10px",
        backgroundColor: "white",
        border: "1px solid #ddd",
        borderRadius: "5px",
        boxShadow: "0px 2px 5px rgba(0,0,0,0.2)",
        zIndex: 1000,
      }}
    >
      <h4 style={{ margin: "0 0 10px 0" }}>Page monitor & legend</h4>
      Page: {currentPage}
    </div>
  );
};
