import { useState, useEffect, useCallback } from "react";
import { pdfjs } from "react-pdf";
import { Col, Row, Spin} from 'antd';
import 'antd/dist/reset.css';
import './App.css';

/** React DOM Components */
import { PDFContainer } from "./components/pdfContainer";
import { VisContainer } from "./components/visContainer";

/** Import utilitie functions */
import { extractAndHighlight } from "./util/pdfUtil";

/** Import TEST Data */
import authorRaw from "./data/author.json";
import venueRaw from "./data/venue.json";
import citationRaw from "./data/citation.json";
import anomalousRaw from "./data/anomalous.json";

/** load test PDF - should be uploaded by user */
import samplePDF from "./data/testpaper.pdf";

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

  const loadAndExtract = async (sentenceList, page) => {
    const loadingTask = pdfjs.getDocument(pdfData);
    const pdf = await loadingTask.promise;
    return await extractAndHighlight(pdf, sentenceList, page);
  };

  /** init anomalous list */
  const initAnomalous = () => {
    const anomalousList = JSON.parse(JSON.stringify(anomalousRaw.identifiedIssue));
    setAnomalous(anomalousList);
  };

  /** extract */
  const initSentenceHightlights = () => {
    const anomalousList = JSON.parse(JSON.stringify(anomalousRaw.identifiedIssue));
    const _sentenceHighlights = [];
    anomalousList.forEach(e=>{
      const issueID = e.id;
      const issueName = e.displayName;
      const issueCategory = e.category.displayName;
      const page = e.page;
      const baseColor = anomalousColorScheme[e.name]['category'][e.category.name]['baseColor'];
      const boxColor = anomalousColorScheme[e.name]['category'][e.category.name]['boxColor'];
      const sentenceList = e.sentence;
      // construct sentence highlight object
      sentenceList.forEach(sentenceObj=>{
        const sentenceHighlight = {
          issueID: issueID,
          issueName: issueName,
          issueCategory: issueCategory,
          page: page,
          baseColor: baseColor,
          boxColor: boxColor,
          sentence: sentenceObj.sentence,
          bbox: sentenceObj.bbox
        };
        _sentenceHighlights.push(sentenceHighlight);
      });
    });
    setSentenceAnnotationList(_sentenceHighlights);
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

  useEffect(() => {
    setPdfData(samplePDF);
  }, []);

  useEffect(() => {
    initCitations();
  }, [citationRaw]);

  useEffect(() => {
    initAnomalous();
  }, [anomalousRaw]);

  useEffect(() => {
    initSentenceHightlights();
  }, [anomalousRaw]);

  useEffect(() => {
    initAuthor();
  }, [authorRaw]);

  useEffect(() => {
    initVenue();
  }, [venueRaw]);

  //const { Header, Content } = Layout;
  //console.log("activeHighlight", activeHighlight);
  return (
    <div className="App">
      <div className="mainContainer">
          <Row>
            <Col span={14}>
              <PDFContainer
                file={pdfData}
                citation={citation}
                anomalous={anomalous}
                anomalousColorScheme={anomalousColorScheme}
                sentenceAnnotationList={sentenceAnnotationList}
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
