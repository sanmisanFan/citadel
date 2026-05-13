import { Popover, Tag } from "antd";

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
        ? (!issue.filter ? anomalousColorScheme[issue.name]['category'][issue.category.name]['baseColor'] : "gray")
        : null;

    const boxColor = issue !== null
        ? anomalousColorScheme[issue.name]['category'][issue.category.name]['boxColor']
        : null;

    // const doiString = `https://doi.org/${citeObj.doi}`;
    const popContent = (
        <div
            style={{
                maxWidth: 400
            }}
        >
            <p style={{ margin: 0 }}><b>Source:</b> {citeObj.source}</p>
            <div style={{ marginTop: 8 }}>
                {cite.has_issue ? (
                    cite.issues.map((issueId) => {
                        const relatedIssue = issue !== null && cite.issues.includes(issue.id) ? issue : null;
                        if (relatedIssue) {
                            const issueDisplayName = relatedIssue.displayName;
                            const issueCategoryName = relatedIssue.category.displayName;
                            const issueBaseColor = anomalousColorScheme[relatedIssue.name]['baseColor'];
                            const issueCategoryColor = anomalousColorScheme[relatedIssue.name]['category'][relatedIssue.category.name]['baseColor'];
                            return (
                                <div key={issueId = "_container"}>
                                    <b style={{ color: issueBaseColor }}>{issueDisplayName}: </b>
                                    <Tag key={issueId} color={issueCategoryColor} style={{ margin: "0 4px" }}>
                                        {issueCategoryName}
                                    </Tag>
                                </div>

                            );
                        }
                        return null;
                    })
                ) : (
                    <Tag color="green" style={{ margin: "0 4px" }}>
                        <b>No Issues Found</b>
                    </Tag>
                )}
            </div>
        </div>
    );

    return (
        <Popover
            content={popContent}
        >
            <div
                //className="highlight"
                id={"citeAnnotation_" + boxid}
                style={{
                    position: "absolute",
                    left: 0,
                    top: 0,
                    width: "100%",
                    height: "100%",
                    background: Array.isArray(cite.issues) && cite.issues.includes(activeHighlight) ? boxColor : "",
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
