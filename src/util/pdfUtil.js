import { pdfjs } from "react-pdf";

/*pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();*/
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

// Function to extract text from a PDF page
export const extractTextFromPage = async (pdf, pageNumber) => {
  try {
    const page = await pdf.getPage(pageNumber);
    const textContent = await page.getTextContent();
    return textContent.items.map((item) => ({
      text: item.str,
      transform: item.transform,
      width: item.width,
      height: item.height,
      x: item.transform[4],
      y: item.transform[5],
    }));
  } catch (error) {
    console.error(`Error extracting text from page ${pageNumber}:`, error);
    return [];
  }
};

// search for the first sentence in the first section
export const findSentenceCoordinates = (textItems, sentence) => {
  const targetItem = textItems.find((item) => item.text.includes(sentence));
  if (targetItem) {
    return {
      x: targetItem.x,
      y: targetItem.y,
      width: targetItem.width,
      height: targetItem.height,
    };
  }
  return null;
};

/**
 * Find the <span> element in the rendered text layer that contains the citation
 * marker (e.g. "[21]"). Used as a proximity anchor for disambiguation.
 */
export const findCitationAnchorSpan = (textLayerEl, citationMarker) => {
  if (!citationMarker || !textLayerEl) return null;
  return (
    Array.from(textLayerEl.querySelectorAll("span")).find((s) =>
      s.textContent.includes(citationMarker)
    ) || null
  );
};

/**
 * Find a sentence's bounding rects in the rendered PDF text layer DOM.
 *
 * Each PDF line is one or more <span> elements. We build a character-indexed
 * map over the concatenated (normalised) text of all spans so we can locate
 * a substring match and resolve it back to individual spans.
 *
 * When the same sentence appears more than once on the page, anchorEl
 * (the citation-marker span) is used to pick the occurrence that is
 * visually closest — by vertical distance — to that marker.
 *
 * Returns an array of { x, y, width, height } pixel rects measured
 * relative to textLayerEl. One rect per involved span (= per visual line).
 */
export const findSentenceInTextLayer = (textLayerEl, sentenceText, anchorEl = null) => {
  if (!textLayerEl || !sentenceText) return [];

  const spans = Array.from(textLayerEl.querySelectorAll("span"));
  if (!spans.length) return [];

  const norm = (s) => s.replace(/\s+/g, " ").trim().toLowerCase();
  const target = norm(sentenceText);
  if (!target) return [];

  // Build normalised full text + per-character span-index map.
  // We add a single space between spans so that words at span boundaries
  // are not accidentally merged.
  const charSpanMap = [];
  let fullText = "";

  spans.forEach((span, spanIdx) => {
    const t = norm(span.textContent);
    for (let j = 0; j < t.length; j++) charSpanMap.push(spanIdx);
    fullText += t;
    // separator (not attributed to any span)
    fullText += " ";
    charSpanMap.push(-1);
  });

  // Collect every occurrence of target in fullText.
  const occurrences = [];
  let pos = 0;
  while (pos < fullText.length) {
    const idx = fullText.indexOf(target, pos);
    if (idx === -1) break;
    const spanSet = new Set();
    for (let i = idx; i < idx + target.length; i++) {
      const si = charSpanMap[i];
      if (si !== -1) spanSet.add(si);
    }
    if (spanSet.size > 0) occurrences.push({ idx, spanIndices: [...spanSet] });
    pos = idx + 1;
  }

  if (!occurrences.length) return [];

  // Choose the occurrence closest to the anchor (citation marker span).
  let chosen = occurrences[0];
  if (occurrences.length > 1 && anchorEl) {
    const layerRect = textLayerEl.getBoundingClientRect();
    const anchorY = anchorEl.getBoundingClientRect().top - layerRect.top;
    let minDist = Infinity;
    for (const occ of occurrences) {
      const firstSpan = spans[occ.spanIndices[0]];
      const dist = Math.abs(
        firstSpan.getBoundingClientRect().top - layerRect.top - anchorY
      );
      if (dist < minDist) {
        minDist = dist;
        chosen = occ;
      }
    }
  }

  // Convert matched span bounding boxes to coords relative to the text layer.
  const layerRect = textLayerEl.getBoundingClientRect();
  return chosen.spanIndices.map((si) => {
    const r = spans[si].getBoundingClientRect();
    return {
      x: r.left - layerRect.left,
      y: r.top - layerRect.top,
      width: r.width,
      height: r.height,
    };
  });
};

