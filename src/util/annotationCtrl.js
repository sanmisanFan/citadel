export const citationHighlight = (viewerRef, citations) => {
  if (!viewerRef.current) return;

  const viewer = viewerRef.current;
  citations.forEach((e, i) => {
    const pageElement = viewer.querySelector(
      `.react-pdf__Page[data-page-number="${page}"] .react-pdf__Page__textContent`
    );

    if (pageElement) {
      const highlightDiv = document.createElement("div");
      highlightDiv.style.position = "absolute";
      highlightDiv.style.left = `${rect.x * 100}%`;
      highlightDiv.style.top = `${rect.y * 100}%`;
      highlightDiv.style.width = `${rect.width * 100}%`;
      highlightDiv.style.height = `${rect.height * 100}%`;
      highlightDiv.style.backgroundColor = color;
      highlightDiv.style.opacity = "0.5";
      pageElement.appendChild(highlightDiv);
    }
  });

};