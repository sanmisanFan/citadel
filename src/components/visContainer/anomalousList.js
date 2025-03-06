import { useEffect, useCallback, useState, useRef } from "react";
import { Card, Space, Flex, Badge, Tag } from 'antd';

import "./style.css";

export const AnomalousListCard = ({
  anomalous,
  anomalousColorScheme,
  activeHighlight,
  setActiveHighlight
}) => {
  const listRef = useRef(null);
  const itemRefs = useRef({});

  const handleCardClick = (id) => {
    //console.log(id);
    id === activeHighlight ? setActiveHighlight(null) : setActiveHighlight(id);
  };

 // Scroll active highlight into view
 useEffect(() => {
  if (activeHighlight && itemRefs.current[activeHighlight]) {
    itemRefs.current[activeHighlight].scrollIntoView({
      behavior: "smooth",
      block: "nearest",
    });
  }
}, [activeHighlight]);


  return(
    <Card
      ref={listRef}
      id="anomalousListContainer-card"
      size="small"
      title="Anomalous List"
      style={{
        width: '40.3%',
        display: "flex",
        flexDirection: "column",
        //flex: 1, // Ensures the Card itself stretches
        height: "100%", // Fills the parent container
      }}
      styles={{
        body: {
          height: "100%",
          overflowY: "scroll",
          position: "relative"
        },
      }}
      //className="custom-card"
    >
       {anomalous.map(e=>{
        const anomalousName = e.displayName;
        const anomalousCategoryName = e.category.displayName;
        const baseColor = anomalousColorScheme[e.name]['baseColor'];
        const categoryColor = anomalousColorScheme[e.name]['category'][e.category.name]['baseColor'];
        const boxColor = anomalousColorScheme[e.name]['category'][e.category.name]['boxColor'];
        const bgColor = activeHighlight === e.id && boxColor
        return(
          <Card
            key={'anomalous-list-element-key-'+e.id}
            id={'anomalous-list-element-'+e.id}
            size="small"
            style={{
              width: "100%",
              padding: 10,
              //marginTop: 5,
              marginBottom: 10,
              backgroundColor: bgColor
            }}
            onClick={() => handleCardClick(e.id)}
            ref={(el) => (itemRefs.current[e.id] = el)}
          >
            <Flex
              gap="small"
              align="center"
            >
              <b>Potential Anomalous:</b>
              <div>
              <span style={{
                color: baseColor
              }}>
                {anomalousName}
              </span> - <span style={{
                color: categoryColor
              }}>
                 {anomalousCategoryName}
              </span>
              
              </div>
            </Flex>
          </Card>
        );
      }
      )}
    </Card>
  );
};
