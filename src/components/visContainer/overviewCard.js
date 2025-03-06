import { useEffect, useCallback, useState } from "react";
import { Card, Space, Flex, Badge, Tag, Tooltip } from 'antd';

import "./style.css";

export const OverviewCard = ({
  anomalous,
  author,
  venue,
  citation
}) => {
  // Calculate most cited authors
  const mostCitedAuthors = () => {
    const authorCitationCounts = {};
    if (!citation || citation.length === 0 || !author || author.length === 0) return [];

    citation.forEach((cite) => {
      if (cite.author) {
        cite.author.forEach((authorId) => {
          authorCitationCounts[authorId] = (authorCitationCounts[authorId] || 0) + 1;
        });
      }
    });

    const sortedAuthorIds = Object.keys(authorCitationCounts).sort(
      (a, b) => authorCitationCounts[b] - authorCitationCounts[a]
    );

    return sortedAuthorIds.slice(0, 3).map(authorId => {
      const authorObj = author.find(a => a.id === authorId);
      return {
        name: authorObj ? authorObj.standardized_name : "Unknown Author",
        count: authorCitationCounts[authorId],
        id: authorId
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

    return sortedVenueIds.slice(0, 3).map(venueId => {
      const venueObj = venue.find(v => v.id === venueId);
      return {
        name: venueObj ? venueObj.standardized_name : "Unknown Venue",
        type: venueObj ? venueObj.type : "Unknown Type",
        count: venueCitationCounts[venueId],
        id: venueId
      };
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

  const citedAuthors = mostCitedAuthors();
  const citedVenues = mostCitedVenues();
  const timeDistribution = citationTimeDistribution();
  const anomalousCategories = {};

  if (anomalous && anomalous.length > 0) {
    anomalous.forEach(e => {
      const catName = e.category.displayName;
      anomalousCategories[catName] = true;
    });
  }

  return (
    <Card
      id="overviewContainer-card"
      size="small"
      title="Information Overview"
      style={{
        width: '100%', // Changed to 100% to fill the available width
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
      <Space
        direction="vertical"
        size="middle"
        style={{
          flex: 1,
          width: '100%'
        }}
      >
        <Flex
          gap="middle" // Reduced gap
          align="center"
          wrap="wrap" // Add wrap for better responsiveness
        >
          <b>Most cited author:</b>
          <Flex wrap='wrap' gap={20}>
            {citedAuthors.map((author, index) => (
              <Badge key={`author-${author.id}`} count={author.count} size="small" offset={[5, 0]}>
                <span id={`author-${author.id}`}>{author.name}</span>
              </Badge>
            ))}
          </Flex>
        </Flex>

        <Flex
          gap="middle" // Reduced gap
          align="center"
          wrap="wrap" // Add wrap for better responsiveness
        >
          <b>Most cited venue:</b>
          <Flex wrap='wrap' gap={20}>
            {citedVenues.map((venue, index) => (
              <Tooltip key={`venue-tip-${venue.id}`} title={`${venue.name} [${venue.type}]`}>
                <Badge key={`venue-${venue.id}`} count={venue.count} size="small" offset={[5, 0]}>
                  <span id={`venue-${venue.id}`} style={{display:"inline-block", overflow:"hidden", textOverflow:"ellipsis", maxWidth:"200px", whiteSpace:"nowrap"}}>{venue.name}</span>
                </Badge>
              </Tooltip>
            ))}
          </Flex>
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
              borderBottom: '1px solid #ddd',
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
                    
                  }}
                />
              </Tooltip>
            ))}
          </Flex>
        </Flex>

        <Flex
          gap="small"
          align="center"
          wrap='wrap'
        >
          <b>Detected Potential Anomalous:</b>
          {Object.keys(anomalousCategories).map((catName, index) => {
            let tagColor = "blue";
            if (catName.toLowerCase().includes("retracted")) {
              tagColor = "red";
            } else if (catName.toLowerCase().includes("relevancy")) {
              tagColor = "magenta";
            }
            return (
              <Tag key={catName + index} bordered={false} color={tagColor}>
                {catName}
              </Tag>
            );
          })}
        </Flex>
      </Space>
    </Card>
  );
};
