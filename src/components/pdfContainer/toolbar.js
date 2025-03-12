import { useState } from "react";

import "./toolbar.css";

export const ToolBar = ({ setPdfScale, currentPage }) => {
  const [zoom, setZoom] = useState(1);
  const [isHighlightPen, setIsHighlightPen] = useState(false);

  const zoomIn = () => {
    if (zoom) {
      if (zoom < 4) {
        setPdfScale(zoom + 0.1);
        setZoom(zoom + 0.1);
      }
    } else {
      setPdfScale(1);
      setZoom(1);
    }
  };

  const zoomOut = () => {
    if (zoom) {
      if (zoom > 0.2) {
        setPdfScale(zoom - 0.1);
        setZoom(zoom - 0.1);
      }
    } else {
      setPdfScale(1);
      setZoom(1);
    }
  };

  return (
    <div className="Toolbar">
      <span href="#">
        <b>ReviewerAPP</b>
      </span>
      <div className="ZoomControls">
        <span style={{marginRight: 20}}><b>Page: {currentPage}</b></span>
        <button title="Zoom in" onClick={zoomIn}>+</button>
        <button title="Zoom out" onClick={zoomOut}>-</button>
        {zoom ? `${(zoom * 100).toFixed(0)}%` : "Auto"}
      </div>
      {/*<button title="Highlight" className={`HighlightButton ${isHighlightPen ? 'active' : ''}`} onClick={() => {
        toggleHighlightPen();
        setIsHighlightPen(!isHighlightPen);
      }}>Toggle Highlights</button>*/}
    </div>
  );
}