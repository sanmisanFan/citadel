import { Card, Descriptions, Tag } from 'antd';

import "./style.css";

export const ContentCard = ({
  width,
  id,
  title,
  activeHighlight,
  anomalous,
  citation,
  author,
  venue,
  anomalousColorScheme
}) => {
  const selectedAnomalous = anomalous.find(e => e.id === activeHighlight);
  const baseColor = anomalousColorScheme[selectedAnomalous.name]['baseColor'];
  const categoryColor = anomalousColorScheme[selectedAnomalous.name]['category'][selectedAnomalous.category.name]['baseColor'];

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
    return venueObj ? `${venueObj.standardized_name}` : "Unknown Venue";
  };

  const citationInfo = paper && paper.length > 0 ? (
    paper.map((citationId, index) => {
      const citationObj = citation.find(c=>c.id===citationId);
      console.log("citationObj", citationObj);
      
      return (
        <div key={`citation-${index}`} style={{padding: 5}}>
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
            {(category.options !== null && category.options.unreferenced) && (
              <Tag color="default" style={{fontSize: 12, lineHeight: 1.5}}>Unreferenced</Tag>
            )}
          </Descriptions.Item>
          <Descriptions.Item label="Page">
            {page ?? '—'}
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
