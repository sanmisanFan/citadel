export const SentenceAnnotation = ({
  issueID,
  issueName,
  issueCategory,
  baseColor,
  boxColor,
  activeHighlight,
  onClick
}) => {
  const isActive = activeHighlight === issueID;

  return(
    <div
      id={"sentenceAnnotation_"+issueID}
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        width: "100%",
        height: "100%",
        cursor: "pointer",
        pointerEvents: "auto",
      }}
      onClick={() => onClick(isActive ? null : issueID)}
    >
      {/* Background highlight - only when active, behind text */}
      {isActive && (
        <div
          style={{
            position: "absolute",
            left: 0,
            top: 0,
            width: "100%",
            height: "100%",
            background: boxColor,
            pointerEvents: "none",
            zIndex: -1,
          }}
        />
      )}
      {/* Underline - thicker/saturated when active, muted when inactive,
          so the selected anomaly is unambiguous even when several
          underlines stack on the same line. */}
      <div
        style={{
          position: "absolute",
          left: 0,
          bottom: isActive ? -3 : -2,
          width: "100%",
          height: isActive ? "3px" : "2px",
          background: baseColor,
          opacity: isActive ? 1 : 0.35,
          pointerEvents: "none",
        }}
      />
    </div>
  );
};