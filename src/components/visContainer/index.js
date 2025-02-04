import { useEffect, useCallback, useState, useRef } from "react";
import { Card, Alert } from 'antd';

export const VisContainer = ({
  highlights,
  currentPage,
  activeHighlight,
  setActiveHighlight
}) => {

  const handleCardClick = (id) => {
    id === activeHighlight ? setActiveHighlight(null) : setActiveHighlight(id);
  };
  //console.log('activeHighlight', activeHighlight);
  return(
    <div
      style={{
        height: '100vh',
        padding: 10,
        backgroundColor: '#ffffff'
        //borderRight: '1px solid #dddddd'
      }}
    >
      {highlights.map(e=>
        <Card
          key={'highlight-card-container-key-'+e.id}
          id={'highlight-card-container-'+e.id}
          size="small"
          style={{
            width: "100%",
            padding: 10,
            marginTop: 10,
            marginBottom: 10,
            backgroundColor: activeHighlight === e.id && e.color
          }}
          onClick={() => handleCardClick(e.id)}
        >
          <span>{e.redFlag.category}</span>
          {/*<p>{e.redFlag.type} ({e.glyph})</p>
          <p>{e.redFlag.explanation}</p>*/}
        </Card>
      )}
    </div>
  );
}