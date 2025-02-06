import { useEffect, useCallback, useState } from "react";
import { Card, Space, Flex, Badge, Tag } from 'antd';

import "./style.css";

export const AnomalousListCard = ({
  anomalous,
  anomalousColorScheme,
  activeHighlight,
  setActiveHighlight
}) => {

  const handleCardClick = (id) => {
    //console.log(id);
    id === activeHighlight ? setActiveHighlight(null) : setActiveHighlight(id);
  };

  return(
    <Card
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
        display: "flex",
        flexDirection: "column",
        flex: 1, // Allows the body to expand
        overflow: "auto", // Enables scrolling if content is too large
      },
    }}
    //className="custom-card"
    >
      <Space 
      direction="vertical"
      size="small"
        style={{ 
          flex: 1, 
          padding: "10px"
        }}
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
              marginTop: 10,
              marginBottom: 10,
              backgroundColor: bgColor
            }}
            onClick={() => handleCardClick(e.id)}
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
      </Space>
    </Card>
  );
};