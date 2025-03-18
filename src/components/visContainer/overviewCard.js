import { useEffect, useCallback, useState } from "react";
import { Card, Space, Flex, Badge, Tag, Tooltip, Descriptions, Typography, Modal, List, Button } from 'antd';

import AuthorGraph from "./authorGraph";
import AdjacencyMatrixPanel from "./adjacencyMatrix.js";

import "./style.css";

export const OverviewCard = ({
  anomalous,
  author,
  venue,
  citation,
  graphData
}) => {
  const { Text } = Typography;
  const [isModalVisible, setIsModalVisible] = useState(false);

  // Helper function to get author object by ID
  const getAuthorById = (authorId) => {
    return author.find(a => a.id === authorId);
  };

  // Helper function to get venue object by ID
  const getVenueById = (venueId) => {
    return venue.find(v => v.id === venueId);
  }
  // Calculate authors with hop1 citations and their issue counts
  const authorsWithHop1Citations = () => {
    if (!citation || citation.length === 0 || !author || author.length === 0) return [];

    const authorCitationCounts = {};
    const authorIssueCounts = {};
    //console.log('citation', citation);
    citation.forEach((cite) => {
      if (cite.author) {
        cite.author.forEach((authorId) => {
          authorCitationCounts[authorId] = (authorCitationCounts[authorId] || 0) + 1;
          if(cite.has_issue){
            authorIssueCounts[authorId] = (authorIssueCounts[authorId] || 0) + 1;
          }
          
        });
      }
    });

    const authorData = Object.keys(authorCitationCounts).map(authorId => {
      const authorObj = getAuthorById(authorId);
      return {
        id: authorId,
        name: authorObj ? authorObj.standardized_name : "Unknown Author",
        totalCount: authorCitationCounts[authorId],
        issueCount: authorIssueCounts[authorId] || 0,
      };
    });

    // Sort authors: first by issue count (descending), then by total citation count (descending)
    authorData.sort((a, b) => {
      if (b.issueCount !== a.issueCount) {
        return b.issueCount - a.issueCount; // Sort by issue count descending
      } else {
        return b.totalCount - a.totalCount; // Sort by citation count descending
      }
    });

    return authorData;
  };

  // Calculate how many citation issues each venue has
  const calculateIssueCountForVenues = (mostCitedVenues) => {
    if (!anomalous || anomalous.length === 0) {
        return mostCitedVenues.map(venue => ({ ...venue, issueCount: 0 }));
    }

    return mostCitedVenues.map(venue => {
      let issueCount = 0;
      citation.forEach((cite) => {
        if (cite.venue && cite.venue === venue.id && cite.has_issue) {
          
          const citeAnomalous = anomalous.filter(e => e.paper && e.paper.includes(cite.id));

          if(citeAnomalous && citeAnomalous.length > 0){
            issueCount++;
          }
        }
      });

      return {
        ...venue,
        issueCount: issueCount
      };
    });
  };

  // Calculate most cited venues
  const mostCitedVenues = () => {
    const venueCitationCounts = {};
    if (!citation || citation.length === 0 || !venue || venue.length === 0) return [];

    citation.forEach((cite) => {
      if (cite.venue) {
        venueCitationCounts[cite.venue] = (venueCitationCounts[cite.venue] || 0) + 1;
      }
    });

    const sortedVenueIds = Object.keys(venueCitationCounts).sort(
      (a, b) => venueCitationCounts[b] - venueCitationCounts[a]
    );

    return sortedVenueIds.slice(0, 3).map(venueId => { // Top 3
      const venueObj = getVenueById(venueId);
      return {
        name: venueObj ? venueObj.standardized_name : "Unknown Venue",
        type: venueObj ? venueObj.type : "Unknown Type",        
        totalCount: venueCitationCounts[venueId],
        id: venueId,
        issueCount:0,
      }
    });
  };

  // Calculate citation time distribution
  const citationTimeDistribution = () => {
    if (!citation || citation.length === 0) return [];

    const yearCounts = {};
    const years = [];
    citation.forEach(c => {
      if (c.year) {
        yearCounts[c.year] = (yearCounts[c.year] || 0) + 1;
        if (!years.includes(c.year)) {
          years.push(c.year);
        }
      }
    });

    const sortedYears = years.sort((a, b) => a - b);

    const maxCount = Object.values(yearCounts).reduce((max, count) => Math.max(max, count), 0);

    return sortedYears.map(year => ({
      year: year,
      count: yearCounts[year] || 0,
      height: maxCount > 0 ? (yearCounts[year] / maxCount) * 50 : 0, // Normalize height based on max count
    }));
  };

  const hop1CitedAuthors = authorsWithHop1Citations();
  //console.log('hop1CitedAuthors', hop1CitedAuthors);
  const citedVenues = mostCitedVenues();
  const citedVenuesWithIssue = calculateIssueCountForVenues(citedVenues);
  const timeDistribution = citationTimeDistribution();

  // Calculate the appropriate offset based on the font size and rotation
  const labelFontSize = 0.6; //rem
  const labelOffset = labelFontSize*16*0.5 + 2;

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  return (
    <Card
      id="overviewContainer-card"
      size="small"
      title="Information Overview"
      style={{
        width: '100%',
        display: "flex",
        flexDirection: "column",
        flex: 1,
        height: "100%",
      }}
      styles={{
        body: {
          display: "flex",
          flexDirection: "column",
          flex: 1,
          overflow: "auto",
          padding: "10px",
        },
      }}
    >
      <Descriptions size="small" column={1} >
        <Descriptions.Item label="Author Overview">
            <Flex gap={10} wrap={true}>
                {hop1CitedAuthors.slice(0,4).map((author, index) => ( // Display the top 3 authors
                  <span key={`author-${author.id}`}>
                    {author.name}
                    <Text type={author.issueCount > 0 ? 'danger' : 'success'}>
                      {
                        author.issueCount > 0 ? `[${author.issueCount}/${author.totalCount}]` : `[${author.totalCount}]`
                      }
                    </Text>
                  </span>
                ))}
                {/* Show More Button */}
              {hop1CitedAuthors.length > 3 && (
                <Button size="small" type="link" onClick={showModal} style={{padding: 0}}>
                    Show More
                </Button>
              )}
            </Flex>
              <Modal
                title="All Cited Authors"
                open={isModalVisible}
                onCancel={handleCancel}
                width={1200}
                destroyOnClose={true}
                style={{
                  top: 20
                }}
                footer={[
                  <Button key="show-author-graph-btn" onClick={handleCancel}>
                    Show author graph
                  </Button>
                ]}
                >
                  {<List
                    style={{
                      height: 800,
                      overflow: 'auto'
                    }}
                    dataSource={hop1CitedAuthors}
                    renderItem={(item) => (
                      <List.Item>
                        <Text strong>{item.name}</Text>
                        <Text type={item.issueCount > 0 ? 'danger' : 'success'}>
                          {item.issueCount > 0 ? `[${item.issueCount}/${item.totalCount}]` : `[${item.totalCount}]`}
                        </Text>
                      </List.Item>
                    )}
                  />}
                  {<AdjacencyMatrixPanel 
                    graphData={graphData}
                    author={author}
                    citation={citation}
                  />}
                  {/*<AuthorGraph 
                    graphData={graphData}
                    author={author}
                  />*/}
              </Modal>
        </Descriptions.Item>
        <Descriptions.Item label="Most Cited Venues">
          <Flex gap={10}>
            {citedVenuesWithIssue.map((venue, index) => (
              <span key={`venue-${venue.id}`}>
                  <Tooltip key={`venue-tip-${venue.id}`} title={`${venue.name} [${venue.type}]`}>
                    <span style={{display:"inline-block", overflow:"hidden", textOverflow:"ellipsis", maxWidth:"200px", whiteSpace:"nowrap"}}>{venue.name}</span>
                    <Text type={venue.issueCount > 0 ? 'danger' : 'success'} style={{position: 'relative', top: -5, marginLeft: 5}}>
                      {
                        venue.issueCount > 0 ? `[${venue.issueCount}/${venue.totalCount}]` : `[${venue.totalCount}]`
                      }
                    </Text>
                  </Tooltip>
                </span>
              
            ))}
          </Flex>
        </Descriptions.Item>
        <Descriptions.Item label="Citation Time Distribution" >
          
          
            <Flex gap={5}>
            <Flex
              gap="small"
              align="flex-end"
              style={{
                height: 50,
                borderBottom: '1px solid #ddd',
                width: '100%', // Ensure the container takes the full width
                position: 'relative' // Add relative positioning
              }}
            >
              {timeDistribution.map((item, index) => (
                <Tooltip key={`time-dist-tooltip-${index}`} title={`${item.year}: ${item.count} citations`}>
                  <div
                    key={`time-dist-${index}`}
                    style={{
                      height: item.height,
                      width: 20,
                      backgroundColor: '#999',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      position: 'relative' // Add relative positioning
                    }}
                  >
                    {/* Citation count label */}
                    <span
                      style={{
                        fontSize: '0.6rem',
                        position: 'absolute', // Absolute positioning to overlap
                        top: '-0.8rem', // Position above the bar
                        left: '50%', // Center horizontally
                        transform: 'translateX(-50%)', // Adjust for centering
                        whiteSpace: 'nowrap',
                        color: '#000'
                      }}
                    >
                      {item.count}
                    </span>
                    <span style={{
                        fontSize: `${labelFontSize}rem`, // Small font size
                        position: 'absolute', // Change to absolute
                        bottom: `-${labelOffset+8}px`, // Use calculated offset here
                        whiteSpace: 'nowrap',
                        textAlign: 'center',
                        transform: 'rotate(-30deg) translateX(-50%)', // Center horizontally and rotate
                        left: '50%'
                      }}>{item.year}</span>
                  </div>
                </Tooltip>
              ))}
            </Flex>
          </Flex>
        </Descriptions.Item>
      </Descriptions>
    </Card>
  );
};
