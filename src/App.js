import { useState, useEffect, useCallback } from "react";
import {Layout, Col, Row, Spin} from 'antd';
import 'antd/dist/reset.css';
import './App.css';

/** React DOM Components */
import { NavBar } from "./components/nav";
import { PDFContainer } from "./components/pdfContainer";
import { VisContainer } from "./components/visContainer";

/** Import utilitie functions */
//EMPTY

/** Import TEST Data */
import testData from "./data/test.json";

/** load test PDF - should be uploaded by user */
import samplePDF from "./data/test.pdf";

const issueScheme = {
  citation_issue: {
    themeColor: "rgb(221, 52, 151)",
    glyph: {
      irrelevent_citation: 'IC'
    }
  },
  statistical_error: {
    themeColor: "rgb(255, 106, 0)",
    glyph: {
      irrelevent_citation: 'FST'
    },
  }
};

function App() {
  // global init
  const [pdfData, setPdfData] = useState(null);
  const [highlights, setHighlights] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

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
