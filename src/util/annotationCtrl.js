import { createRoot } from "react-dom/client";
import { HighlightBbox } from "../components/issueComps/issueHighLighter";



export const citationHighlight = (viewerRef, citation, anomalous, anomalousColorScheme) => {
  const bboxHeightOffest = 0.003;

  if (!viewerRef.current) return;

  const viewer = viewerRef.current;
  const pageElements = viewer.querySelectorAll(".react-pdf__Page");
  pageElements.forEach((pageElement) => {
    const textContentLayer = pageElement.querySelector(".react-pdf__Page__textContent");
    if (textContentLayer) {
      // Clear existing React Highlights
      const existingContainers = textContentLayer.querySelectorAll(".citation-highlighter-container");
      existingContainers.forEach((container) => container.remove());

      // Get the transformation scale from the text layer
      const { width: layerWidth, height: layerHeight } = textContentLayer.getBoundingClientRect();
      citation.forEach((e, i) => {
        // get each citation
        const id = e.id;
        const citePos = e.cite_positions;
        const anomalousFlag = e.has_issue;

        // Filter citations for the current page
        citePos
        .filter((cite) => cite.page === Number(pageElement.dataset.pageNumber))
        .forEach((cite, citeIndex) => {
          const bbox = cite.bbox;
          const hasIssue = cite.has_issue;
          const issueID = hasIssue ? cite.issues[0] : null;
          const issue = !hasIssue 
            ? null 
            : anomalous.filter(anomalousObj=>anomalousObj.id === issueID)[0];

          // Convert normalized coordinates to pixel values
          const highlightX = bbox.x * layerWidth;
          const highlightY = bbox.y * layerHeight;
          const highlightWidth = bbox.width * layerWidth;
          const highlightHeight = (bbox.height + bboxHeightOffest) * layerHeight;

          // Create a container for the individual highlight
          const highlightContainer = document.createElement("div");
          highlightContainer.className = "citation-highlighter-container";
          highlightContainer.style.position = "absolute";
          highlightContainer.style.left = `${highlightX}px`;
          highlightContainer.style.top = `${highlightY}px`;
          highlightContainer.style.width = `${highlightWidth}px`;
          highlightContainer.style.height = `${highlightHeight}px`;

          // Mount the React Highlight component
          const root = createRoot(highlightContainer);
          root.render(
            <HighlightBbox
              issue={issue}
              cite={cite}
              anomalousColorScheme={anomalousColorScheme}

              onClick={(highlightId) => console.log(highlightId)}
            />
          );
          // Append the highlight container to the text layer
          textContentLayer.appendChild(highlightContainer);
        });
      });
    }
  });
};