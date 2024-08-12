import { useState, useEffect, useCallback } from "react";
import {Layout, Col, Row, Spin} from 'antd';
import 'antd/dist/reset.css';
import './App.css';

/** React DOM Components */
import { NavBar } from "./components/nav";

function App() {
  const { Header, Content } = Layout;
  
  return (
    <div className="App">
      <Layout className="mainContainer">
        <Header style={{height: 40}}>
          <NavBar />
        </Header>
      </Layout>
    </div>
  );
}

export default App;
