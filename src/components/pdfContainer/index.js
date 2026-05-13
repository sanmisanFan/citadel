import { useEffect, useCallback, useState, useRef } from "react";
import { createRoot } from "react-dom/client";
import { pdfjs, Document, Page } from 'react-pdf';

import { citationHighlight } from "../../util/annotationCtrl";
import {
  resolveAllAnchors,
  resolveAnomalyAnchor,
} from "../../util/anomalyAnchor";

import { SentenceAnnotation } from "../issueComps/sentenceAnnotate";
import { FloatingPanel } from "../issueComps/floatPanel";
import { ToolBar } from "./toolbar";

import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';
import './style.css';

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

export const PDFContainer = ({
  file,
  citation,
  anomalous,
  anomalousColorScheme,
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
  // onRenderSuccess (canvas-only) because anchor resolution walks the
  // text-layer spans — those may not exist yet when the canvas finishes.
  //
  // This callback must be reference-stable: react-pdf's TextLayer lists
  // onRenderSuccess in its layout-effect deps, so a fresh function instance
  // each parent re-render cancels the in-flight text-layer render and
  // restarts it.
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

  const handleScroll = useCallback(() => {
    if (!viewerRef.current) return;

    const viewer = viewerRef.current;
    const pageElements = Array.from(viewer.querySelectorAll(".react-pdf__Page"));
    const scrollTop = viewer.scrollTop;

    for (let i = 0; i < pageElements.length; i++) {
      const page = pageElements[i];
      const { offsetTop, clientHeight } = page;
      if (scrollTop >= offsetTop - clientHeight / 2 && scrollTop < offsetTop + clientHeight / 2) {
        setCurrentPage(i + 1);
        break;
      }
    }
  }, [setCurrentPage]);

  // Draw the secondary sentence underlines. Each underline is grouped per
  // (page, rect) so N anomalies that resolve to the same line render as
  // ONE element tagged with all N issue IDs — clicking cycles through
  // them on subsequent presses.
  const applySentenceUnderlinesReact = useCallback(() => {
    const viewer = viewerRef.current;
    if (!viewer) return;

    viewer.querySelectorAll(".sentence-highlight-container").forEach((c) => c.remove());

    const groups = resolveAllAnchors(anomalous, viewer);

    groups.forEach((group) => {
      const pageEl = viewer.querySelector(
        `.react-pdf__Page[data-page-number="${group.page}"]`
      );
      const textLayer = pageEl?.querySelector(".react-pdf__Page__textContent");
      if (!textLayer) return;

      const firstIssue = group.issues[0];
      const colorScheme = anomalousColorScheme[firstIssue.name];
      const categoryColors = colorScheme?.category?.[firstIssue.category.name] || {};
      const baseColor = categoryColors.baseColor;
      const boxColor = categoryColors.boxColor;

      const container = document.createElement("div");
      container.className = "sentence-highlight-container";
      container.style.position = "absolute";
      container.style.left = `${group.rect.x}px`;
      container.style.top = `${group.rect.y}px`;
      container.style.width = `${group.rect.width}px`;
      container.style.height = `${group.rect.height}px`;

      const issueIDs = group.issues.map((i) => i.id);
      const activeMatch = issueIDs.includes(activeHighlight);
      const displayIssueID = activeMatch ? activeHighlight : issueIDs[0];

      const root = createRoot(container);
      root.render(
        <SentenceAnnotation
          issueID={displayIssueID}
          issueName={firstIssue.displayName}
          issueCategory={firstIssue.category.displayName}
          baseColor={baseColor}
          boxColor={boxColor}
          activeHighlight={activeHighlight}
          onClick={() => {
            // Cycle: if the active one is in this group, pick the next; else
            // jump to the first. Keeps multi-anomaly markers reachable.
            const idx = issueIDs.indexOf(activeHighlight);
            const next = idx === -1 ? issueIDs[0] : issueIDs[(idx + 1) % issueIDs.length];
            setActiveHighlight(next);
          }}
        />
      );
      textLayer.appendChild(container);
    });
  }, [anomalous, anomalousColorScheme, activeHighlight, setActiveHighlight]);

  useEffect(() => {
    if (Object.keys(textLayerReadyPages).length === numPages) {
      const t = setTimeout(applySentenceUnderlinesReact, 100);
      return () => clearTimeout(t);
    }
  }, [textLayerReadyPages, numPages, applySentenceUnderlinesReact]);

  useEffect(() => {
    if (Object.keys(textLayerReadyPages).length === numPages) {
      const t = setTimeout(() => {
        citationHighlight(
          viewerRef,
          citation,
          anomalous,
          anomalousColorScheme,
          activeHighlight,
          setActiveHighlight
        );
      }, 100);
      return () => clearTimeout(t);
    }
  }, [textLayerReadyPages, numPages, citation, anomalous, anomalousColorScheme, activeHighlight, setActiveHighlight]);

  // Scroll-to-marker on card click. Walks the active anomaly's anchors
  // and resolves the first one that lands. Falls back to the page top.
  useEffect(() => {
    if (activeHighlight === null || !viewerRef.current) return;
    const selected = anomalous.find((e) => e.id === activeHighlight);
    if (!selected) return;

    const viewer = viewerRef.current;
    let resolved = null;
    for (const anchor of selected.anchors || []) {
      resolved = resolveAnomalyAnchor(anchor, viewer);
      if (resolved) break;
    }

    const targetPage = resolved?.page ?? selected.page;
    if (targetPage == null) return;

    const pageEl = viewer.querySelector(
      `.react-pdf__Page[data-page-number="${targetPage}"]`
    );
    if (!pageEl) return;

    if (resolved?.rects?.length) {
      const rect = resolved.rects[0];
      const viewerRect = viewer.getBoundingClientRect();
      const target = pageEl.offsetTop + rect.y - viewerRect.height / 3;
      viewer.scrollTo({ top: Math.max(target, 0), behavior: "smooth" });
    } else {
      pageEl.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [activeHighlight, anomalous, textLayerReadyPages]);

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
  }, [handleScroll]);

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
        style={{}}
      >
        <FloatingPanel
          anomalous={anomalous}
          anomalousColorScheme={anomalousColorScheme}
          setAnomalous={setAnomalous}
        />

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
