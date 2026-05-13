import { useEffect, useCallback, useState, useRef } from "react";
import { createRoot } from "react-dom/client";
import { pdfjs, Document, Page, Outline } from 'react-pdf';
import { findSentenceInTextLayer, findCitationAnchorSpan } from "../../util/pdfUtil";

import { citationHighlight } from "../../util/annotationCtrl";

import { HighlightBbox } from "../issueComps/highlightBox";
import { SentenceAnnotation } from "../issueComps/sentenceAnnotate";
import { FloatingPanel } from "../issueComps/floatPanel";
import { ToolBar } from "./toolbar";

import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';
import './style.css';

//import samplePDF from "../../data/test.pdf";

/*pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();*/
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

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
  const viewerRef = useRef(null);

  const [numPages, setNumPages] = useState(null);
  const [width, setWidth] = useState(0);
  const [pdfScale, setPdfScale] = useState(1);
  const [textLayerReadyPages, setTextLayerReadyPages] = useState({});

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
  };

  // Track when each page's text layer is fully rendered. We can't use
  // onRenderSuccess (canvas-only) because findSentenceInTextLayer walks the
  // text-layer spans — those may not exist yet when the canvas finishes.
  //
  // This callback must be reference-stable: react-pdf's TextLayer lists
  // onRenderSuccess in its layout-effect deps, so a fresh function instance
  // each parent re-render cancels the in-flight text-layer render and
  // restarts it. Combined with frequent re-renders from scroll
  // (setCurrentPage) and click (setActiveHighlight) state updates, that
  // produced thousands of "TextLayer task cancelled" warnings and prevented
  // highlights from being applied. We can't close over a per-page index
  // either; instead, on every text-layer completion we rescan the viewer
  // DOM and mark pages whose .react-pdf__Page__textContent has spans.
  const onPageTextLayerRenderSuccess = useCallback(() => {
    if (!viewerRef.current) return;
    const ready = {};
    viewerRef.current
      .querySelectorAll(".react-pdf__Page__textContent")
      .forEach((el) => {
        if (!el.querySelector("span")) return;
        const pageEl = el.closest(".react-pdf__Page");
        const num = Number(pageEl?.dataset.pageNumber);
        if (num) ready[num] = true;
      });
    setTextLayerReadyPages(ready);
  }, []);

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
        // Clear existing highlights
        textContentLayer
          .querySelectorAll(".sentence-highlight-container")
          .forEach((c) => c.remove());

        const pageNumber = Number(pageElement.dataset.pageNumber);

        sentenceAnnotationList
          .filter((highlight) => highlight.page === pageNumber)
          .forEach((highlight) => {
            // Find the citation marker span to use as disambiguation anchor.
            const anchorSpan = findCitationAnchorSpan(
              textContentLayer,
              highlight.citationMarker
            );

            // Auto-detect sentence position from the rendered text layer DOM.
            const rects = findSentenceInTextLayer(
              textContentLayer,
              highlight.sentence,
              anchorSpan
            );

            if (!rects.length) {
              console.warn(
                `[Highlight] Sentence not found on page ${pageNumber}:`,
                highlight.sentence
              );
              return;
            }

            rects.forEach((rect) => {
              const highlightContainer = document.createElement("div");
              highlightContainer.className = "sentence-highlight-container";
              highlightContainer.style.position = "absolute";
              highlightContainer.style.left = `${rect.x}px`;
              highlightContainer.style.top = `${rect.y}px`;
              highlightContainer.style.width = `${rect.width}px`;
              highlightContainer.style.height = `${rect.height}px`;

              const root = createRoot(highlightContainer);
              root.render(
                <SentenceAnnotation
                  issueID={highlight.issueID}
                  issueName={highlight.issueName}
                  issueCategory={highlight.issueCategory}
                  baseColor={highlight.baseColor}
                  boxColor={highlight.boxColor}
                  activeHighlight={activeHighlight}
                  anomalous={anomalous}
                  citation={citation}
                  onClick={(issueID) => setActiveHighlight(issueID)}
                />
              );
              textContentLayer.appendChild(highlightContainer);
            });
          });
      }
    });
  };

  useEffect(() => {
    // render anomalous highlight
    if (Object.keys(textLayerReadyPages).length === numPages) {
      //console.log("activeHighlight:", activeHighlight);
      setTimeout(() => {
        applyHighlightsReact();
       }, 100);
    }
  }, [textLayerReadyPages, sentenceAnnotationList, activeHighlight]);

  useEffect(() => {
    if (Object.keys(textLayerReadyPages).length === numPages) {
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
  }, [textLayerReadyPages, citation, anomalous, activeHighlight]);

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
              onRenderTextLayerSuccess={onPageTextLayerRenderSuccess}
            />
          ))}
        </Document>
      </div>
    </div>
  );
};