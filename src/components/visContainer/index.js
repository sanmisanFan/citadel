import { useEffect, useCallback, useState, useRef } from "react";
import { Card, Empty } from 'antd';
import { pdfjs } from "react-pdf";

import { ContentCard } from "./contentCard";
import { AnomalousLegendCard } from "./anomalousLegendCard";
import { OverviewCard } from "./overviewCard";
import { AnomalousListCard } from "./anomalousList";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

/**
 * 
 * <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span>Anomalous Overview</span>
          <span onClick={toggleLegend} style={{ cursor: "pointer", fontSize: '12px', textDecoration: 'underline' }}>
              {isLegendOpen ? "Hide Legend" : "Show Legend"}
          </span>
        </div>
 */

export const VisContainer = ({
  file,
  citation,
  author,
  venue,
  anomalous,
  anomalousColorScheme,
  currentPage,
  activeHighlight,
  setActiveHighlight,
  authorGraphData
}) => {

  const [graphData, setGraphData] = useState(null);

  const graphDataProcess = () => {
    if (!authorGraphData || !author) return;

    // Construct nodes and links for D3
    const nodes = [];
    const links = [];
    const nodeMap = {}; // To track existing nodes

    // Filter links and count targets for each source
    const filteredLinks = authorGraphData
      .filter((link) => link.value > 3);

    filteredLinks.forEach((link) => {
      const sourceAuthor = author.find((a) => a.id === link.source);
      const targetAuthor = author.find((a) => a.id === link.target);

      if (sourceAuthor && targetAuthor) {
        if (!nodeMap[link.source]) {
          nodes.push({ id: link.source, name: sourceAuthor.standardized_name });
          nodeMap[link.source] = true;
        }
        if (!nodeMap[link.target]) {
          nodes.push({ id: link.target, name: targetAuthor.standardized_name });
          nodeMap[link.target] = true;
        }
        links.push({ source: link.source, target: link.target });
      }
    });

    const graphData = { nodes, links };
    console.log(graphData);
    return graphData;
  };

  useEffect(() => {
    setGraphData(graphDataProcess());
  }, [authorGraphData, author]);
  
  return(
    <div
      style={{
        height: '100vh',
        padding: 5,
        backgroundColor: '#f9f9f9',
        display: 'flex',
        flexDirection: 'column',
        gap: 5
        //borderRight: '1px solid #dddddd'
      }}
    >
      <div
        style={{
          width: '100%',
          height: 250,
          display: 'flex',
          gap: 5
        }}
      >
       <OverviewCard 
          anomalous={anomalous}
          author={author}
          venue={venue}
          citation={citation}
          graphData={graphData}
       />
       {/*<AnomalousLegendCard />*/}
      </div>

      <div
        style={{
          width: '100%',
          //flex: 1,
          height: 'calc(100% - 250px)',
          display: 'flex',
          gap: 5
        }}
      >
        <AnomalousListCard 
          anomalous={anomalous}
          anomalousColorScheme={anomalousColorScheme}
          activeHighlight={activeHighlight}
          setActiveHighlight={setActiveHighlight}
        />
        {
          activeHighlight === null ? 
          <Card
            size="small"
            style={{
              width: '60%',
            }}
            //className="custom-card"
          >
            <Empty
              description={"Select a anomalous"}
              style={{
                marginTop: 300
              }}
            />
          </Card> :
          <ContentCard 
            width={'60%'}
            id={'anomalousContainer-card'}
            title={'Citation Anomalous'}
            activeHighlight={activeHighlight}
            anomalous={anomalous}
            citation={citation}
            author={author}
            venue={venue}
          />
        }
      </div>
    </div>
  );
}