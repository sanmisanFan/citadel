import { useEffect, useCallback, useState, useRef } from "react";
import { Card } from 'antd';

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
        height: '96vh',
        padding: 10,
        //borderRight: '1px solid #dddddd'
      }}
    >
      {highlights.map(e=>
        <Card
          key={'highlight-card-container-key-'+e.id}
          id={'highlight-card-container-'+e.id}
          style={{
            width: "100%",
            marginTop: 10,
            marginBottom: 10,
            backgroundColor: activeHighlight === e.id && e.color
          }}
          onClick={() => handleCardClick(e.id)}
        >
          <h2>{e.redFlag.category}</h2>
          <p>{e.redFlag.type} ({e.glyph})</p>
          <p>{e.redFlag.explanation}</p>
        </Card>
      )}
    </div>
  );
}