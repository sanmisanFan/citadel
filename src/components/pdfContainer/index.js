import { useEffect, useCallback, useState, useRef } from "react";
import { pdfjs, Document, Page } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';
import './style.css';

//import samplePDF from "../../data/test.pdf";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

export const PDFContainer = ({ 
  file, 
  highlights 
}) => {
  const [numPages, setNumPages] = useState(null);

  const viewerRef = useRef(null);

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
  };

  // Function to apply highlights
  const applyHighlights = () => {
    if (!viewerRef.current) return;

    highlights.forEach(({ page, rect, color }) => {
      const pageElement = viewerRef.current.querySelector(
        `.react-pdf__Page[data-page-number="${page}"] .react-pdf__Page__textContent`
      );

      if (pageElement) {
        const highlightDiv = document.createElement("div");
        highlightDiv.style.position = "absolute";
        highlightDiv.style.left = `${rect.x * 100}%`;
        highlightDiv.style.top = `${rect.y * 100}%`;
        highlightDiv.style.width = `${rect.width * 100}%`;
        highlightDiv.style.height = `${rect.height * 100}%`;
        highlightDiv.style.backgroundColor = color || "yellow";
        highlightDiv.style.opacity = "0.5";
        pageElement.appendChild(highlightDiv);
      }
    });
  };

  useEffect(() => {
    //applyHighlights();
  }, [highlights]);

  return (
    <div
      ref={viewerRef}
      style={{
        //backgroundColor: "#ffffff",
        //height: '94vh',
        width: '100%',
      }}
    >
      <Document
        file={file}
        onLoadSuccess={onDocumentLoadSuccess}
        className="pdf-document"
      >
        {Array.from(new Array(numPages), (el, index) => (
          <Page
            key={`page_${index + 1}`}
            pageNumber={index + 1}
            className="pdf-page"
          />
        ))}
      </Document>

    </div>
  );
};