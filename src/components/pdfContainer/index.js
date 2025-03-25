import { useEffect, useCallback, useState, useRef } from "react";
import { createRoot } from "react-dom/client";
import { pdfjs, Document, Page, Outline } from 'react-pdf';
//import { extractAndHighlightCitation } from "../../util/pdfUtil";

import { citationHighlight } from "../../util/annotationCtrl";

import { HighlightBbox } from "../issueComps/highlightBox";
import { SentenceAnnotation } from "../issueComps/sentenceAnnotate";
import { FloatingPanel } from "../issueComps/floatPanel";
import { ToolBar } from "./toolbar";

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
  citation,
  anomalous,
  anomalousColorScheme,
  sentenceAnnotationList,
  currentPage,
  setCurrentPage,
  activeHighlight,
  setActiveHighlight,
  setAnomalous
}) => {
  //const targetSentence = "understand the experience of people that were there [3]";
  const bboxHeightOffest = 0.005;
  const viewerRef = useRef(null);

  const [numPages, setNumPages] = useState(null);
  const [width, setWidth] = useState(0);
  const [pdfScale, setPdfScale] = useState(1);
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

  // Function to scroll to the corresponding page
  const scrollToPage = (pageNumber) => {
    if (!viewerRef.current) return;

    const pageElement = viewerRef.current.querySelector(
      `.react-pdf__Page[data-page-number="${pageNumber}"]`
    );

    if (pageElement) {
      pageElement.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  const applyHighlightsReact = () => {
    if (!viewerRef.current) return;
  
    const viewer = viewerRef.current;
    const pageElements = viewer.querySelectorAll(".react-pdf__Page");
  
    pageElements.forEach((pageElement) => {
      const textContentLayer = pageElement.querySelector(".react-pdf__Page__textContent");
  
      if (textContentLayer) {
        // Clear existing React Highlights
        const existingContainers = textContentLayer.querySelectorAll(".sentence-highlight-container");
        existingContainers.forEach((container) => container.remove());
  
        // Get the transformation scale from the text layer
        const { width: layerWidth, height: layerHeight } = textContentLayer.getBoundingClientRect();
        
        // Filter highlights for the current page
        sentenceAnnotationList
          .filter((highlight) => highlight.page === Number(pageElement.dataset.pageNumber))
          .forEach((highlight) => {
            // Convert normalized coordinates to pixel values
            const highlightX = highlight.bbox.x * layerWidth;
            const highlightY = highlight.bbox.y * layerHeight;
            const highlightWidth = highlight.bbox.width * layerWidth;
            const highlightHeight = (highlight.bbox.height + bboxHeightOffest) * layerHeight;
  
            // Create a container for the individual highlight
            const highlightContainer = document.createElement("div");
            highlightContainer.className = "sentence-highlight-container";
            highlightContainer.style.position = "absolute";
            highlightContainer.style.left = `${highlightX}px`;
            highlightContainer.style.top = `${highlightY}px`;
            highlightContainer.style.width = `${highlightWidth}px`;
            highlightContainer.style.height = `${highlightHeight}px`;
  
            // Mount the React Highlight component
            const root = createRoot(highlightContainer);
            root.render(
              <SentenceAnnotation
                issueID={highlight.issueID}
                issueName={highlight.issueName}
                issueCategory={highlight.issueCategory}
                baseColor={highlight.baseColor}
                boxColor={highlight.boxColor}
                activeHighlight={activeHighlight}
                anomalous={anomalous} // Pass the anomalous data
                citation={citation} // Pass the citation data
                onClick={(issueID) => setActiveHighlight(issueID)}
              />
            );
            // Append the highlight container to the text layer
            textContentLayer.appendChild(highlightContainer);
          });
      }
    });
  };

  useEffect(() => {
    // render anomalous highlight
    if (Object.keys(renderedPages).length === numPages) {
      //console.log("activeHighlight:", activeHighlight);
      setTimeout(() => {
        applyHighlightsReact();
       }, 100);
    }
  }, [renderedPages, sentenceAnnotationList, activeHighlight]);

  useEffect(() => {
    if (Object.keys(renderedPages).length === numPages) {
      setTimeout(() => {
       citationHighlight(
          viewerRef, 
          citation, 
          anomalous, 
          anomalousColorScheme,
          activeHighlight,
          setActiveHighlight
        );
      }, 100);
      
    }
  }, [renderedPages, citation, anomalous, activeHighlight]);

  useEffect(() => {
    if (activeHighlight !== null) {
      const selectedAnomalous = anomalous.find(e => e.id === activeHighlight);
      if (selectedAnomalous) {
        scrollToPage(selectedAnomalous.page);
      }
    }
  }, [activeHighlight, anomalous]);

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

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: '100vh',
        borderRight: "1px solid #ddd"
      }}
    >
      <ToolBar
        setPdfScale={setPdfScale}
        currentPage={currentPage}
      />
      <div
        ref={viewerRef}
        className="pdf-container"
        style={{
          
        }}
      >
        {/* Floating Panel */
        <FloatingPanel
          anomalous={anomalous}
          anomalousColorScheme={anomalousColorScheme}
          setAnomalous={setAnomalous}
        />}

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
              scale={pdfScale}
              renderAnnotationLayer={false}
              onRenderSuccess={() => onPageRenderSuccess(index + 1)}
            />
          ))}
        </Document>
      </div>
    </div>
  );
};