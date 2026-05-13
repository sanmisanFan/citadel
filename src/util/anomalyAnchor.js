import { findSentenceInTextLayer, findCitationAnchorSpan } from "./pdfUtil";

// GROBID emits bboxes in PDF user-space (points). When `page_width` /
// `page_height` are missing we fall back to US-Letter at 72 DPI, which is
// the right default for most academic PDFs and is what GROBID itself uses
// when a `<surface>` block is absent from the TEI.
const DEFAULT_PAGE_WIDTH = 612;
const DEFAULT_PAGE_HEIGHT = 792;

const getPageElement = (viewerEl, pageNumber) =>
  viewerEl?.querySelector(
    `.react-pdf__Page[data-page-number="${pageNumber}"]`
  ) || null;

const getTextLayer = (pageEl) =>
  pageEl?.querySelector(".react-pdf__Page__textContent") || null;

/**
 * Convert a GROBID bbox (PDF user-space) to a pixel rect on the rendered
 * text layer. Returns null if the page or text layer hasn't rendered yet,
 * or if the bbox is missing required fields.
 */
export const pdfBboxToLayerRect = (bbox, pageEl, pageWidth, pageHeight) => {
  if (!bbox || bbox.x == null || bbox.y == null) return null;
  const layer = getTextLayer(pageEl);
  if (!layer) return null;
  const { width: layerWidth, height: layerHeight } = layer.getBoundingClientRect();
  if (!layerWidth || !layerHeight) return null;

  const pw = pageWidth || DEFAULT_PAGE_WIDTH;
  const ph = pageHeight || DEFAULT_PAGE_HEIGHT;
  return {
    x: (bbox.x / pw) * layerWidth,
    y: (bbox.y / ph) * layerHeight,
    width: ((bbox.width || 0) / pw) * layerWidth,
    height: ((bbox.height || 0) / ph) * layerHeight,
  };
};

/**
 * Resolve a single anomaly anchor to one or more pixel rects on the
 * rendered text layer of its page.
 *
 * Priority order:
 *   1. marker_bbox — GROBID-supplied coords for the [N] glyph.
 *   2. sentence fuzzy match — find the sentence string in the text layer,
 *      disambiguating by proximity to the marker label when present.
 *   3. [N] scan — locate the visible marker label anywhere on the page.
 *
 * Returns ``{ page, rects, strategy }`` or null if nothing resolved.
 */
export const resolveAnomalyAnchor = (anchor, viewerEl) => {
  if (!anchor || !viewerEl) return null;
  const page = anchor.page;
  if (page == null) return null;
  const pageEl = getPageElement(viewerEl, page);
  if (!pageEl) return null;

  // Strategy 1: marker bbox.
  if (anchor.marker_bbox && anchor.marker_bbox.x != null) {
    const rect = pdfBboxToLayerRect(
      anchor.marker_bbox,
      pageEl,
      anchor.page_width,
      anchor.page_height
    );
    if (rect) return { page, rects: [rect], strategy: "bbox" };
  }

  const textLayer = getTextLayer(pageEl);
  if (!textLayer) return null;

  // Strategy 2: sentence fuzzy match. We pass the marker label (when
  // present) as the disambiguation anchor so the fuzzy matcher prefers
  // occurrences near the right [N].
  if (anchor.sentence) {
    const anchorSpan = anchor.ref_label
      ? findCitationAnchorSpan(textLayer, anchor.ref_label)
      : null;
    const rects = findSentenceInTextLayer(
      textLayer,
      anchor.sentence,
      anchorSpan
    );
    if (rects.length) return { page, rects, strategy: "sentence" };
  }

  // Strategy 3: [N] scan.
  if (anchor.ref_label) {
    const span = findCitationAnchorSpan(textLayer, anchor.ref_label);
    if (span) {
      const layerRect = textLayer.getBoundingClientRect();
      const r = span.getBoundingClientRect();
      return {
        page,
        rects: [
          {
            x: r.left - layerRect.left,
            y: r.top - layerRect.top,
            width: r.width,
            height: r.height,
          },
        ],
        strategy: "scan",
      };
    }
  }

  return null;
};

/**
 * Stable key for grouping rects that point at the same location. Rounds
 * to integer pixels so floating-point jitter (e.g. from getBoundingClientRect
 * after a scroll) doesn't fragment the group.
 */
const rectKey = (rect) =>
  `${Math.round(rect.x)}:${Math.round(rect.y)}:${Math.round(rect.width)}:${Math.round(rect.height)}`;

/**
 * Resolve every anchor for every anomaly, then coalesce by (page, rect)
 * so multiple anomalies that point at the same marker render as a single
 * highlight element tagged with all of their issue IDs.
 *
 * Returns an array of groups: ``[{ page, rect, issues: [{id, ...}], strategy }]``.
 */
export const resolveAllAnchors = (anomalies, viewerEl) => {
  if (!Array.isArray(anomalies) || !viewerEl) return [];
  const groups = new Map();

  anomalies.forEach((anomaly) => {
    if (anomaly?.filter) return;
    (anomaly.anchors || []).forEach((anchor) => {
      const resolved = resolveAnomalyAnchor(anchor, viewerEl);
      if (!resolved) return;
      resolved.rects.forEach((rect) => {
        const key = `${resolved.page}|${rectKey(rect)}`;
        const existing = groups.get(key);
        const issueRef = {
          id: anomaly.id,
          name: anomaly.name,
          displayName: anomaly.displayName,
          category: anomaly.category,
        };
        if (existing) {
          existing.issues.push(issueRef);
        } else {
          groups.set(key, {
            page: resolved.page,
            rect,
            strategy: resolved.strategy,
            issues: [issueRef],
          });
        }
      });
    });
  });

  return [...groups.values()];
};
