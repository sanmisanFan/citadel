import { useEffect, useRef } from "react";
import * as d3 from "d3";

const AdjacencyMatrixPanel = ({ graphData, author, citation }) => {
  const canvasRef = useRef(null);

  const drawGraph = () => {
    if (!graphData || !graphData.nodes || !graphData.links || graphData.nodes.length === 0) {
      return; // Exit if data is invalid or empty
    }
    const { scrollWidth, scrollHeight } = canvasRef.current;
    let dimensions = {
      width: scrollWidth,
      height: scrollHeight,
      margin: {
        top: 110, // Increased top margin for labels
        right: 50,
        bottom: 10,
        left: 150, // Increased left margin for labels
      },
    };
    dimensions.boundedWidth =
      dimensions.width - dimensions.margin.left - dimensions.margin.right;
    dimensions.boundedHeight =
      dimensions.height - dimensions.margin.top - dimensions.margin.bottom;

    const svgRoot = d3.select(canvasRef.current).select("svg");
    const rootGroup = svgRoot.select("g#root-group");

    // Clear previous content
    rootGroup.selectAll("*").remove();

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
    if (nodes.length === 0) return;

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
        matrix[link.source][link.target] = link.value; // Increment the count for each link
      }
    });

    // Function to calculate the degree of each node
    const calculateNodeDegree = (matrix) => {
      const degree = {};
      for (const source in matrix) {
        degree[source] = 0;
        for (const target in matrix[source]) {
          degree[source] += matrix[source][target];
        }
      }
      return degree;
    };

    // Calculate node degrees
    const nodeDegree = calculateNodeDegree(matrix);
    //console.log(matrix);

    // Sort nodes by degree (descending) and then alphabetically
    nodes.sort((a, b) => {
      const degreeDiff = nodeDegree[b.id] - nodeDegree[a.id];
      if (degreeDiff !== 0) {
        return degreeDiff;
      }
      return a.name.localeCompare(b.name);
    });

    // Sorted node order
    const nodeOrder = nodes.map(node => node.id);
    //console.log(nodeOrder);

    // Calculate cell size
    const cellSize = Math.min(dimensions.boundedWidth / nodes.length, dimensions.boundedHeight / nodes.length);

    // Define the color scale for the heatmap
    const colorScheme = ['#eee', '#c6dbef','#9ecae1','#6baed6','#3182bd','#08519c'];
    const colorSchemeCluster = ['#eee', '#fcc5c0','#fa9fb5','#f768a1','#dd3497','#ae017e'];

    const colorScale = d3.scaleThreshold()
    .domain([1, 2, 3, 5, 10])
    .range(colorScheme);

    const colorScaleCluster = d3.scaleThreshold()
    .domain([1, 2, 3, 5, 10])
    .range(colorSchemeCluster);

    // Create scales for x and y axes
    const xScale = d3.scaleBand()
      .domain(nodeOrder)
      .range([0, nodeOrder.length * cellSize]);

    const yScale = d3.scaleBand()
      .domain(nodeOrder)
      .range([0, nodeOrder.length * cellSize]);

    // Create a group for the graph within the root group
    const graphGroup = rootGroup
      .append("g")
      .attr("id", "graph-group")
      .attr(
        "transform",
        `translate(${dimensions.margin.left}, ${dimensions.margin.top})`
      );

    // Draw the matrix
    const rows = graphGroup.selectAll(".row")
      .data(nodeOrder)
      .enter().append("g")
      .attr("class", "row")
      .attr("transform", (d, i) => `translate(0,${yScale(d)})`);

    const cells = rows.selectAll(".cell")
      .data(source => nodeOrder.map(target => ({ source, target })))
      .enter().append("rect")
      .attr("class", "cell")
      .attr("x", d => xScale(d.target))
      .attr("width", xScale.bandwidth())
      .attr("height", yScale.bandwidth())
      .style("fill", d => {
        const hasIssue = citation.some(cite => 
          cite.author.includes(d.target) && 
          cite.has_issue === true
        );
        return hasIssue ? colorScaleCluster(matrix[d.source][d.target]) : colorScale(matrix[d.source][d.target]);
      })
      .style("stroke", "white")
      .style("stroke-width", 1)
      .on("mouseover", function(event, d) {
        d3.select(this).style("stroke", "black").style("stroke-width", 2);
        d3.selectAll(`.row text`).filter(text => text === d.source).style("font-weight", "bold");
        d3.selectAll(`.column text`).filter(text => text === d.target).style("font-weight", "bold");
      })
      .on("mouseout", function(event, d) {
        d3.select(this).style("stroke", "white").style("stroke-width", 1);
        d3.selectAll(`.row text`).filter(text => text === d.source).style("font-weight", "normal");
        d3.selectAll(`.column text`).filter(text => text === d.target).style("font-weight", "normal");
      });

    // Add citation text to each cell
    rows.selectAll(".cell-text")
      .data(source => nodeOrder.map(target => ({ source, target })))
      .enter().append("text")
      .attr("class", "cell-text")
      .attr("x", d => xScale(d.target) + xScale.bandwidth() / 2)
      .attr("y", yScale.bandwidth() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "middle")
      .text(d => matrix[d.source][d.target] > 0 ? matrix[d.source][d.target] : "")
      .style("font-size", "0.5rem")
      .style("pointer-events", "none");

    // Add node labels
    rows.append("text")
      .attr("x", -5)
      .attr("y", yScale.bandwidth() / 2)
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
      .attr("transform", (d, i) => `translate(${xScale(d)}, 0)`);

    columnLabels.append("text")
      .attr("x", 5)
      .attr("y", xScale.bandwidth() / 2 - 5)
      .attr("dy", ".32em")
      .attr("text-anchor", "start")
      .attr("transform", "rotate(-65)")
      .text(target => authorLookup[target].name)
      .style("font-size", "0.7rem")
      .style("pointer-events", "none");

    // Brush
    /*const brush = d3.brush()
      .extent([[0, 0], [xScale.range()[1], yScale.range()[1]]])
      .on("start brush end", brushed);

    graphGroup.append("g")
      .attr("class", "brush")
      .call(brush);

    function brushed({ selection }) {
      if (selection) {
        const [[x0, y0], [x1, y1]] = selection;
        const selectedNodes = new Set();
        cells.classed("selected", d => {
          const x = xScale(d.target);
          const y = yScale(d.source);
          const isSelected = x0 <= x && x < x1 && y0 <= y && y < y1;
          if (isSelected) {
            selectedNodes.add(d.source);
            selectedNodes.add(d.target);
          }
          return isSelected;
        });

        // Highlight labels
        rows.selectAll("text").classed("selected", d => selectedNodes.has(d));
        columnLabels.selectAll("text").classed("selected", d => selectedNodes.has(d));

      } else {
        cells.classed("selected", false);
        rows.selectAll("text").classed("selected", false);
        columnLabels.selectAll("text").classed("selected", false);
      }
    }*/
  };

  const clearCanvas = () => {
    const rootGroup = d3.select(canvasRef.current).select("g#root-group");
    rootGroup.selectAll("g").remove();
  };

  useEffect(() => {
    if (graphData === null || !citation) return;
    clearCanvas();
    drawGraph();
  }, [graphData, author, citation]);

  return (
    <div ref={canvasRef} style={{ height: "100%" }}>
      <svg
        style={{
          width: "100%", 
          height: "950px",
        }}
      >
        <g id="root-group" />
      </svg>
    </div>
  );
};

export default AdjacencyMatrixPanel;
