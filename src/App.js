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

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

const BACKEND_URL = (process.env.BACKEND_URL) ? process.env.BACKEND_URL : "localhost:8000";

function App() {
    // global init
    const [pdfData, setPdfData] = useState(null);
    const [title, setTitle] = useState("");
    const [authors, setAuthors] = useState([""]);
    const [year, setYear] = useState("");
    const [isProcessed, setIsProcessed] = useState(false);

    const [citation, setCitation] = useState([]);
    const [anomalous, setAnomalous] = useState([]);
    const [author, setAuthor] = useState([]);
    const [venue, setVenue] = useState([]);
    const [sentenceAnnotationList, setSentenceAnnotationList] = useState([]);
    const [authorGraph, setAuthorGraph] = useState(null);

    const [currentPage, setCurrentPage] = useState(1);
    const [activeHighlight, setActiveHighlight] = useState(null);

    const uploadPdf = (file) => {
        setPdfData(file);
    };

    const onSubmit = () => {
        const ws = new WebSocket(`ws://${BACKEND_URL}/ws/process_pdf`);
        //TODO: add validation for each metadata field
        console.log(pdfData, title, authors, year);

        ws.onopen = () => {
            ws.send(JSON.stringify({
                title,
                authors,
                year,

            }));

            ws.send(JSON.stringify({
                filename: pdfData.name,
                mime_type: pdfData.type,
                size: pdfData.size,
            }));

            pdfData.arrayBuffer().then((buffer) => {
                ws.binaryType = "arraybuffer";
                ws.send(buffer);
            });
        };

        ws.onmessage = (e) => {
            const data = JSON.parse(e.data);
            console.log(data);
            //TODO: make sure this works properly
            if (data !== null && data.type === "end") {
                const results = data.results;

                const citationRaw = results.citations;
                const authorRaw = results.authors;
                const venueRaw = results.venues;
                const anomalousRaw = results.anomalous;
                const authorGraphRaw = results.authorGraph;

                const citationsList = citationRaw.filter(e => e.hop === 1 && e.has_issue);

                authorRaw.forEach(author => {
                    author.has_issue = citationsList.some(citation =>
                        citation.author.includes(author.id) && citation.has_issue
                    );
                });

                venueRaw.forEach(venue => {
                    venue.has_issue = citationsList.some(citation =>
                        citation.venue.includes(venue.id) && citation.has_issue
                    );
                });

                console.log("citationsList", citationsList);
                console.log("authorList", authorRaw);
                console.log("venueList", venueRaw);

                const anomalousList = anomalousRaw.identifiedIssue;
                anomalousList.map(e => e.filter = false);


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
                            console.log(`Adding highlight: ${issueID}, page ${page}, sentence: "${sentenceObj.sentence?.substring(0, 50)}..."`);
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
                setAnomalous(anomalousList);
                setAuthor(authorRaw);
                setVenue(venueRaw);
                setCitation(citationsList);
                setSentenceAnnotationList(_sentenceHighlights);
                // not sure what author graph is needed here...
                setAuthorGraph(authorGraphRaw);
                setIsProcessed(true);
            }
        };
    };
    //TODO: add labels around fields, fix antd CSS
    return (
        <div className="App">
            <div className="mainContainer">
                {!isProcessed && <Flex vertical gap="medium" align="center">
                    <h1>CITADEL</h1>
                    <Upload className="pdf_upload" multiple={false} action={uploadPdf}>
                        <Flex vertical align="center">
                            <p>
                                <InboxOutlined />
                            </p>
                            <p>Please upload a PDF. Click here or drag a file to upload.</p>
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
                </Flex>}
                {isProcessed && <div className="mainContainer">
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
                                authorGraphDataRaw={authorGraph}
                            />
                        </Col>
                    </Row>
                </div>}
            </div>
        </div >
    );
}

export default App;
