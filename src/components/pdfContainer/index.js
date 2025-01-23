import { useEffect, useCallback, useState, useRef } from "react";
import { createRoot } from "react-dom/client";
import { pdfjs, Document, Page, Outline } from 'react-pdf';
//import { extractTextFromPage, findSentenceCoordinates } from "../../util/pdfUtil";

import { HighlightBbox } from "../issueComps/issueHighLighter";
import { FloatingPanel } from "../issueComps/floatPanel";

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
  highlights,
  currentPage,
  setCurrentPage
}) => {
  //const targetSentence = "understand the experience of people that were there [3]";
  const bboxHeightOffest = 0.005;
  const viewerRef = useRef(null);

  const [numPages, setNumPages] = useState(null);
  const [width, setWidth] = useState(0);
  const [renderedPages, setRenderedPages] = useState({});


  /*const extractAndHighlight = async (pdf) => {
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
  };*/

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
  };

  const onPageRenderSuccess = (pageNumber) => {
    setRenderedPages((prev) => ({
      ...prev,
      [pageNumber]: true,
    }));
  };

  const handleScroll = () => {
    if (!viewerRef.current) return;

    const viewer = viewerRef.current;
    const pageElements = Array.from(viewer.querySelectorAll(".react-pdf__Page"));
    const scrollTop = viewer.scrollTop;

    // Find the first page that is at least partially visible
    for (let i = 0; i < pageElements.length; i++) {
      const page = pageElements[i];
      const { offsetTop, clientHeight } = page;
      if (scrollTop >= offsetTop - clientHeight / 2 && scrollTop < offsetTop + clientHeight / 2) {
        setCurrentPage(i + 1);
        break;
      }
    }
  };

  // Function to apply highlights
  /*const applyHighlights = () => {
    if (!viewerRef.current) return;

    // Clear existing highlights to prevent duplication
    const existingHighlights = viewerRef.current.querySelectorAll(".highlight");
    existingHighlights.forEach((el) => el.remove());

    // Apply new highlights
    highlights.forEach(({ page, bbox, color, id }) => {
      const pageElement = viewerRef.current.querySelector(
        `.react-pdf__Page[data-page-number="${page}"] .react-pdf__Page__textContent`
      );

      if (pageElement) {
        const highlightDiv = document.createElement("div");
        highlightDiv.id = "highlight-bbox-"+id;
        highlightDiv.className = "highlight";
        highlightDiv.style.position = "absolute";
        highlightDiv.style.left = `${bbox.x * 100}%`;
        highlightDiv.style.top = `${bbox.y * 100}%`;
        highlightDiv.style.width = `${bbox.width * 100}%`;
        highlightDiv.style.height = `${(bbox.height + bboxHeightOffest) * 100}%`;
        highlightDiv.style.backgroundColor = color || "yellow";
        highlightDiv.style.opacity = "0.3";

        pageElement.appendChild(highlightDiv);
      }
    });
  };*/

  const applyHighlightsReact = () => {
    if (!viewerRef.current) return;
  
    const viewer = viewerRef.current;
    const pageElements = viewer.querySelectorAll(".react-pdf__Page");
  
    pageElements.forEach((pageElement) => {
      const textContentLayer = pageElement.querySelector(".react-pdf__Page__textContent");
  
      if (textContentLayer) {
        // Clear existing React Highlights
        const existingContainers = textContentLayer.querySelectorAll(".react-highlight-container");
        existingContainers.forEach((container) => container.remove());
  
        // Get the transformation scale from the text layer
        const { width: layerWidth, height: layerHeight } = textContentLayer.getBoundingClientRect();
        
        // Filter highlights for the current page
        highlights
          .filter((highlight) => highlight.page === Number(pageElement.dataset.pageNumber))
          .forEach(({ id, bbox, color, glyph }) => {
            // Convert normalized coordinates to pixel values
            const highlightX = bbox.x * layerWidth;
            const highlightY = bbox.y * layerHeight;
            const highlightWidth = bbox.width * layerWidth;
            const highlightHeight = (bbox.height + bboxHeightOffest) * layerHeight;
  
            // Create a container for the individual highlight
            const highlightContainer = document.createElement("div");
            highlightContainer.className = "react-highlight-container";
            highlightContainer.style.position = "absolute";
            highlightContainer.style.left = `${highlightX}px`;
            highlightContainer.style.top = `${highlightY}px`;
            highlightContainer.style.width = `${highlightWidth}px`;
            highlightContainer.style.height = `${highlightHeight}px`;
  
            // Mount the React Highlight component
            const root = createRoot(highlightContainer);
            root.render(
              <HighlightBbox
                glyph={glyph}
                color={color}
                id={id}
                onClick={(highlightId) => console.log(highlightId)}
              />
            );
            // Append the highlight container to the text layer
            textContentLayer.appendChild(highlightContainer);
          });
      }
    });
  };

  useEffect(() => {
    if (Object.keys(renderedPages).length === numPages) {
      //applyHighlights();
      applyHighlightsReact();
    }
  }, [renderedPages, highlights]);

  useEffect(() => {
    if (viewerRef.current) {
      setWidth(viewerRef.current.offsetWidth);
    }
  }, []);

  useEffect(() => {
    const viewer = viewerRef.current;
    if (viewer) {
      viewer.addEventListener("scroll", handleScroll);
      return () => viewer.removeEventListener("scroll", handleScroll);
    }
  }, []);

  /*useEffect(() => {
    const loadAndExtract = async () => {
      const loadingTask = pdfjs.getDocument(file);
      const pdf = await loadingTask.promise;
      await extractAndHighlight(pdf);
    };
    loadAndExtract();
  }, [file]);*/

  return (
    <div
      ref={viewerRef}
      className="pdf-container"
      style={{
        borderRight: "1px solid #ddd"
      }}
    >
      {/* Floating Panel */}
      <FloatingPanel
        currentPage={currentPage}
      />
      {/* PDF Viewer */}
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
            width={width}
            scale={0.8}
            onRenderSuccess={() => onPageRenderSuccess(index + 1)}
          />
        ))}
      </Document>

    </div>
  );
};