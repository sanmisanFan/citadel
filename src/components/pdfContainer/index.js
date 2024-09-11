import { useEffect, useCallback, useState, useRef } from "react";

import { 
  PdfHighlighter,
  PdfLoader 
} from "react-pdf-highlighter-extended";

import { ToolBar } from "./toolbar";
import { ExpandableTip } from "./ExpandableTip";

export const PDFContainer = ({PDF_URL}) => {
  const [highlights, setHighlights] = useState([]);
  const [pdfScaleValue, setPdfScaleValue] = useState('page-width');
  const [highlightPen, setHighlightPen] = useState(false);


const getNextId = () => String(Math.random()).slice(2);

  /** Refs for PdfHighlighter utilities
   * These contain numerous helpful functions, such as scrollToHighlight,
   * getCurrentSelection, setTip, and many more
   */
  const highlighterUtilsRef = useRef();
  const resetHash = () => {
    document.location.hash = "";
  };

  const addHighlight = (highlight, comment) => {
    console.log("Saving highlight", highlight);
    setHighlights([{ ...highlight, comment, id: getNextId() }, ...highlights]);
  };

  return(
    <div
      style={{
        //backgroundColor: "#ffffff",
        //height: '94vh',
        width: '100%',
      }}
    >
      <ToolBar 
        setPdfScaleValue={setPdfScaleValue} 
      />
      <div
        style={{
          //backgroundColor: "#ffffff",
          height: '90vh',
          width: '100%',
        }}
      >
        <PdfLoader document={PDF_URL}>
        {(pdfDocument) => (
          <PdfHighlighter
            enableAreaSelection={(event) => event.altKey}
            pdfDocument={pdfDocument}
            utilsRef={(_pdfHighlighterUtils) => {
              highlighterUtilsRef.current = _pdfHighlighterUtils;
            }}
            pdfScaleValue={pdfScaleValue}
            highlights={highlights}
            selectionTip={highlightPen ? undefined : <ExpandableTip addHighlight={addHighlight} />}
            onScrollAway={resetHash}
            textSelectionColor={highlightPen ? "rgba(255, 226, 143, 1)" : undefined}
            onSelection={highlightPen ? (selection) => addHighlight(selection.makeGhostHighlight(), "") : undefined}
          >
            {console.log('pdfScaleValue', pdfScaleValue)}
            {/* User-defined HighlightContainer component goes here */}
          </PdfHighlighter>
        )}
      </PdfLoader>
      </div>
      
    </div>
  );
}