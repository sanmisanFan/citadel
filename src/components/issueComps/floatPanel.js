import { useState, useEffect } from "react";
import { Tag, Collapse } from 'antd';

const { Panel } = Collapse;

export const FloatingPanel = ({ currentPage, anomalous, anomalousColorScheme, setAnomalous }) => {
  const [isLegendOpen, setIsLegendOpen] = useState(true);

  const toggleLegend = () => {
    setIsLegendOpen(!isLegendOpen);
  };

  // Dynamically generate legend data based on anomalous and anomalousColorScheme
  const generateLegendData = () => {
    const legend = {};

    anomalous.forEach((issue) => {
      const issueType = issue.name; // 'citation', 'statistic', 'other'
      const issueCategory = issue.category.name; // e.g., 'lowRelevancy', 'retractedPaper', 'testFailure', 'valueInconsistency', 'noRef'
      const issueCategoryDisplayName = issue.category.displayName;
      const issueFilter = issue.filter

      if (!legend[issueType]) {
        legend[issueType] = {
          label: capitalizeFirstLetter(issueType) + (issueType === "other" ? " Anomalies" : " Issues"), // Make label more user friendly
          color: anomalousColorScheme[issueType].baseColor,
          children: [],
          filter: false, // Initialize parent filter to false
          typeName: issueType,
        };
      }

      const existingChild = legend[issueType].children.find(child => child.label === issueCategoryDisplayName);

      if (!existingChild) {
        legend[issueType].children.push({
          label: issueCategoryDisplayName,
          color: anomalousColorScheme[issueType].category[issueCategory].baseColor,
          count: 1,
          categoryName: issueCategory,
          typeName: issueType,
          filter: issueFilter
        });
      } else {
        existingChild.count++;
        existingChild.filter = issueFilter
      }
    });

    //check if all children are filtered under same parent
    for (const typeName in legend) {
      const parent = legend[typeName];
      if (parent.children.every(child => child.filter)) {
        parent.filter = true;
      } else {
        parent.filter = false;
      }
    }

    // Convert the legend object to an array for rendering
    return Object.values(legend);
  };

  // Helper function to capitalize the first letter of a string
  const capitalizeFirstLetter = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  const [legendData, setLegendData] = useState([]);

  useEffect(() => {
    setLegendData(generateLegendData());
  }, [anomalous, anomalousColorScheme]);

    const handleLegendClick = (typeName, categoryName = null) => {
        setAnomalous(prevAnomalous => {
            return prevAnomalous.map(anomalousObj => {
              if (categoryName === null && anomalousObj.name === typeName) {
                  return {
                      ...anomalousObj,
                      filter: !anomalousObj.filter,
                  };
                }

              if (anomalousObj.name === typeName && anomalousObj.category.name === categoryName) {
                  return {
                      ...anomalousObj,
                      filter: !anomalousObj.filter,
                  };
              }
                return anomalousObj;
            });
        });
        setLegendData(generateLegendData()); //update the legend data
    };

  const renderTree = (data) => {
    return (
      <ul style={{ listStyle: "none", padding: 0 }}>
        {data.map((item, index) => (
          <li key={index} style={{ marginBottom: "12px" }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "8px",
                cursor: "pointer",
                opacity: item.filter ? 0.5 : 1,
                fontWeight: item.filter ? "normal" : "bold",
                textDecoration: item.filter ? "line-through" : "none",
                 color: item.filter ? '#999' : '#000'
              }}
               onClick={() => handleLegendClick(item.typeName)}
            >
              <div
                style={{
                  width: "20px",
                  height: "12px",
                  backgroundColor: item.color,
                  borderRadius: "2px",
                  display: "inline-block",
                }}
              />
              <span style={{ fontSize: "14px", fontWeight: 500 }}>
                {item.label}
              </span>
            </div>
            <ul style={{ listStyle: "none", padding: 0, marginLeft: '20px', marginTop: '8px' }}>
              {item.children.map((child, childIndex) => (
                <li
                  key={childIndex}
                  style={{
                    marginBottom: "8px",
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    cursor: 'pointer',
                    opacity: child.filter ? 0.5 : 1, // Gray out if filtered
                    fontWeight: child.filter ? 'normal' : 'bold', // Bold if not filtered
                    textDecoration: child.filter ? 'line-through' : 'none',
                    color: child.filter ? '#999' : '#666'
                  }}
                  onClick={() => handleLegendClick(child.typeName, child.categoryName)}
                >
                  <div
                    style={{
                      width: '15px',
                      height: '10px',
                      backgroundColor: child.color,
                      borderRadius: '2px',
                      display: 'inline-block',
                    }}
                  />
                  <span style={{ fontSize: '12px' }}>{child.label}</span>
                  <span style={{ fontSize: '12px', marginLeft: '5px' }}>({child.count})</span>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    );
  };

  return (
    <div
      style={{
        position: "absolute",
        top: "50px",
        right: "10px",
        width: "300px", // Increased width for better readability
        padding: "10px",
        backgroundColor: "white",
        border: "1px solid #ddd",
        borderRadius: "5px",
        boxShadow: "0px 2px 5px rgba(0,0,0,0.2)",
        zIndex: 1000,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h4 style={{ margin: "0" }}>Detected Anomalous Legend:</h4>
        <span onClick={toggleLegend} style={{ cursor: "pointer", fontSize: '12px', textDecoration: 'underline' }}>
            {isLegendOpen ? "Hide Legend" : "Show Legend"}
        </span>
      </div>

      {isLegendOpen && (
        <div>
          <div style={{ marginTop: "10px", marginBottom: "5px" }}></div>
          {renderTree(legendData)}
        </div>
      )}
    </div>
  );
};
