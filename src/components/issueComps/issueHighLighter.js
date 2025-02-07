import { Popover } from "antd";

export const HighlightBbox = ({
  issue,
  cite,
  citeObj,
  anomalousColorScheme,
  activeHighlight,
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
    : null;

  const popContent = (
    <div
      style={{
        maxWidth: 400
      }}
    >
      <p style={{margin: 0}}>{citeObj.source}</p>
    </div>
  );

  console.log(activeHighlight, cite.issues[0]);

  return(
    <Popover 
      content={popContent}
    >
    <div
      //className="highlight"
      id={"citeAnnotation_"+cite.id}
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        width: "100%",
        height: "100%",
        background: issue !== null ? annotationColor : '',
        //transition: "all 0.2s ease-out",
        border: activeHighlight === cite.issues[0] && "3px solid blue",
        opacity: 0.8,
        cursor: "pointer",
        pointerEvents: "auto"
      }}
      onClick={() => onClick(cite.issues[0])}
      onMouseEnter={(e) => {
        e.target.style.border = "3px solid blue";
      }}
      onMouseLeave={(e) => {
        e.target.style.border = "";
      }}
    >
    </div>
    </Popover>
  );
};