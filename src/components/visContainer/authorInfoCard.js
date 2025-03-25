import React from 'react';
import { Card, Typography, List, Tooltip, Divider, Space, Tag, Popover } from 'antd';
import AuthorGraph from './authorGraph'; // Import AuthorGraph component

const { Text, Link } = Typography;

export const AuthorInfoCard = ({ author, citation, authorGraphData, anomalous, anomalousColorScheme }) => {
  if (!author) return null;

  const authorCitations = citation.filter(cite => cite.author.includes(author.id));
  const authorAnomalies = anomalous.filter(anomaly =>
    anomaly.paper !== null && authorCitations.some(cite => cite.id === anomaly.paper[0])
  );

  // Filter graph data
  const authorNode = authorGraphData.nodes.find(node => node.id === author.id);
  const authorGroup = authorNode ? authorNode.group : null;

  const filteredNodes = authorGraphData.nodes.filter(node => node.id === author.id || node.group === authorGroup);
  const filteredNodeIds = new Set(filteredNodes.map(node => node.id));

  const filteredLinks = authorGraphData.links.filter(link => 
    filteredNodeIds.has(link.source.id || link.source) && filteredNodeIds.has(link.target.id || link.target)
  );

  console.log("filteredGraphData", author.standardized_name, filteredLinks);
  const filteredGraphData = {
    nodes: filteredNodes,
    links: filteredLinks
  };

  return (
    <div
      style={{ width: '500px', height: '100%', overflowY: 'scroll' }}
    >
      <Space direction="vertical" style={{ width: '100%' }}>
        <Text strong style={{ fontSize: '18px' }}>{author.standardized_name}</Text>

        <Space wrap>
          {author.orcid && (
            <Tooltip title="ORCID">
              <Link href={author.orcid} target="_blank">
                <Tag color="blue">ORCID</Tag>
              </Link>
            </Tooltip>
          )}
        </Space>
        <Divider style={{ margin: '8px 0' }} />

        <Text strong>Citations</Text>
        {authorCitations.length > 0 ? (
          <List
            size="small"
            bordered
            dataSource={authorCitations}
            renderItem={cite => {
              const citeAnomalies = anomalous.filter(anomaly => anomaly.paper && anomaly.paper.includes(cite.id));
              const hasIssue = cite.has_issue;
              const anomalousNames = citeAnomalies.map(anomaly => anomaly.displayName);
              const anomalousCategories = citeAnomalies.map(anomaly => anomaly.category.displayName);
              const anomalousOptions = citeAnomalies.map(anomaly => anomaly.category.options);
              const anomalousColors = citeAnomalies.map(anomaly => anomalousColorScheme[anomaly.name]['category'][anomaly.category.name]['baseColor']);

              return (
                <List.Item>
                <Text>
                  <Text strong>Source:</Text> {cite.source}
                  <br />
                  {hasIssue && (
                    <Tag color={anomalousNames.length > 0 ? anomalousColors[0] : "red"} style={{ marginLeft: '8px' }}>
                      {anomalousNames.length > 0 ? anomalousNames[0] : "Has Issue"}
                    </Tag>
                  )}
                  {anomalousOptions.length > 0 && anomalousOptions[0] && anomalousOptions[0].citationRing && (
                    <Tag color="blue" style={{ marginLeft: '8px' }}>
                      Citation Ring
                    </Tag>
                  )}
                  {anomalousOptions.length > 0 && anomalousOptions[0] && anomalousOptions[0].selfCitation && (
                    <Tag color="purple" style={{ marginLeft: '8px' }}>
                      Self Citation
                    </Tag>
                  )}
                </Text>  
                </List.Item>
              );
            }}
            style={{ marginBottom: '10px' }}
          />
        ) : (
          <Text type="secondary">No citations found for this author.</Text>
        )}

        {/* Add AuthorGraph component */}
        <Divider style={{ margin: '8px 0' }} />
        <Text strong>Citation Graph</Text>
        <AuthorGraph 
          authorID={author.id}
          graphData={filteredGraphData} 
          author={author} 
          height={300}
        />
      </Space>
    </div>
  );
};
