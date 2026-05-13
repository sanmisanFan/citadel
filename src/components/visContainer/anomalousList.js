import { useEffect, useRef } from "react";
import { Card, Flex, Tag, Typography, Tooltip } from 'antd';

import "./style.css";

const { Text } = Typography;

export const AnomalousListCard = ({
  anomalous,
  anomalousColorScheme,
  activeHighlight,
  setActiveHighlight
}) => {
  //const listRef = useRef(null);
  const itemRefs = useRef({});

  const handleCardClick = (id) => {
    //console.log(id);
    id === activeHighlight ? setActiveHighlight(null) : setActiveHighlight(id);
  };

  // Scroll active highlight into view
  useEffect(() => {
    if (activeHighlight && itemRefs.current[activeHighlight]) {
      itemRefs.current[activeHighlight].scrollIntoView({
        behavior: "smooth",
        block: "nearest",
      });
    }
  }, [activeHighlight]);

  // Tooltip content for each tag
  const tagTooltips = {
    citationRing: "Citations within the same paper or among a close network of papers.",
    selfCitation: "Citations referring to the authors' own previous work.",
    unreferenced: "Reference listed in the bibliography but never cited in the body of the manuscript.",
  };


  return (
    <Card
      //ref={listRef}
      id="anomalousListContainer-card"
      size="small"
      title="Anomalous List"
      style={{
        width: '40.3%',
        display: "flex",
        flexDirection: "column",
        //flex: 1, // Ensures the Card itself stretches
        height: "100%", // Fills the parent container
      }}
      styles={{
        body: {
          height: "100%",
          overflowY: "scroll",
          position: "relative"
        },
      }}
    //className="custom-card"
    >
      {anomalous
      .filter(e => !e.filter) // Filter out anomalous with filter === true
      .map(e => {
        const anomalousName = e.displayName;
        const anomalousCategoryName = e.category.displayName;
        const baseColor = anomalousColorScheme[e.name]['baseColor'];
        const categoryColor = anomalousColorScheme[e.name]['category'][e.category.name]['baseColor'];
        const boxColor = anomalousColorScheme[e.name]['category'][e.category.name]['boxColor'];
        const bgColor = activeHighlight === e.id && boxColor;
        const page = e.page;

        // Extract options and create tags
        const options = e.category.options;
        const optionTags = [];
        if (options) {
          if (options.citationRing) {
            optionTags.push(
                <Tooltip key="citationRing" title={tagTooltips.citationRing}>
                  <Tag color="purple" style={{fontSize: 10, lineHeight: 1.5}}>
                    Citation Ring
                  </Tag>
                </Tooltip>
            );
          }
          if (options.selfCitation) {
            optionTags.push(
               <Tooltip key="selfCitation" title={tagTooltips.selfCitation}>
                  <Tag color="magenta" style={{fontSize: 10, lineHeight: 1.5}}>
                    Self Citation
                  </Tag>
                </Tooltip>
            );
          }
          if (options.unreferenced) {
            optionTags.push(
              <Tooltip key="unreferenced" title={tagTooltips.unreferenced}>
                <Tag color="default" style={{fontSize: 10, lineHeight: 1.5}}>
                  Unreferenced
                </Tag>
              </Tooltip>
            );
          }
        }
        return (
          <Card
            key={'anomalous-list-element-key-' + e.id}
            id={'anomalous-list-element-' + e.id}
            size="small"
            style={{
              width: "100%",
              padding: 5,
              //marginTop: 5,
              marginBottom: 10,
              backgroundColor: bgColor,
              cursor: "pointer"
            }}
            onClick={() => handleCardClick(e.id)}
            ref={(el) => (itemRefs.current[e.id] = el)}
          >
            <Flex
              justify="space-between"
              align="center"
              style={{width:'100%'}}
            >
              <Flex vertical gap={1}>
                <Text strong style={{ color: baseColor, fontSize:12 }}>
                    {anomalousName}
                </Text>
                <Tag color={categoryColor}>
                  <b>{anomalousCategoryName}</b>
                </Tag>
              </Flex>
              <Flex vertical gap={5}>
              {optionTags}
              </Flex>
              <Text type="secondary" style={{fontSize:14}}>Page: {page ?? '—'}</Text>
            </Flex>
          </Card>
        );
      }
      )}
    </Card>
  );
};
