export const HighlightBbox = ({
  issue,
  cite,
  anomalousColorScheme,
  onClick
}) => {
  const categoryColor = issue !== null 
    ? anomalousColorScheme[issue.name]['category'][issue.category.name]['baseColor']
    : null;

  const boxColor = issue !== null 
    ? anomalousColorScheme[issue.name]['category'][issue.category.name]['boxColor']
    : null;

  const annotationColor = issue !== null 
    ? anomalousColorScheme[issue.name]['category'][issue.category.name]['annotationCss']
    : null
  

  return(
    <div
      className="highlight"
      id={"citeAnnotation_"+cite.id}
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        width: "100%",
        height: "100%",
        background: issue !== null ? annotationColor : '',
        transition: "all 0.2s ease-in-out",
        border: "2px solid transparent",
        //opacity: 0.8,
        cursor: "pointer",
        pointerEvents: "auto"
      }}
      onClick={() => onClick(cite)}
      onMouseEnter={(e) => {
        e.target.style.border = "2px solid green";
        //e.target.style.borderImage = annotationColor+" 1";
        //e.target.style.background = "transparent";
      }}
      onMouseLeave={(e) => {
        e.target.style.border = "2px solid transparent";
      }}
    >
    </div>
  );
};