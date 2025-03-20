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
  authorGraphDataRaw
}) => {

  const [authorGraphData, setAuthorGraphData] = useState(null);

  const authorGraphDataProcess = () => {
    if (!authorGraphDataRaw || !author) return;

    // add author names to author nodes
    const authorGraphDataRaw_ = JSON.parse(JSON.stringify(authorGraphDataRaw));

    // Filter nodes with groups not equal to 0
    authorGraphDataRaw_.nodes = authorGraphDataRaw_.nodes.filter(node => node.group !== 0);

    // Filter links that only contain nodes with groups not equal to 0
    const validNodeIds = new Set(authorGraphDataRaw_.nodes.map(node => node.id));
    authorGraphDataRaw_.links = authorGraphDataRaw_.links.filter(link => validNodeIds.has(link.source) && validNodeIds.has(link.target));

    // Add corresponding author name to each node
    authorGraphDataRaw_.nodes.forEach(node => {
      const authorData = author.find((a) => a.id === node.id);
      if (authorData) {
        node.name = authorData.standardized_name;
      }
     // node.name = author.find((a) => a.id === node.id).standardized_name;
    });

    console.log(authorGraphDataRaw_);
    return(authorGraphDataRaw_);
  };



  useEffect(() => {
    setAuthorGraphData(authorGraphDataProcess());
  }, [authorGraphDataRaw, author]);
  
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
          graphData={authorGraphData}
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