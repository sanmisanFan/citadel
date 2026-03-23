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
      {/* Underline - positioned at bottom, outside of text area */}
      <div
        style={{
          position: "absolute",
          left: 0,
          bottom: -2,
          width: "100%",
          height: "2px",
          background: baseColor,
          pointerEvents: "none",
        }}
      />
    </div>
  );
};