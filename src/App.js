import { useState, useEffect, useCallback } from "react";
import {Layout, Col, Row, Spin} from 'antd';
import 'antd/dist/reset.css';
import './App.css';

/** React DOM Components */
import { NavBar } from "./components/nav";
import { PDFContainer } from "./components/pdfContainer";
import { VisContainer } from "./components/visContainer";

/** Import utilitie functions */
//import { loadPDF } from "./util/pdfLoader";

/** load test PDF - should be uploaded by user */
import samplePDF from "./data/test.pdf";

const highlightsList = [
  {
    page: 1,
    rect: { x: 0.5, y: 0.5, width: 0.8, height: 0.1 }, // Normalized coordinates
    color: "rgba(255, 255, 0, 0.5)", // Highlight color
  },
  {
    page: 1,
    rect: { x: 0.1, y: 0.01, width: 0.5, height: 0.2 }, // Normalized coordinates
    color: "rgba(255, 106, 0, 0.5)", // Highlight color
  },
  {
    page: 2,
    rect: { x: 0.2, y: 0.4, width: 0.6, height: 0.2 },
    color: "rgba(0, 255, 0, 0.5)",
  },
];

function App() {
  // global init
  const [pdfData, setPdfData] = useState(null);
  const [highlights, setHighlights] = useState([]);

  useEffect(() => {
    setPdfData(samplePDF);
  }, []);

  useEffect(() => {
    setHighlights(highlightsList);
  }, []);

  const { Header, Content } = Layout;
  console.log('pdfData', pdfData);
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
