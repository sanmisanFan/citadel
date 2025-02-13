import { pdfjs } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

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


export const extractAndHighlight = async (pdf, targetSentence) => {
  console.log(pdf);
  const page = await pdf.getPage(1);
  const viewport = page.getViewport({ scale: 1 });

  const textItems = await extractTextFromPage(pdf, 1); // Extract text from the first page
  const coordinates = findSentenceCoordinates(textItems, targetSentence);

  const normalizedCoordinates = {
    x: coordinates.x / viewport.width,
    y: (viewport.height - coordinates.y - coordinates.height) / viewport.height, // Flip y-axis
    width: coordinates.width / viewport.width,
    height: coordinates.height / viewport.height,
  };
  console.log('normalizedCoordinates', normalizedCoordinates);
  console.log('coordinates', coordinates);
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
  
    //console.log('Normalized citation coordinates:', normalizedCitations, targetCitation);
    return normalizedCitations;
  } catch (error) {
    console.error('Error in extractAndHighlightCitation:', error);
    return [];
  }
};
