import { useLayoutEffect, useRef, useState } from "react";

import { usePdfHighlighterContext } from "react-pdf-highlighter-extended";

import "./expandableTip.css";

export const ExpandableTip = ({ addHighlight }) => {
  const [compact, setCompact] = useState(true);
  const selectionRef = useRef(null);

  const {
    getCurrentSelection,
    removeGhostHighlight,
    setTip,
    updateTipPosition,
  } = usePdfHighlighterContext();

  useLayoutEffect(() => {
    updateTipPosition();
  }, [compact]);

  return (
    <div className="Tip">
      {compact ? (
        <button
          className="Tip__compact"
          onClick={() => {
            setCompact(false);
            selectionRef.current = getCurrentSelection();
            selectionRef.current.makeGhostHighlight();
          }}
        >
          Add highlight
        </button>
      ) : (
        <div>COMMENT SET FORM</div>
      )}
    </div>
  );

}