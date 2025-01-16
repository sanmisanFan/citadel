import { useState, useEffect, useCallback } from "react";
import {Layout, Col, Row, Spin} from 'antd';
import 'antd/dist/reset.css';
import './App.css';

/** React DOM Components */
import { NavBar } from "./components/nav";
import { PDFContainer } from "./components/pdfContainer";
import { VisContainer } from "./components/visContainer";

/** Import utilitie functions */
import { loadPDF } from "./util/pdfLoader";

/** load test PDF - should be uploaded by user */
const PDF_URL = "https://arxiv.org/pdf/2203.11115"; //https://arxiv.org/pdf/2203.11115

function App() {
  // global init
  const [pdfData, setPdfData] = useState(null);
  const { Header, Content } = Layout;

  return (
    <div className="App">
      <Layout className="mainContainer">
        <Header style={{height: '43px'}}>
          <NavBar />
        </Header>
        <Content style={{
          backgroundColor: '#ffffff'
          //padding: 10
        }}>
          <Row>
            <Col span={13}>
              {/*<PDFContainer
                PDF_URL={PDF_URL}
              />*/}
              <div
                style={{
                  backgroundColor: "#9096a2",
                  height: '100%',
                }}
              ></div>
            </Col>
            <Col span={11}>
              <VisContainer />
            </Col>
          </Row>
        </Content>
      </Layout>
    </div>
  );
}

export default App;
