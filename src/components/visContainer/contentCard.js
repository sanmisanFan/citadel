import { useEffect, useCallback, useState } from "react";
import { Card, Row, Col } from 'antd';

import "./style.css";

export const ContentCard = ({
  width,
  id,
  title,
  activeHighlight,
  anomalous
}) => {
  //console.log(activeHighlight);
  return(
    <Card
      id={id}
      size="small"
      title={title}
      style={{
        width: width,
      }}
      //className="custom-card"
    >
    {JSON.stringify(anomalous.filter(e=>e.id === activeHighlight)[0])}
    </Card>
  );
};