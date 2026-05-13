// https://sanmisanfan.github.io/ReviewerApp-demo/
import { useState } from "react";
import { pdfjs } from "react-pdf";
import { Col, Row, Spin, Upload, Input, Button, Typography, Divider, Card, Space, Alert, Modal, List } from 'antd';
import './App.css';
import { CloudUploadOutlined, FileTextOutlined, UserOutlined, CalendarOutlined, CheckCircleOutlined } from '@ant-design/icons';
import TextInputArray from "./components/textInputArray.js"

/** React DOM Components */
import { PDFContainer } from "./components/pdfContainer";
import { VisContainer } from "./components/visContainer";

/** Import annotation configure */
import { anomalousColorScheme } from "./annotationConfig";

const { Title, Text } = Typography;
const { Dragger } = Upload;

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

const BACKEND_URL = (process.env.BACKEND_URL) ? process.env.BACKEND_URL : "localhost:8000";

function App() {
    // global init
    const [pdfData, setPdfData] = useState(null);
    const [title, setTitle] = useState("");
    const [authors, setAuthors] = useState([""]);
    const [year, setYear] = useState("");
    const [authorsInitial, setAuthorsInitial] = useState(null);
    const [isExtractingMetadata, setIsExtractingMetadata] = useState(false);
    const [metadataExtractionError, setMetadataExtractionError] = useState(null);
    const [isProcessed, setIsProcessed] = useState(false);

    const [citation, setCitation] = useState([]);
    const [anomalous, setAnomalous] = useState([]);
    const [author, setAuthor] = useState([]);
    const [venue, setVenue] = useState([]);
    const [sentenceAnnotationList, setSentenceAnnotationList] = useState([]);
    const [authorGraph, setAuthorGraph] = useState(null);

    const [currentPage, setCurrentPage] = useState(1);
    const [activeHighlight, setActiveHighlight] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [progressStatus, setProgressStatus] = useState("");
    const [progressSteps, setProgressSteps] = useState([]);
    const [missingAbstracts, setMissingAbstracts] = useState([]);
    const [showMissingModal, setShowMissingModal] = useState(false);
    const [abstractPdfs, setAbstractPdfs] = useState({});

    const uploadPdf = (file) => {
        setPdfData(file);
        autoFillMetadata(file);
    };

    const autoFillMetadata = async (file) => {
        setMetadataExtractionError(null);
        setIsExtractingMetadata(true);
        try {
            const formData = new FormData();
            formData.append("file", file);
            const response = await fetch(`http://${BACKEND_URL}/api/extract_metadata`, {
                method: "POST",
                body: formData,
            });
            if (!response.ok) {
                throw new Error(`Status ${response.status}`);
            }
            const data = await response.json();
            if (data.title) setTitle(data.title);
            if (data.year !== null && data.year !== undefined) setYear(String(data.year));
            if (Array.isArray(data.authors) && data.authors.length > 0) {
                setAuthorsInitial(data.authors);
            }
        } catch (err) {
            console.error("Metadata extraction failed:", err);
            setMetadataExtractionError(
                "Couldn't auto-fill metadata — please enter it manually."
            );
        } finally {
            setIsExtractingMetadata(false);
        }
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

            // Handle progress messages
            if (data.type === "info") {
                setProgressStatus(data.msg);
                setProgressSteps(prev => [...prev, { msg: data.msg, time: new Date().toLocaleTimeString() }]);
                return;
            }

            // Handle backend error messages
            if (data.type === "error") {
                console.error("Backend error:", data.msg);
                setProgressStatus(`Error: ${data.msg}`);
                setIsProcessing(false);
                return;
            }

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
                        Array.isArray(citation.author) && citation.author.includes(author.id) && citation.has_issue
                    );
                });

                venueRaw.forEach(venue => {
                    venue.has_issue = citationsList.some(citation =>
                        citation.venue != null && citation.venue.includes(venue.id) && citation.has_issue
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
                            // Skip anomalies without a body location (e.g. Unreferenced).
                            if (page == null || !sentenceObj.sentence) {
                                return;
                            }
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
                setAuthorGraph(authorGraphRaw);

                // Track papers missing abstracts
                const papersWithoutAbstract = citationRaw
                    .filter(c => c.hop === 1 && !c.abstract)
                    .map(c => ({
                        id: c.id,
                        title: c.title,
                        cite_number: c.cite_number,
                        authors: c.author,
                    }));
                setMissingAbstracts(papersWithoutAbstract);

                setIsProcessing(false);
                setIsProcessed(true);

                // Show modal if there are missing abstracts
                if (papersWithoutAbstract.length > 0) {
                    setShowMissingModal(true);
                }
            }
        };

        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
            setIsProcessing(false);
            setProgressStatus("Connection error. Please try again.");
        };

        ws.onclose = (event) => {
            if (!isProcessed) {
                const reason = event.reason ? `: ${event.reason}` : "";
                setProgressStatus(`Connection closed${reason}`);
                setIsProcessing(false);
            }
        };
    };

    const handleSubmit = () => {
        setIsProcessing(true);
        setProgressStatus("Connecting to server...");
        setProgressSteps([]);
        onSubmit();
    };

    return (
        <div className="App">
            <div className="mainContainer">
                {!isProcessed && (
                    <div className="upload-page">
                        <div className="upload-container">
                            {/* Header */}
                            <div className="upload-header">
                                <Title level={1} className="brand-title">CITADEL</Title>
                                <Text type="secondary" className="brand-subtitle">
                                    Citation Analysis &amp; Anomaly Detection for Academic Papers
                                </Text>
                            </div>

                            {/* Main Upload Card */}
                            <Card className="upload-card" bordered={false}>
                                {/* Step 1: Upload PDF */}
                                <div className="upload-section">
                                    <div className="section-header">
                                        <Text strong className="section-number">1</Text>
                                        <Text strong className="section-title">Upload Manuscript</Text>
                                    </div>

                                    <Dragger
                                        className="pdf-dragger"
                                        multiple={false}
                                        accept=".pdf"
                                        showUploadList={false}
                                        beforeUpload={(file) => {
                                            uploadPdf(file);
                                            return false;
                                        }}
                                    >
                                        {pdfData ? (
                                            <div className="upload-success">
                                                <CheckCircleOutlined className="upload-success-icon" />
                                                <Text strong>{pdfData.name}</Text>
                                                <Text type="secondary" className="file-size">
                                                    {(pdfData.size / 1024 / 1024).toFixed(2)} MB
                                                </Text>
                                            </div>
                                        ) : (
                                            <div className="upload-prompt">
                                                <CloudUploadOutlined className="upload-icon" />
                                                <Text strong className="upload-text">
                                                    Drop your PDF here or click to browse
                                                </Text>
                                                <Text type="secondary" className="upload-hint">
                                                    Supports PDF files up to 50MB
                                                </Text>
                                            </div>
                                        )}
                                    </Dragger>
                                </div>

                                {/* Step 2: Paper Metadata */}
                                {pdfData && (
                                    <>
                                        <Divider className="section-divider" />
                                        <div className="metadata-section">
                                            <div className="section-header">
                                                <Text strong className="section-number">2</Text>
                                                <Text strong className="section-title">Paper Metadata</Text>
                                                {isExtractingMetadata && (
                                                    <Space size={6} style={{ marginLeft: 12 }}>
                                                        <Spin size="small" />
                                                        <Text type="secondary">Auto-filling from PDF…</Text>
                                                    </Space>
                                                )}
                                            </div>
                                            <Text type="secondary" style={{ display: "block", marginBottom: 12 }}>
                                                We pre-fill these from the PDF — review and edit if anything looks off.
                                            </Text>
                                            {metadataExtractionError && (
                                                <Alert
                                                    type="warning"
                                                    message={metadataExtractionError}
                                                    showIcon
                                                    style={{ marginBottom: 12 }}
                                                />
                                            )}

                                            <div className="form-grid">
                                                <div className="form-field">
                                                    <label className="field-label">
                                                        <FileTextOutlined /> Paper Title
                                                    </label>
                                                    <Input
                                                        size="large"
                                                        placeholder="Enter the full title of the paper"
                                                        value={title}
                                                        onChange={(e) => setTitle(e.currentTarget.value)}
                                                    />
                                                </div>

                                                <div className="form-field">
                                                    <label className="field-label">
                                                        <UserOutlined /> Authors
                                                    </label>
                                                    <TextInputArray
                                                        updateCallback={setAuthors}
                                                        unitName="Author"
                                                        initialValues={authorsInitial}
                                                    />
                                                </div>

                                                <div className="form-field form-field-year">
                                                    <label className="field-label">
                                                        <CalendarOutlined /> Publication Year
                                                    </label>
                                                    <Input
                                                        size="large"
                                                        placeholder="e.g., 2024"
                                                        value={year}
                                                        onChange={(e) => setYear(e.currentTarget.value)}
                                                        style={{ maxWidth: 150 }}
                                                    />
                                                </div>
                                            </div>
                                        </div>

                                        <Divider className="section-divider" />

                                        {/* Submit Section */}
                                        <div className="submit-section">
                                            {isProcessing ? (
                                                <div className="processing-state">
                                                    <Spin size="large" />
                                                    <div className="progress-info">
                                                        <Text strong className="progress-status">
                                                            {progressStatus}
                                                        </Text>
                                                        <div className="progress-steps">
                                                            {progressSteps.slice(-5).map((step, idx) => (
                                                                <div key={idx} className="progress-step">
                                                                    <CheckCircleOutlined className="step-icon" />
                                                                    <Text type="secondary" className="step-text">
                                                                        {step.msg}
                                                                    </Text>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </div>
                                                </div>
                                            ) : (
                                                <Button
                                                    type="primary"
                                                    size="large"
                                                    className="submit-button"
                                                    onClick={handleSubmit}
                                                    disabled={!title || !year || authors.every(a => !a)}
                                                >
                                                    Analyze Paper
                                                </Button>
                                            )}
                                        </div>
                                    </>
                                )}
                            </Card>

                            {/* Footer */}
                            <div className="upload-footer">
                                <Text type="secondary">
                                    CITADEL analyzes citation patterns, detects anomalies, and identifies potential issues in academic manuscripts.
                                </Text>
                            </div>
                        </div>
                    </div>
                )}

                {isProcessed && (
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
                                    authorGraphDataRaw={authorGraph}
                                />
                            </Col>
                        </Row>
                    </div>
                )}

                {/* Missing Abstracts Modal */}
                <Modal
                    title={
                        <Space>
                            <FileTextOutlined />
                            <span>Missing Abstracts</span>
                        </Space>
                    }
                    open={showMissingModal}
                    onCancel={() => setShowMissingModal(false)}
                    footer={[
                        <Button key="skip" onClick={() => setShowMissingModal(false)}>
                            Skip for Now
                        </Button>,
                        <Button
                            key="submit"
                            type="primary"
                            disabled={Object.keys(abstractPdfs).length === 0}
                            loading={isProcessing}
                            onClick={async () => {
                                setIsProcessing(true);
                                const formData = new FormData();
                                const citationIds = [];

                                // Add files and collect IDs
                                Object.entries(abstractPdfs).forEach(([citationId, file]) => {
                                    formData.append('files', file);
                                    citationIds.push(citationId);
                                });
                                formData.append('citation_ids', citationIds.join(','));

                                try {
                                    const response = await fetch(`http://${BACKEND_URL}/api/extract_abstracts`, {
                                        method: 'POST',
                                        body: formData,
                                    });

                                    if (response.ok) {
                                        const data = await response.json();
                                        console.log("Extracted abstracts:", data);

                                        // Update citations with new abstracts
                                        // (In a full implementation, you'd update the citation state here)
                                        alert(`Successfully extracted ${data.successful}/${data.total} abstracts!`);
                                    } else {
                                        const error = await response.json();
                                        alert(`Error: ${error.detail || 'Failed to extract abstracts'}`);
                                    }
                                } catch (err) {
                                    console.error("Extract error:", err);
                                    alert("Failed to connect to server. Is GROBID running?");
                                }

                                setIsProcessing(false);
                                setShowMissingModal(false);
                                setAbstractPdfs({});
                            }}
                        >
                            Extract Abstracts
                        </Button>
                    ]}
                    width={600}
                >
                    <div className="missing-abstracts-modal">
                        <Alert
                            message={`${missingAbstracts.length} referenced papers are missing abstracts`}
                            description="You can optionally upload PDFs for these papers to extract their abstracts. This will improve citation relevance analysis."
                            type="info"
                            showIcon
                            style={{ marginBottom: 16 }}
                        />
                        <List
                            className="missing-list"
                            dataSource={missingAbstracts}
                            renderItem={(paper) => (
                                <List.Item
                                    actions={[
                                        <Upload
                                            key="upload"
                                            accept=".pdf"
                                            showUploadList={false}
                                            beforeUpload={(file) => {
                                                setAbstractPdfs(prev => ({
                                                    ...prev,
                                                    [paper.id]: file
                                                }));
                                                return false;
                                            }}
                                        >
                                            <Button
                                                size="small"
                                                type={abstractPdfs[paper.id] ? "primary" : "default"}
                                            >
                                                {abstractPdfs[paper.id] ? "PDF Added" : "Add PDF"}
                                            </Button>
                                        </Upload>
                                    ]}
                                >
                                    <List.Item.Meta
                                        title={
                                            <Text className="missing-paper-title">
                                                [{paper.cite_number}] {paper.title?.substring(0, 60)}
                                                {paper.title?.length > 60 ? "..." : ""}
                                            </Text>
                                        }
                                    />
                                </List.Item>
                            )}
                        />
                    </div>
                </Modal>
            </div>
        </div>
    );
}

export default App;
