import { useState, useEffect, useCallback } from "react";
import {Layout, Col, Row, Spin} from 'antd';
import 'antd/dist/reset.css';
import './App.css';

/** React DOM Components */
import { NavBar } from "./components/nav";
import { PDFContainer } from "./components/pdfContainer";
import { VisContainer } from "./components/visContainer";

/** Import utilitie functions */

/** load test PDF - should be uploaded by user */
import samplePDF from "./data/test.pdf";

const highlightsList = [
  {
    page: 1,
    rect: { x: 0.1, y: 0.1, width: 0.1, height: 0.2 }, // Normalized coordinates
    color: "rgba(255, 255, 0, 0.5)", // Highlight color
  },
  {
    page: 1,
    rect: { x: 0.08811928104575163, y: 0.35267171717171714, width: 0.39718679757352937, height: 0.012579545454545454+0.005 }, // Normalized coordinates
    color: "rgba(255, 106, 0, 0.5)", // Highlight color
  },
  {
    page: 2,
    rect: { x: 0.2, y: 0.4, width: 0.5, height: 0.2 },
    color: "rgba(0, 255, 0, 0.5)",
  },
];

function App() {
  // global init
  const [pdfData, setPdfData] = useState(null);
  const [highlights, setHighlights] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    setPdfData(samplePDF);
  }, []);

  useEffect(() => {
    setHighlights(highlightsList);
  }, []);

  const { Header, Content } = Layout;
  //console.log('currentPage', currentPage);
  return (
    <div className="App">
      <Layout className="mainContainer">
        <Header style={{height: '43px'}}>
          <NavBar />
        </Header>
        <Content style={{
          backgroundColor: '#ffffff'
        }}>
          <Row>
            <Col span={16}>
              <PDFContainer
                file={pdfData}
                highlights={highlights}
                setCurrentPage={setCurrentPage}
              />
            </Col>
            <Col span={8}>
              <VisContainer />
            </Col>
          </Row>
        </Content>
      </Layout>
    </div>
  );
}

export default App;
