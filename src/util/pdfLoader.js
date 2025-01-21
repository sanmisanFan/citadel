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
}