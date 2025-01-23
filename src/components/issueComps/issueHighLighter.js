export const HighlightBbox = ({
  glyph,
  color,
  id,
  onClick
}) => {
  return(
    <div
      className="highlight"
      id={"highlight-bbox-"+id}
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        width: "100%",
        height: "100%",
        backgroundColor: color,
        //opacity: 0.3,
        cursor: "pointer",
        pointerEvents: "auto",
      }}
      onClick={() => onClick(id)}
    >
      {/* Add a small square in the top-right corner */}
      <div
        id={"highlight-bbox-square-"+id}
        className="highlight-square"
        style={{
          position: "absolute",
          top: "5px", // Position above the rect
          right: "-25px", // Position to the right of the rect
          width: "20px",
          height: "15px",
          backgroundColor: color, // Color of the square
          borderRadius: "2px", // Optional: Rounded corners
          cursor: "pointer",
        }}
        onClick={(e) => {
          e.stopPropagation(); // Prevent the highlight click from triggering
          alert(`Clicked on the square of highlight: ${id}`);
        }}
      >
        <b>{glyph}</b>
      </div>
    </div>
  );
};