import { useEffect, useCallback, useState, useRef } from "react";
import { Card, Empty } from 'antd';
import { pdfjs } from "react-pdf";

import { ContentCard } from "./contentCard";
import { SectionCard } from "./sectionCard";
import { OverviewCard } from "./overviewCard";
import { AnomalousListCard } from "./anomalousList";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

export const VisContainer = ({
  file,
  citation,
  author,
  venue,
  anomalous,
  anomalousColorScheme,
  currentPage,
  activeHighlight,
  setActiveHighlight
}) => {
  const [selectedTarget, setSelectedTarget] = useState(null);
  const [sections, setSections] = useState([]);

  const handleCardClick = (id) => {
    id === activeHighlight ? setActiveHighlight(null) : setActiveHighlight(id);
  };
  

  useEffect(() => {
    if (!file) return; // Ensure file is loaded before calling pdfjs
  
    const loadSections = async () => {
      try {
        const loadingTask = pdfjs.getDocument(file);
        const pdf = await loadingTask.promise;
  
        // Get document outline (sections)
        const outline = await pdf.getOutline();
        if (!outline) {
          console.warn("No outline found in this PDF.");
          return;
        }
  
        // Resolve page numbers for each section
        const sectionsWithPages = await Promise.all(
          outline.map(async (item) => {
            let pageNumber = null;
  
            if (item.dest) {
              try {
                const dest = Array.isArray(item.dest) ? item.dest[0] : item.dest;
                const resolvedDest = await pdf.getDestination(dest);
                const pageRef = resolvedDest ? resolvedDest[0] : dest;
  
                if (pageRef && pageRef.num) {
                  const pageIndex = await pdf.getPageIndex(pageRef);
                  pageNumber = pageIndex + 1;
                }
              } catch (error) {
                console.warn(`Error resolving page for section: ${item.title}`, error);
              }
            }
  
            return {
              title: item.title,
              page: pageNumber,
            };
          })
        );
  
        setSections(sectionsWithPages);
      } catch (error) {
        console.error("Error loading PDF sections:", error);
      }
    };
  
    loadSections();
  }, [file]); // Runs only when `file` changes
  
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
       {/*<SectionCard 
          sections={sections}
       />*/}
       <OverviewCard 
          anomalous={anomalous}
          author={author}
          venue={venue}
          citation={citation}
       />
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