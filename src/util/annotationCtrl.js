import { createRoot } from "react-dom/client";
import { HighlightBbox } from "../components/issueComps/highlightBox";
import { pdfBboxToLayerRect } from "./anomalyAnchor";

const BBOX_HEIGHT_OFFSET = 0.003;

/**
 * Draw a colored box around every [N] citation marker that has an issue.
 *
 * Each citation now carries ``cite_positions`` — one record per [N]
 * occurrence in the manuscript body — populated server-side from the
 * GROBID TEI coords. Each record has ``page``, raw-PDF-coord ``bbox``,
 * ``page_width`` / ``page_height`` for normalization, ``ref_label``, and
 * ``issues`` (the anomaly IDs attached to this marker).
 */
export const citationHighlight = (
  viewerRef,
  citation,
  anomalous,
  anomalousColorScheme,
  activeHighlight,
  setActiveHighlight
) => {
  if (!viewerRef.current) return;

  const viewer = viewerRef.current;
  const pageElements = viewer.querySelectorAll(".react-pdf__Page");
  pageElements.forEach((pageElement) => {
    const textContentLayer = pageElement.querySelector(".react-pdf__Page__textContent");
    if (!textContentLayer) return;

    // Clear existing React highlights (re-rendered every effect tick).
    textContentLayer
      .querySelectorAll(".citation-highlighter-container")
      .forEach((container) => container.remove());

    const pageNumber = Number(pageElement.dataset.pageNumber);

    citation.forEach((citationObj) => {
      const positions = citationObj.cite_positions;
      if (!Array.isArray(positions) || positions.length === 0) return;

      positions
        .filter((p) => p.page === pageNumber && p.bbox && p.bbox.x != null)
        .forEach((cite, citeIndex) => {
          const rect = pdfBboxToLayerRect(
            cite.bbox,
            pageElement,
            cite.page_width,
            cite.page_height
          );
          if (!rect) return;

          // Pad height slightly so the box sits comfortably around the
          // marker glyphs without clipping descenders.
          const paddedHeight = rect.height * (1 + BBOX_HEIGHT_OFFSET);

          const hasIssue = Array.isArray(cite.issues) && cite.issues.length > 0;
          const primaryIssueId = hasIssue ? cite.issues[0] : null;
          const issue = primaryIssueId
            ? anomalous.find((a) => a.id === primaryIssueId) || null
            : null;
          // Pass the full set of issue IDs for this marker so HighlightBbox
          // can tell when the *active* anomaly matches any of them.
          const citeForBox = { ...cite, has_issue: hasIssue };

          const container = document.createElement("div");
          container.className = "citation-highlighter-container";
          container.style.position = "absolute";
          container.style.left = `${rect.x}px`;
          container.style.top = `${rect.y}px`;
          container.style.width = `${rect.width}px`;
          container.style.height = `${paddedHeight}px`;

          const root = createRoot(container);
          root.render(
            <HighlightBbox
              boxid={citationObj.id + "_" + citeIndex}
              issue={issue}
              cite={citeForBox}
              citeObj={citationObj}
              anomalousColorScheme={anomalousColorScheme}
              activeHighlight={activeHighlight}
              onClick={(highlightId) =>
                highlightId !== undefined && setActiveHighlight(highlightId)
              }
            />
          );
          textContentLayer.appendChild(container);
        });
    });
  });
};