// Function to find the bounding box for a specific citation (e.g. "[14]") within text items
export const findCitationCoordinates = (textItems, targetCitation) => {
  const results = [];
  
  textItems.forEach((item) => {
    // Find the starting index of the target citation within the text item
    const index = item.text.indexOf(targetCitation);
    if (index !== -1) {
      // Estimate the average width per character
      const totalChars = item.text.length;
      if (totalChars === 0) return; // safeguard
      
      const charWidth = item.width / totalChars;
      // Calculate the width of the citation substring
      const citationWidth = charWidth * targetCitation.length;
      // Calculate the x-offset for the citation substring
      const citationX = item.x + (index * charWidth);
      
      results.push({
        citation: targetCitation,
        x: citationX,
        y: item.y,
        width: citationWidth,
        height: item.height,
      });
    }
  });
  
  return results;
};


export async function loadPDF(path) {
  try {
    const pdfPath = "../data/test.pdf"; // Replace 'sample.pdf' with your file name

    // Fetch the PDF file as a binary blob
    const response = await fetch(pdfPath);

    if (!response.ok) {
      throw new Error(`Failed to fetch PDF file: ${response.statusText}`);
    }

    // Read the response as an ArrayBuffer
    const arrayBuffer = await response.arrayBuffer();

    // Convert the ArrayBuffer into a Uint8Array
    const uint8Array = new Uint8Array(arrayBuffer);

    // returm the PDF data in Uint8Array for PDFJS
    console.log("PDF loaded and converted to Uint8Array:", uint8Array);

    return uint8Array;

  } catch (error) {
    console.error("Error loading PDF:", error);
  }
};


export const extractAndHighlight = async (pdf, targetSentence, pageNumber = 1) => {
  const page = await pdf.getPage(pageNumber);
  const viewport = page.getViewport({ scale: 1 });

  const textItems = await extractTextFromPage(pdf, pageNumber); // Extract text from the first page
  const coordinates = findSentenceCoordinates(textItems, targetSentence);

  const normalizedCoordinates = coordinates!== null ? {
    x: coordinates.x / viewport.width,
    y: (viewport.height - coordinates.y - coordinates.height) / viewport.height, // Flip y-axis
    width: coordinates.width / viewport.width,
    height: coordinates.height / viewport.height,
  } : null;
  console.log('normalizedCoordinates', normalizedCoordinates, targetSentence, pageNumber);
};

// Function to extract and highlight a specific citation on a given page
export const extractAndHighlightCitation = async (pdf, targetCitation, pageNumber = 1) => {
  try {
    const page = await pdf.getPage(pageNumber);
    const viewport = page.getViewport({ scale: 1 });
  
    const textItems = await extractTextFromPage(pdf, pageNumber);
    const citations = findCitationCoordinates(textItems, targetCitation);
  
    // Normalize coordinates for the target citation relative to the page viewport
    const normalizedCitations = citations.map(citation => ({
      citation: citation.citation,
      x: citation.x / viewport.width,
      y: (viewport.height - citation.y - citation.height) / viewport.height,
      width: citation.width / viewport.width,
      height: citation.height / viewport.height,
    }));
  
    console.log('Normalized citation coordinates:', normalizedCitations, targetCitation);
    //return normalizedCitations;
  } catch (error) {
    console.error('Error in extractAndHighlightCitation:', error);
    return [];
  }
};
