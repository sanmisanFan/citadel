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
  const viewerRef = useRef(null);

  const [numPages, setNumPages] = useState(null);
  const [width, setWidth] = useState(0);
  const [renderedPages, setRenderedPages] = useState({});

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
  };

  const onPageRenderSuccess = (pageNumber) => {
    setRenderedPages((prev) => ({
      ...prev,
      [pageNumber]: true,
    }));
  };

  // Function to apply highlights
  const applyHighlights = () => {
    if (!viewerRef.current) return;

    // Clear existing highlights to prevent duplication
    const existingHighlights = viewerRef.current.querySelectorAll(".highlight");
    existingHighlights.forEach((el) => el.remove());

    // Apply new highlights
    highlights.forEach(({ page, rect, color }) => {
      const pageElement = viewerRef.current.querySelector(
        `.react-pdf__Page[data-page-number="${page}"] .react-pdf__Page__textContent`
      );
      console.log('pageElement', pageElement, 'page', page);

      if (pageElement) {
        const highlightDiv = document.createElement("div");
        highlightDiv.className = "highlight";
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
    if (Object.keys(renderedPages).length === numPages) {
      applyHighlights();
    }
  }, [renderedPages, highlights]);

  useEffect(() => {
    if (viewerRef.current) {
      setWidth(viewerRef.current.offsetWidth);
    }
  }, []);

  return (
    <div
      ref={viewerRef}
      style={{
        height: "96vh", // Full viewport height
        //width: '100%',
        overflowY: "scroll", // Enable vertical scrolling
        //padding: "10px",
        borderRight: "1px solid #ddd",
        backgroundColor: "#f9f9f9",
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
            width={width*0.98}
            onRenderSuccess={() => onPageRenderSuccess(index + 1)}
          />
        ))}
      </Document>

    </div>
  );
};