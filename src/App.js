// https://sanmisanfan.github.io/ReviewerApp-demo/
import { useState, useEffect, useCallback } from "react";
import { pdfjs } from "react-pdf";
//import pdfjsWorker from "pdfjs-dist/build/pdf.worker.entry";
import { Col, Row, Spin } from 'antd';
import 'antd/dist/reset.css';
import './App.css';

/** React DOM Components */
import { PDFContainer } from "./components/pdfContainer";
import { VisContainer } from "./components/visContainer";

/** Import utilitie functions */
import { extractAndHighlight } from "./util/pdfUtil";

/** Import annotation configure */
import { anomalousColorScheme } from "./annotationConfig";

/** Import TEST Data */
import authorRaw from "./data/case1/authors.json";
import venueRaw from "./data/case1/venues.json";
import citationRaw from "./data/case1/citation.json";
import anomalousRaw from "./data/case1/anomalous.json";
import authorGraphDataRaw from "./data/case1/community_graph.json";
//import authorGraphData from "./data/case1/author_graph.json";

/** load test PDF - should be uploaded by user */
import samplePDF from "./data/case1/reviewerAPP_case1.pdf";

/*pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();*/
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;


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
        const citationsList = JSON.parse(JSON.stringify(citationRaw.citations))
            .filter(e => e.hop === 1);

        citationsList.map(e => {
            e.cite_positions.filter(f => f.has_issue).length > 0 && (e.has_issue = true);
            return e;
        });

        const authorList = JSON.parse(JSON.stringify(authorRaw.authors));
        authorList.forEach(author => {
            author.has_issue = citationsList.some(citation =>
                citation.author.includes(author.id) && citation.has_issue
            );
        });

        const venueList = JSON.parse(JSON.stringify(venueRaw.venues));
        venueList.forEach(venue => {
            venue.has_issue = citationsList.some(citation =>
                citation.venue.includes(venue.id) && citation.has_issue
            );
        });

        console.log("citationsList", citationsList);
        console.log("authorList", authorList);
        console.log("venueList", venueList);

        setAuthor(authorList);
        setVenue(venueList);
        setCitation(citationsList);
    };

    /** init anomalous list */
    const initAnomalous = () => {
        const anomalousList = JSON.parse(JSON.stringify(anomalousRaw.identifiedIssue));
        anomalousList.map(e => e.filter = false);
        setAnomalous(anomalousList);
    };

    /** extract */
    const initSentenceHightlights = () => {
        const anomalousList = JSON.parse(JSON.stringify(anomalous));
        const _sentenceHighlights = [];
        anomalousList
            .filter(e => !e.filter) // Filter out anomalous with filter === true
            .forEach(e => {
                const issueID = e.id;
                const issueName = e.displayName;
                const issueCategory = e.category.displayName;
                const page = e.page;
                const baseColor = anomalousColorScheme[e.name]['category'][e.category.name]['baseColor'];
                const boxColor = anomalousColorScheme[e.name]['category'][e.category.name]['boxColor'];
                const sentenceList = e.sentence;

                // Derive the inline citation marker (e.g. "[21]") from the paper field.
                // Used as a disambiguation anchor when the same sentence appears on the page more than once.
                const citationMarker =
                    e.paper && e.paper.length > 0
                        ? (() => {
                            const cit = citation.find((c) => e.paper.includes(c.id));
                            return cit ? `[${cit.cite_number}]` : null;
                        })()
                        : null;

                sentenceList.forEach(sentenceObj => {
                    _sentenceHighlights.push({
                        issueID,
                        issueName,
                        issueCategory,
                        page,
                        baseColor,
                        boxColor,
                        sentence: sentenceObj.sentence,
                        citationMarker,
                    });
                });
            });
        setSentenceAnnotationList(_sentenceHighlights);
    };

    /** init author list */
    /*const initAuthor = () => {
      const authorList = JSON.parse(JSON.stringify(authorRaw.authors));
      setAuthor(authorList);
    };*/

    /** PDF file on load */
    useEffect(() => {
        setPdfData(samplePDF);
    }, []);

    /** load citation objects */
    useEffect(() => {
        initCitations();
    }, [citationRaw, authorRaw, venueRaw]);

    /** load detected anomalous */
    useEffect(() => {
        initAnomalous();
    }, [anomalousRaw]);

    useEffect(() => {
        anomalous.length > 0 && citation.length > 0 && initSentenceHightlights();
    }, [anomalous, citation]);

    return (
        <div className="App">
            <div className="mainContainer">
                <Row>
                    <Col span={14}>
                        {pdfData !== null && <PDFContainer
                            file={pdfData}
                            citation={citation}
                            anomalous={anomalous}
                            anomalousColorScheme={anomalousColorScheme}
                            sentenceAnnotationList={sentenceAnnotationList}
                            currentPage={currentPage}
                            setCurrentPage={setCurrentPage}
                            activeHighlight={activeHighlight}
                            setActiveHighlight={setActiveHighlight}
                            setAnomalous={setAnomalous}
                        />}
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
                            authorGraphDataRaw={authorGraphDataRaw}
                        />
                    </Col>
                </Row>
            </div>
        </div>
    );
}

export default App;
