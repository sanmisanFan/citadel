import { useEffect, useCallback, useState } from "react";
import { Card, Row, Col, Descriptions, Tag, Space, Alert, Typography } from 'antd';
import { LinkOutlined, UserOutlined, WarningOutlined } from '@ant-design/icons';

import "./style.css";

const { Text } = Typography;

export const ContentCard = ({
  width,
  id,
  title,
  activeHighlight,
  anomalous,
  citation,
  author,
  venue,
  anomalousColorScheme,
  mainPaperAuthors  // Authors of the paper being reviewed
}) => {
  const selectedAnomalous = anomalous.find(e => e.id === activeHighlight);
  const baseColor = anomalousColorScheme[selectedAnomalous.name]['baseColor'];
  const categoryColor = anomalousColorScheme[selectedAnomalous.name]['category'][selectedAnomalous.category.name]['baseColor'];
  const boxColor = anomalousColorScheme[selectedAnomalous.name]['category'][selectedAnomalous.category.name]['boxColor'];
  const bgColor = activeHighlight === selectedAnomalous.id && boxColor;

  if (!selectedAnomalous) {
    return (
      <Card
        id={id}
        size="small"
        //title={title}
        style={{
          width: width,
        }}
      >
        <p>No anomalous data found for the current selection.</p>
      </Card>
    );
  }

  // Extract relevant information from the selected anomalous object
  const { displayName, category, paper, page, explanation } = selectedAnomalous;

  // Function to format the authors, if available
  const formatAuthors = (authorIds) => {
    if (!authorIds) return "N/A";

    const authorNames = authorIds.map(authorId => {
      const authorObj = author.find(a => a.id === authorId);
      return authorObj ? `${authorObj.standardized_name}` : "Unknown Author";
    });
    return authorNames.join(", ");
  };

  // Find overlapping authors between citation and main paper for self-citation detection
  const findOverlappingAuthors = (citationAuthorIds) => {
    if (!citationAuthorIds || !mainPaperAuthors) return [];

    const overlapping = [];
    citationAuthorIds.forEach(authorId => {
      if (mainPaperAuthors.includes(authorId)) {
        const authorObj = author.find(a => a.id === authorId);
        if (authorObj) {
          overlapping.push(authorObj.standardized_name);
        }
      }
    });
    return overlapping;
  };

  // Generate relationship explanation
  const getRelationshipInfo = (citationObj) => {
    if (!citationObj) return null;

    const isSelfCitation = category.options?.selfCitation;
    const isCitationRing = category.options?.citationRing;
    const overlappingAuthorIds = category.options?.overlappingAuthorIds || [];

    if (isSelfCitation) {
      // Use overlapping author IDs from backend if available, otherwise try to find them
      let overlappingNames = [];
      if (overlappingAuthorIds.length > 0) {
        overlappingNames = overlappingAuthorIds.map(authorId => {
          const authorObj = author.find(a => a.id === authorId);
          return authorObj ? authorObj.standardized_name : authorId;
        });
      } else {
        overlappingNames = findOverlappingAuthors(citationObj.author);
      }

      return {
        type: 'self-citation',
        message: `This paper shares ${overlappingNames.length || 'some'} author(s) with your manuscript`,
        authors: overlappingNames,
        color: '#eb2f96'
      };
    }

    if (isCitationRing) {
      return {
        type: 'citation-ring',
        message: 'Authors of this paper show unusually high mutual citation patterns',
        color: '#722ed1'
      };
    }

    return null;
  };
  
  // Function to format the venues, if available
  const formatVenue = (venueId) => {
    if (!venueId) return "N/A";

    const venueObj = venue.find(v => v.id === venueId);
    return venueObj ? `${venueObj.standardized_name}` : "Unknown Venue";
  };

  const citationInfo = paper && paper.length > 0 ? (
    paper.map((citationId, index) => {
      const citationObj = citation.find(c=>c.id===citationId);
      const relationshipInfo = citationObj ? getRelationshipInfo(citationObj) : null;

      return (
        <div key={`citation-${index}`} style={{padding: 5}}>
          {/* Relationship Alert */}
          {relationshipInfo && (
            <Alert
              type={relationshipInfo.type === 'self-citation' ? 'warning' : 'info'}
              showIcon
              icon={relationshipInfo.type === 'self-citation' ? <UserOutlined /> : <LinkOutlined />}
              style={{ marginBottom: 12 }}
              message={
                <Text strong style={{ color: relationshipInfo.color }}>
                  {relationshipInfo.type === 'self-citation' ? 'Self-Citation Detected' : 'Citation Ring Pattern'}
                </Text>
              }
              description={
                <div>
                  <Text>{relationshipInfo.message}</Text>
                  {relationshipInfo.authors && relationshipInfo.authors.length > 0 && (
                    <div style={{ marginTop: 8 }}>
                      <Text type="secondary">Shared authors: </Text>
                      {relationshipInfo.authors.map((name, i) => (
                        <Tag key={i} color="magenta" style={{ margin: 2 }}>{name}</Tag>
                      ))}
                    </div>
                  )}
                </div>
              }
            />
          )}

          <Descriptions size="small" >
            <Descriptions.Item label={`Author`} span={3}>
              {citationObj && formatAuthors(citationObj.author)}
            </Descriptions.Item>
            <Descriptions.Item label={`Title`} span={3}>
              {citationObj && citationObj.title}
            </Descriptions.Item>
            <Descriptions.Item label={`Venue`} span={3}>
              {citationObj && formatVenue(citationObj.venue)}
            </Descriptions.Item>
            <Descriptions.Item label={`Year`}>
              {citationObj && citationObj.year}
            </Descriptions.Item>
            <Descriptions.Item label={`Citation Number`} span={3}>
              {citationObj && citationObj.cite_number}
            </Descriptions.Item>
            <Descriptions.Item label={`DOI`} span={3}>
              {citationObj && citationObj.doi ? (<a href={citationObj.doi} target="_blank" rel="noopener noreferrer">{citationObj.doi}</a>) : 'N/A'}
            </Descriptions.Item>
            <Descriptions.Item label={`Source`} span={3}>
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
      //title={title}
      style={{
        width: width,
        height: '100%'
      }}
      styles={{
        body: {
          height: 'calc(100%)',
          overflowY: "scroll",
          position: "relative"
        },
      }}
    >
      <div>
        <Descriptions size="small" column={1} bordered>
          <Descriptions.Item label="Type">
            <Tag color={baseColor} style={{fontSize: 12, lineHeight: 1.5}}>{displayName}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Anomalous">
            <Tag 
              color={categoryColor}
              style={{fontSize: 12, lineHeight: 1.5}}
            >
                {category.displayName}
            </Tag>
            {(category.options !== null && category.options.citationRing) && (
              <Tag color="red" style={{fontSize: 12, lineHeight: 1.5}}>Citation Ring</Tag>
            )}
            {(category.options !== null && category.options.selfCitation) && (
              <Tag color="blue" style={{fontSize: 12, lineHeight: 1.5}}>Self Citation</Tag>
            )}
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
        </Descriptions>
      </div>
    </Card>
  );
};
