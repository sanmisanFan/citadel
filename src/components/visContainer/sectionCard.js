import { useEffect, useCallback, useState } from "react";
import { Card, Row, Col } from 'antd';

import "./style.css";

export const SectionCard = ({
  sections
}) => {
  //console.log(sections);
  return(
    <Card
      id='sectionContainer-card'
      size="small"
      title='Section Overview'
      style={{
        width: '40%',
      }}
      //className="custom-card"
    >
      <div
        style={{
          height: 250,
          overflowY: 'auto'
        }}
      >
      <ul style={{ listStyle: "none", padding: 0 }}>
        {sections.map((section, index) => (
          <li
            key={index}
            style={{
              padding: "10px",
              borderBottom: "1px solid #ddd",
              cursor: section.page ? "pointer" : "default",
              color: section.page ? "black" : "#aaa",
            }}
            //onClick={() => section.page && scrollToPage(section.page)}
          >
            {section.title} {section.page ? `(Page ${section.page})` : "(Page Unknown)"}
          </li>
        ))}
      </ul>
      </div>
    </Card>
  );
};