import { useEffect, useCallback, useState, useRef } from "react";
import { Card, Empty } from 'antd';

import { ContentCard } from "./contentCard";

export const VisContainer = ({
  highlights,
  currentPage,
  activeHighlight,
  setActiveHighlight
}) => {
  const [selectedTarget, setSelectedTarget] = useState(null);

  const handleCardClick = (id) => {
    id === activeHighlight ? setActiveHighlight(null) : setActiveHighlight(id);
  };
  //console.log('activeHighlight', activeHighlight);
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
          height: 300,
          display: 'flex',
          gap: 5
        }}
      >
       <ContentCard 
        width={'40%'}
        id={'sectionContainer-card'}
        title={'Section Overview'}
       />
       <ContentCard 
        width={'60%'}
        id={'sectionContainer-card'}
        title={'Information Overview'}
       />
      </div>

      <div
        style={{
          width: '100%',
          flex: 1,
          display: 'flex',
          gap: 5
        }}
      >
        <ContentCard 
          width={'40%'}
          id={'anomalousListContainer-card'}
          title={'Anomalous List'}
        />
        {
          selectedTarget === null ? 
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
            title={'Information Overview'}
          />
        }
      </div>
      
      {/*highlights.map(e=>
        <Card
          key={'highlight-card-container-key-'+e.id}
          id={'highlight-card-container-'+e.id}
          size="small"
          style={{
            width: "100%",
            padding: 10,
            marginTop: 10,
            marginBottom: 10,
            backgroundColor: activeHighlight === e.id && e.color
          }}
          onClick={() => handleCardClick(e.id)}
        >
          <span>{e.redFlag.category}</span>
        </Card>
      )*/}
    </div>
  );
}