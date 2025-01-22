import { pdfjs } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

// Function to extract text from a PDF page
export const extractTextFromPage = async (pdf, pageNumber) => {
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
};

// search for the first sentence in the first section
export const findSentenceCoordinates = (textItems, sentence) => {
  const targetItem = textItems.find((item) => item.text.startsWith(sentence));
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

