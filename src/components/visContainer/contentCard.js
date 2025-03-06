import { useEffect, useCallback, useState } from "react";
import { Card, Row, Col, Descriptions, Tag, Space } from 'antd';

import "./style.css";

export const ContentCard = ({
  width,
  id,
  title,
  activeHighlight,
  anomalous,
  citation,
  author,
  venue
}) => {
  const selectedAnomalous = anomalous.find(e => e.id === activeHighlight);

  if (!selectedAnomalous) {
    return (
      <Card
        id={id}
        size="small"
        title={title}
        style={{
          width: width,
        }}
      >
        <p>No anomalous data found for the current selection.</p>
      </Card>
    );
  }

  // Extract relevant information from the selected anomalous object
  const { displayName, category, paper, page, explanation, sentence } = selectedAnomalous;

  // Function to format the authors, if available
  const formatAuthors = (authorIds) => {
    //console.log(author);
    if (!authorIds) return "N/A";

    const authorNames = authorIds.map(authorId => {
      const authorObj = author.find(a => a.id === authorId);
      //console.log("authorObj", authorObj, authorId);
      return authorObj ? `${authorObj.standardized_name}` : "Unknown Author";
    });
    return authorNames.join(", ");
  };
  
  // Function to format the venues, if available
  const formatVenue = (venueId) => {
    if (!venueId) return "N/A";

    const venueObj = venue.find(v => v.id === venueId);
    return venueObj ? `${venueObj.name} [${venueObj.type}]` : "Unknown Venue";
  };

  const citationInfo = paper && paper.length > 0 ? (
    paper.map((citationId, index) => {
      const citationObj = citation.find(c=>c.id===citationId);
      
      return (
        <div key={`citation-${index}`} style={{padding: 10}}>
          <Descriptions size="small" column={1}>
            <Descriptions.Item label={`Citation ${index+1} Author`}>
              {citationObj && formatAuthors(citationObj.author)}
            </Descriptions.Item>
            <Descriptions.Item label={`Citation ${index+1} Title`}>
              {citationObj && citationObj.title}
            </Descriptions.Item>
            <Descriptions.Item label={`Citation ${index+1} Venue`}>
              {citationObj && formatVenue(citationObj.venue)}
            </Descriptions.Item>
            <Descriptions.Item label={`Citation ${index+1} Year`}>
              {citationObj && citationObj.year}
            </Descriptions.Item>
            <Descriptions.Item label={`Citation ${index+1} DOI`}>
              {citationObj && citationObj.doi ? (<a href={citationObj.doi} target="_blank" rel="noopener noreferrer">{citationObj.doi}</a>) : 'N/A'}
            </Descriptions.Item>
            <Descriptions.Item label={`Citation ${index+1} Source`}>
            {citationObj && citationObj.source}
            </Descriptions.Item>
          </Descriptions>
        </div>
      );
    })
  ) : null;

  return (
    <Card
      id={id}
      size="small"
      title={title}
      style={{
        width: width,
        height: '100%'
      }}
    >
      <div style={{height: 'calc(100% - 60px)', overflowY: "auto",}}>
        <Descriptions size="small" column={1} bordered>
          <Descriptions.Item label="Anomalous Type">
            <Tag color="blue">{displayName}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Category">
            <Tag color="green">{category.displayName}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Page">
            {page}
          </Descriptions.Item>
          {citationInfo && (<Descriptions.Item label="Citation Information">
            {citationInfo}
          </Descriptions.Item>)}
          
          <Descriptions.Item label="Explanation">
            {explanation}
          </Descriptions.Item>
          {sentence.map((s, i) => (
            <Descriptions.Item key={i} label={`Sentence ${i + 1}`}>
              {s.sentence}
            </Descriptions.Item>
          ))}
        </Descriptions>
      </div>
    </Card>
  );
};
