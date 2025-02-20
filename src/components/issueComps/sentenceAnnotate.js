import { Popover } from "antd";

export const SentenceAnnotation = ({
  issueID,
  issueName,
  issueCategory,
  baseColor,
  boxColor,
  activeHighlight,
  onClick
}) => {
  return(
    <div
      //className="highlight"
      id={"sentenceAnnotation_"+issueID}
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        width: "100%",
        height: "100%",
        background: activeHighlight === issueID ? boxColor : "",
        //transition: "all 0.2s ease-out",
        //border: activeHighlight === cite.issues[0] && "3px solid blue",
        borderBottom: "3px solid",
        borderBottomColor: baseColor,
        //borderRadius: 8,
        //opacity: 0.5,
        cursor: "pointer",
        pointerEvents: "auto"
      }}
      onClick={() => onClick(activeHighlight === issueID ? null : issueID)}
      /*onMouseEnter={(e) => {
        e.target.style.border = "3px solid blue";
      }}
      onMouseLeave={(e) => {
        e.target.style.border = "";
      }}*/
    >
    </div>
  );
};