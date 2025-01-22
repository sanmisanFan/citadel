import { useEffect, useCallback, useState, useRef } from "react";

import {Layout, Col, Row, Spin} from 'antd';

export const VisContainer = () => {

  return(
    <div>
      <Row>
        <Col span={12}>
          <div
            style={{
              height: '95vh',
              borderRight: '1px solid #dddddd'
            }}
          ></div>
        </Col>
        <Col span={12}>
        <div
            style={{
              height: '100%',
            }}
          ></div></Col>
      </Row>
    </div>
  );
}