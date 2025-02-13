import { useState, useEffect, useCallback } from "react";
import { pdfjs } from "react-pdf";
import { Col, Row, Spin} from 'antd';
import 'antd/dist/reset.css';
import './App.css';

/** React DOM Components */
import { PDFContainer } from "./components/pdfContainer";
import { VisContainer } from "./components/visContainer";

/** Import utilitie functions */
import { extractAndHighlightCitation } from "./util/pdfUtil";

/** Import TEST Data */
import testData from "./data/identifiedIssue.json";
import authorRaw from "./data/author.json";
import venueRaw from "./data/venue.json";
import citationRaw from "./data/citation.json";
import anomalousRaw from "./data/anomalous.json";

/** load test PDF - should be uploaded by user */
import samplePDF from "./data/testpaper.pdf";

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

const anomalousColorScheme = {
  citation: {
    baseColor: "rgba(197,27,138,1)",
    boxColor: "rgba(197,27,138,0.3)",
    annotationCss: "rgba(197,27,138,0.3)",
    category: {
      lowRelevancy: {
        baseColor: "rgba(247,104,161,1)",
        boxColor: "rgba(247,104,161,0.3)",
        annotationCss: "linear-gradient(135deg, rgba(197,27,138,0.5) 50%, rgba(247,104,161,0.5) 50%)",
        divCss: "linear-gradient(135deg, rgba(197,27,138,1) 50%, rgba(247,104,161,1) 50%)"
      },
      retractedPaper: {
        baseColor: "rgba(251,180,185,1)",
        boxColor: "rgba(251,180,185,0.3)",
        annotationCss: "linear-gradient(135deg, rgba(197,27,138,0.5) 50%, rgba(251,180,185,0.5) 50%)",
        divCss: "linear-gradient(135deg, rgba(197,27,138,1) 50%, rgba(251,180,185,1) 50%)",
      }
    }
  },
  statistic: {
    baseColor: "rgba(217,95,14,1)",
    boxColor: "rgba(217,95,14,0.3)",
    annotationCss: "rgba(217,95,14,0.3)",
    category: {
      testFailure: {
        baseColor: "rgba(254,196,79,1)",
        boxColor: "rgba(254,196,79,0.3)",
        annotationCss: "linear-gradient(135deg, rgba(217,95,14,0.3) 50%, rgba(254,196,79,0.3) 50%)",
        divCss: "linear-gradient(135deg, rgba(217,95,14,1) 50%, rgba(254,196,79,1) 50%)"
      },
      valueInconsistency: {
        baseColor: "rgba(255,247,188,1)",
        boxColor: "rgba(255,247,188,0.3)",
        annotationCss: "linear-gradient(135deg, rgba(217,95,14,0.3) 50%, rgba(255,247,188,0.3) 50%)",
        divCss: "linear-gradient(135deg, rgba(217,95,14,1) 50%, rgba(255,247,188,1) 50%)"
      }
    }
  },
  other: {} // other anomalous such as the figure that has never been referenced
};

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

function App() {
  // global init
  const [pdfData, setPdfData] = useState(null);

  const [highlights, setHighlights] = useState([]);
  const [citation, setCitation] = useState([]);
  const [anomalous, setAnomalous] = useState([]);
  const [author, setAuthor] = useState([]);
  const [venue, setVenue] = useState([]);
  const [sentenceAnnotationList, setSentenceAnnotationList] = useState([]);

  const [currentPage, setCurrentPage] = useState(1);
  const [activeHighlight, setActiveHighlight] = useState(null);

  /** init citation list */
  const initCitations = () => {
    const citationsList = JSON.parse(JSON.stringify(citationRaw.citations));
    setCitation(citationsList);
  };

  const loadAndExtract = async (sentence, page) => {
    const loadingTask = pdfjs.getDocument(pdfData);
    const pdf = await loadingTask.promise;
    //await extractAndHighlight(pdf, "[14]");
    return await extractAndHighlightCitation(pdf, sentence, page);
  };

  /** init anomalous list */
  const initAnomalous = () => {
    const anomalousList = JSON.parse(JSON.stringify(anomalousRaw.identifiedIssue));
    const _sentenceHighlights = [];
    anomalousList.forEach(e=>{
      const issueID = e.id;
      const issueName = e.displayName;
      const issueCategory = e.category.displayName;
      const page = e.page;
      const baseColor = anomalousColorScheme[e.name]['category'][e.category.name]['baseColor'];
      const boxColor = anomalousColorScheme[e.name]['category'][e.category.name]['boxColor'];
      // construct sentence highlight object
      const sentenceHighlight = {
        issueID: issueID,
        issueName: issueName,
        issueCategory: issueCategory,
        baseColor: baseColor,
        boxColor: boxColor,
      };
      e.sentence.forEach((se, se_index)=>{
        const sentenceCoords = loadAndExtract(se, page);
        sentenceCoords.length > 0 && console.log(se_index, se, sentenceCoords)
        
      });

    });
    setAnomalous(anomalousList);
  };

  /** init author list */
  const initAuthor = () => {
    const authorList = JSON.parse(JSON.stringify(authorRaw.authors));
    setAuthor(authorList);
  };

   /** init author list */
   const initVenue = () => {
    const venueList = JSON.parse(JSON.stringify(venueRaw.venues));
    setVenue(venueList);
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

  useEffect(() => {
    pdfData !== null && initAnomalous();
  }, [anomalousRaw, pdfData]);

  useEffect(() => {
    initAuthor();
  }, [authorRaw]);

  useEffect(() => {
    initVenue();
  }, [venueRaw]);

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
                anomalous={anomalous}
                anomalousColorScheme={anomalousColorScheme}
                currentPage={currentPage}
                setCurrentPage={setCurrentPage}
                activeHighlight={activeHighlight}
                setActiveHighlight={setActiveHighlight}
              />
            </Col>
            <Col span={10}>
              <VisContainer
                file={pdfData}
                citation={citation}
                author={author}
                venue={venue}
                anomalous={anomalous}
                anomalousColorScheme={anomalousColorScheme}
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
