import { useState } from "react";

import "./toolbar.css";

export const ToolBar = ({ setPdfScale }) => {
  const [zoom, setZoom] = useState(null);
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
      <div className="ZoomControls">
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