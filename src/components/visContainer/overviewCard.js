import { useEffect, useCallback, useState } from "react";
import { Card, Space, Flex, Badge, Tag } from 'antd';

import "./style.css";

export const OverviewCard = ({
  anomalous,
  author,
  venue
}) => {
  
  return(
    <Card
      id="overviewContainer-card"
      size="small"
      title="Information Overview"
      style={{
        width: '60%',
        display: "flex",
        flexDirection: "column",
        flex: 1, // Ensures the Card itself stretches
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
      size="middle"
        style={{ 
          flex: 1, 
          //background: "#e6f7ff", 
          padding: "10px"
        }}
      >
        <Flex
          gap="large"
          align="center"
        >
          <b>Most cited author:</b>
          <Badge count={5} size="small" offset={[5, 0]}><span id="author-2">Firstname Lastname</span></Badge>
          <Badge count={2} size="small" offset={[5, 0]}><span id="author-1">John Doe</span></Badge>
          <Badge status="success" dot="true" offset={[3, 2]}><span id="author-0">Fan Lei</span></Badge>
        </Flex>

        <Flex
          gap="large"
          align="center"
        >
          <b>Most cited venue:</b>
          <Badge count={3} size="small" offset={[5, 0]}><span id="venue-0">TVCG</span>[Journal]</Badge>
          <Badge count={2} size="small" offset={[5, 0]}><span id="author-1">CHI</span>[Conf]</Badge>
          <Badge count={2} size="small" offset={[5, 0]}><span id="author-1">VIS</span>[Conf]</Badge>
        </Flex>   

        <Flex
          gap="large"
          align="center"
        >
          <b>Citation time distribution:</b>
          <Flex
            gap="small"
            align="flex-end"
            style={{
              height: 50,
              width: 200,
              borderBottom: '1px solid #ddd',
            }}
          >
            <div style={{
              height: 50,
              width: 20,
              backgroundColor: '#999',
            }} />
             <div style={{
              height: 30,
              width: 20,
              backgroundColor: '#999',
            }} />
             <div style={{
              height: 20,
              width: 20,
              backgroundColor: '#999',
            }} />
            <div style={{
              height: 10,
              width: 20,
              backgroundColor: '#999',
            }} />
          </Flex>
        </Flex>

        <Flex
          gap="small"
          align="center"
        >
          <b>Detected Potential Anomalous:</b>

          <Tag bordered={false} color="magenta">
            Citation Low Relevancy
          </Tag>

          <Tag bordered={false} color="red">
            Retracted Citation
          </Tag>
        </Flex>    
      </Space>
    </Card>
  );
};