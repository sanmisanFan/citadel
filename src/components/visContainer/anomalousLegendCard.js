import { Card } from 'antd';

import "./style.css";

export const AnomalousLegendCard = ({}) => {
  // Sample data for the tree-style list (replace with your actual data)
  const legendData = [
    {
      label: "Citation Issues",
      color: "#ff7875", // Example color for Citation Issues
      children: [
        { label: "Outdated Citation", color: "#ffccc7" }, // Light red
        { label: "Self-Citation", color: "#ffa39e" }, // Medium red
        { label: "Missing Citation", color: "#ff4d4f" }, // Dark red
      ],
    },
    {
      label: "Other Anomalies",
      color: "#91d5ff", // Example color for Other Anomalies
      children: [
        { label: "Inconsistent Methodology", color: "#d6e4ff" }, // Light blue
        { label: "Unsupported Claim", color: "#69c0ff" }, // Medium blue
      ],
    },
  ];

  const renderTree = (data) => {
    return (
      <ul style={{ listStyle: "none", padding: 0 }}>
        {data.map((item, index) => (
          <li key={index} style={{ marginBottom: "12px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: '8px' }}>
              <div
                style={{
                  width: '12px',
                  height: '12px',
                  backgroundColor: item.color,
                  borderRadius: '2px',
                  display: 'inline-block'
                }}
              />
              <span style={{ fontSize: '14px', fontWeight: 500 }}>{item.label}</span>
            </div>
            <ul style={{ listStyle: "none", padding: 0, marginLeft: '20px', marginTop: '8px' }}>
              {item.children.map((child, childIndex) => (
                <li key={childIndex} style={{ marginBottom: "8px", display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <div
                    style={{
                      width: '10px',
                      height: '10px',
                      backgroundColor: child.color,
                      borderRadius: '2px',
                      display: 'inline-block',

                    }}
                  />
                  <span style={{ fontSize: '12px', color: '#666' }}>{child.label}</span>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    );
  };

  return (
    <Card
      id='sectionContainer-card'
      size="small"
      title={
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontWeight: 600, fontSize: 16 }}>Anomaly Overview</span>
        </div>
      }
      style={{
        width: '40%',
      }}
    >
      <div
        style={{
          height: 200, // Adjusted height
          overflowY: 'auto'
        }}
      >
        {renderTree(legendData)}
      </div>
    </Card>
  );
};
