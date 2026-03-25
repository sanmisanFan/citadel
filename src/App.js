// https://sanmisanfan.github.io/ReviewerApp-demo/
import { useState, useEffect } from "react";
import { pdfjs } from "react-pdf";
import { Col, Row, Spin, Flex, Upload, Input, Button } from 'antd';
import './App.css';
import { InboxOutlined } from '@ant-design/icons';
import TextInputArray from "./components/textInputArray.js"

/** React DOM Components */
import { PDFContainer } from "./components/pdfContainer";
import { VisContainer } from "./components/visContainer";

/** Import annotation configure */
import { anomalousColorScheme } from "./annotationConfig";

/** Import TEST Data 
import authorRaw from "./data/case1/authors.json";
import venueRaw from "./data/case1/venues.json";
import citationRaw from "./data/case1/citation.json";
import anomalousRaw from "./data/case1/anomalous.json";
import authorGraphDataRaw from "./data/case1/community_graph.json";

// load test PDF - should be uploaded by user 
import samplePDF from "./data/case1/reviewerAPP_case1.pdf";
*/

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;


function App() {
    // global init
    const [pdfData, setPdfData] = useState(null);
    const [title, setTitle] = useState("");
    const [authors, setAuthors] = useState([""]);
    const [year, setYear] = useState("");

    const [citation, setCitation] = useState([]);
    const [anomalous, setAnomalous] = useState([]);
    const [author, setAuthor] = useState([]);
    const [venue, setVenue] = useState([]);
    const [sentenceAnnotationList, setSentenceAnnotationList] = useState([]);

    const [currentPage, setCurrentPage] = useState(1);
    const [activeHighlight, setActiveHighlight] = useState(null);

    const uploadPdf = (file) => {
        setPdfData(file);
    };

    const onSubmit = () => {
        //TODO: add validation for each metadata field
        console.log(pdfData, title, authors, year);
    };

    /** init citation list */
    /*const initCitations = () => {
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

    const initAnomalous = () => {
        const anomalousList = JSON.parse(JSON.stringify(anomalousRaw.identifiedIssue));
        anomalousList.map(e => e.filter = false);
        setAnomalous(anomalousList);
    };

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

    useEffect(() => {
        setPdfData(samplePDF);
    }, []);

    useEffect(() => {
        initCitations();
    }, [citationRaw, authorRaw, venueRaw]);

    useEffect(() => {
        initAnomalous();
    }, [anomalousRaw]);

    useEffect(() => {
        anomalous.length > 0 && citation.length > 0 && initSentenceHightlights();
    }, [anomalous, citation]);
    */

    return (
        <div className="App">
            <div className="mainContainer">
                <Flex vertical gap="medium" align="center">
                    <h1>CITADEL</h1>
                    <Upload className="pdf_upload" multiple={false} action={uploadPdf}>
                        <Flex vertical align="center">
                            <p>
                                <InboxOutlined />
                            </p>
                            <p>Please upload a PDF. Click or drag a file to upload.</p>
                        </Flex>
                    </Upload>
                    {pdfData != null &&
                        <Flex vertical gap="medium" align="center">
                            <p>Please fill out the following fields:</p>
                            <Input placeholder="Paper title" onChange={(e) => setTitle(e.currentTarget.value)} />
                            <TextInputArray updateCallback={setAuthors} unitName={"author"} />
                            <Input placeholder="Year" onChange={(e) => setYear(e.currentTarget.value)} />
                            <Button onClick={onSubmit}>Submit</Button>
                        </Flex>
                    }
                </Flex>
            </div>
            {/*<div className="mainContainer">
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
            </div>*/}
        </div >
    );
}

export default App;
