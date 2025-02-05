import { useEffect, useCallback, useState } from "react";
import { Card, Row, Col } from 'antd';

import "./style.css";

export const ContentCard = ({
  width,
  id,
  title,
  headComp=null
}) => {
  
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

    </Card>
  );
};