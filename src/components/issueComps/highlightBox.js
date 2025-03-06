import { Popover } from "antd";

export const HighlightBbox = ({
  boxid,
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

  const popContent = (
    <div
      style={{
        maxWidth: 400
      }}
    >
      <p style={{margin: 0}}>{citeObj.source}</p>
    </div>
  );

  return(
    <Popover 
      content={popContent}
    >
    <div
      //className="highlight"
      id={"citeAnnotation_"+boxid}
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        width: "100%",
        height: "100%",
        background: activeHighlight === cite.issues[0] ? boxColor : "",
        border: categoryColor !== null ? "3px solid" : "",
        borderColor: categoryColor !== null ? categoryColor : "",
        borderRadius: 8,
        //opacity: 0.5,
        cursor: "pointer",
        pointerEvents: "auto"
      }}
      onClick={() => onClick(cite.issues[0])}
      /*onMouseEnter={(e) => {
        e.target.style.border = "3px solid blue";
      }}
      onMouseLeave={(e) => {
        e.target.style.border = "";
      }}*/
    >
    </div>
    </Popover>
  );
};