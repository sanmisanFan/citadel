import { useEffect, useRef } from "react";
import * as d3 from "d3";

const AdjacencyMatrixPanel = ({ graphData, author, citation }) => {
  const canvasRef = useRef(null);

  const drawGraph = (graphData) => {
    if (!graphData || !graphData.nodes || !graphData.links || graphData.nodes.length === 0) {
      return; // Exit if data is invalid or empty
    }
    const { scrollWidth, scrollHeight } = canvasRef.current;
    let dimensions = {
      width: scrollWidth,
      height: scrollHeight,
      margin: {
        top: 100, // Increased top margin for labels
        right: 10,
        bottom: 10,
        left: 200, // Increased left margin for labels
      },
    };
    dimensions.boundedWidth =
      dimensions.width - dimensions.margin.left - dimensions.margin.right;
    dimensions.boundedHeight =
      dimensions.height - dimensions.margin.top - dimensions.margin.bottom;

    const svgRoot = d3.select(canvasRef.current).select("svg");
    const rootGroup = svgRoot.select("g#root-group");

    // Remove existing graph group if it exists
    rootGroup.select("#graph-group").remove();

    // Create a group for the graph within the root group
    const graphGroup = rootGroup
      .append("g")
      .attr("id", "graph-group")
      .attr(
        "transform",
        `translate(${dimensions.margin.left}, ${dimensions.margin.top})`
      );

    // Extract nodes and links
    let nodes = graphData.nodes;
    const links = graphData.links;

    // Filter authors to include only those in hop1 citations
    const hop1AuthorIds = new Set();
    citation.forEach(cite => {
      if (cite.hop === 1 && cite.author) {
        cite.author.forEach(authorId => hop1AuthorIds.add(authorId));
      }
    });
      
    nodes = nodes.filter(node => hop1AuthorIds.has(node.id));
    if(nodes.length === 0) return;

    // Create an author lookup table (node id => author object)
    const authorLookup = {};
    nodes.forEach((node) => {
      authorLookup[node.id] = node;
    });

    // Create an adjacency matrix
    const matrix = {};
    nodes.forEach((source) => {
      matrix[source.id] = {};
      nodes.forEach((target) => {
        matrix[source.id][target.id] = 0;
      });
    });

    // Populate the adjacency matrix, only considering links between hop1 authors
    links.forEach((link) => {
      if (hop1AuthorIds.has(link.source) && hop1AuthorIds.has(link.target)) {
        matrix[link.source][link.target] = 1;
      }
    });

    // Sort nodes alphabetically for consistent matrix
    nodes.sort((a, b) => a.name.localeCompare(b.name));
    const nodeOrder = nodes.map(node => node.id);

    // Calculate cell size
    const cellSize = Math.min(dimensions.boundedWidth / nodes.length, dimensions.boundedHeight / nodes.length);

     // Define the color scale for the heatmap
     const colorScale = d3.scaleLinear()
     .domain([0, 1]) // We have 0 (no link) and 1 (link)
     .range(["#eee", "steelblue"]); // Light gray to blue

    // Draw the matrix
    const rows = graphGroup.selectAll(".row")
      .data(nodeOrder)
      .enter().append("g")
      .attr("class", "row")
      .attr("transform", (d, i) => `translate(0,${i * cellSize})`);
    
    const cells = rows.selectAll(".cell")
      .data(source => nodeOrder.map(target => ({source, target})))
      .enter().append("rect")
        .attr("class", "cell")
        .attr("x", d => nodeOrder.indexOf(d.target) * cellSize)
        .attr("width", cellSize)
        .attr("height", cellSize)
        .style("fill", d => colorScale(matrix[d.source][d.target]))
        .style("stroke", "white")
        .style("stroke-width", 1);

    // Add node labels
    rows.append("text")
        .attr("x", -5)
        .attr("y", cellSize / 2)
        .attr("dy", ".32em")
        .attr("text-anchor", "end")
        .text(source => authorLookup[source].name)
        .style("font-size", "0.7rem")
        .style("pointer-events", "none");

    // Add column labels
    const columnLabels = graphGroup.selectAll(".column")
        .data(nodeOrder)
        .enter().append("g")
        .attr("class", "column")
        .attr("transform", (d, i) => `translate(${i * cellSize}, 0)`);
    
    columnLabels.append("text")
        .attr("x", cellSize / 2)
        .attr("y", -5)
        .attr("dy", ".32em")
        .attr("text-anchor", "start")
        .attr("transform", "rotate(-90)")
        .text(target => authorLookup[target].name)
        .style("font-size", "0.7rem")
        .style("pointer-events", "none");
  };

  const clearCanvas = () => {
    const rootGroup = d3.select(canvasRef.current).select("g#root-group");
    rootGroup.selectAll("g").remove();
  };

  useEffect(() => {
    if (graphData === null || !citation) return;
    clearCanvas();
    drawGraph(graphData);
  }, [graphData, author, citation]);

  return (
    <div ref={canvasRef} style={{ height: "100%" }}>
      <svg
        style={{
          width: "100%",
          height: "900px",
        }}
      >
        <g id="root-group" />
      </svg>
    </div>
  );
};

export default AdjacencyMatrixPanel;
