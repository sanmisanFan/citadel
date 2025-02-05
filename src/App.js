import { useState, useEffect, useCallback } from "react";
import { Col, Row, Spin} from 'antd';
import 'antd/dist/reset.css';
import './App.css';

/** React DOM Components */
import { PDFContainer } from "./components/pdfContainer";
import { VisContainer } from "./components/visContainer";

/** Import utilitie functions */
//EMPTY

/** Import TEST Data */
import testData from "./data/identifiedIssue.json";
import citationRaw from "./data/citation.json";

/** load test PDF - should be uploaded by user */
import samplePDF from "./data/test.pdf";

const issueScheme = {
  citation_issue: {
    themeColor: "rgba(221, 52, 151, 0.3)",
    glyph: {
      irrelevent_citation: 'IC'
    }
  },
  statistical_error: {
    themeColor: "rgba(255, 106, 0, 0.3)",
    glyph: {
      failed_statistical_tests: 'FST'
    },
  }
};

function App() {
  // global init
  const [pdfData, setPdfData] = useState(null);

  const [highlights, setHighlights] = useState([]);
  const [citation, setCitation] = useState([]);

  const [currentPage, setCurrentPage] = useState(1);
  const [activeHighlight, setActiveHighlight] = useState(null);

  /** init citation list */
  const initCitations = () => {
    const citationsList = JSON.parse(JSON.stringify(citationRaw.citations));
    setCitation(citationsList);
  };

  const initHighlights = () => {
    const issueListRaw = JSON.parse(JSON.stringify(testData.identifiedIssue));
    issueListRaw.forEach(e=>{
      const issueCategory = e.redFlag.category;
      const issueType = e.redFlag.type;
      const color = issueScheme[issueCategory].themeColor;
      const glyph = issueScheme[issueCategory].glyph[issueType];
      e.color = color;
      e.glyph = glyph;
    });
    //console.log(issueListRaw);
    setHighlights(issueListRaw);
  };

  useEffect(() => {
    setPdfData(samplePDF);
  }, []);

  useEffect(() => {
    initHighlights();
  }, []);

  useEffect(() => {
    initCitations();
  }, [citationRaw]);

  //const { Header, Content } = Layout;
  
  return (
    <div className="App">
      <div className="mainContainer">
          <Row>
            <Col span={14}>
              <PDFContainer
                file={pdfData}
                highlights={highlights}
                citation={citation}
                currentPage={currentPage}
                setCurrentPage={setCurrentPage}
              />
            </Col>
            <Col span={10}>
              <VisContainer
                highlights={highlights}
                currentPage={currentPage}
                activeHighlight={activeHighlight}
                setActiveHighlight={setActiveHighlight}
              />
            </Col>
          </Row>
      </div>
    </div>
  );
}

export default App;
