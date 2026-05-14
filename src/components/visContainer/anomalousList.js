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

  // Order: by first page the issue appears (null pages — e.g. unreferenced —
  // go last), then by category severity within the page. Insertion order is
  // preserved within ties.
  const CATEGORY_RANK = {
    testFailure: 0,
    selfCitation: 1,
    citationRing: 2,
    unreferenced: 3,
    lowRelevancy: 4,
  };
  const firstPage = (e) => {
    const pages = (e.anchors || [])
      .map(a => a && a.page)
      .filter(p => p != null);
    if (pages.length) return Math.min(...pages);
    return e.page != null ? e.page : Number.POSITIVE_INFINITY;
  };


  return (
    <Card
      //ref={listRef}
      id="anomalousListContainer-card"
      size="small"
      title="Anomalies List"
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
      .map((e, i) => ({ e, i }))
      .sort((a, b) => {
        const pageDiff = firstPage(a.e) - firstPage(b.e);
        if (pageDiff !== 0) return pageDiff;
        const rankA = CATEGORY_RANK[a.e.category?.name] ?? 99;
        const rankB = CATEGORY_RANK[b.e.category?.name] ?? 99;
        if (rankA !== rankB) return rankA - rankB;
        return a.i - b.i;
      })
      .map(({ e }) => {
        const anomalousName = e.displayName;
        const anomalousCategoryName = e.category.displayName;
        const baseColor = anomalousColorScheme[e.name]['baseColor'];
        const categoryColor = anomalousColorScheme[e.name]['category'][e.category.name]['baseColor'];
        const boxColor = anomalousColorScheme[e.name]['category'][e.category.name]['boxColor'];
        const bgColor = activeHighlight === e.id && boxColor;
        const anchorPages = Array.from(
          new Set(
            (e.anchors || [])
              .map(a => a && a.page)
              .filter(p => p != null)
          )
        ).sort((a, b) => a - b);
        const pages = anchorPages.length ? anchorPages : (e.page != null ? [e.page] : []);
        const pageLabel = pages.length > 1
          ? `Pages: ${pages.join(', ')}`
          : `Page: ${pages.length === 1 ? pages[0] : '—'}`;

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
              <Text type="secondary" style={{fontSize:14}}>{pageLabel}</Text>
            </Flex>
          </Card>
        );
      }
      )}
    </Card>
  );
};
