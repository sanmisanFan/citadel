import { useEffect, useRef } from "react";
import * as d3 from "d3";

const AuthorGraph = ({ 
  graphData, 
  author 
}) => {
  const canvasRef = useRef(null);

  const drawGraph = () => {
    const { scrollWidth, scrollHeight } = canvasRef.current;
    let dimensions = {
      width: scrollWidth,
      height: scrollHeight,
      margin: {
        top: 0,
        right: 0,
        bottom: 0,
        left: 0,
      },
    };
    dimensions.boundedWidth =
      dimensions.width - dimensions.margin.left - dimensions.margin.right;
    dimensions.boundedHeight =
      dimensions.height - dimensions.margin.top - dimensions.margin.bottom;

    const svgRoot = d3.select(canvasRef.current).select("svg");
    const rootGroup = svgRoot.select("g#root-group");

    // Create a group for the graph within the root group
    const graphGroup = rootGroup
      .append("g")
      .attr("id", "graph-group")
      .attr(
        "transform",
        `translate(${dimensions.margin.left}, ${dimensions.margin.top})`
      );

    // Add arrowheads
    svgRoot
      .append("defs")
      .append("marker")
      .attr("id", "arrowhead")
      .attr("viewBox", "-0 -5 10 10")
      .attr("refX", 13) // Adjust this value to move the arrowhead along the line
      .attr("refY", 0)
      .attr("orient", "auto")
      .attr("markerWidth", 8)
      .attr("markerHeight", 8)
      .attr("xoverflow", "visible")
      .append("svg:path")
      .attr("d", "M 0,-5 L 10 ,0 L 0,5")
      .attr("fill", "#999")
      .style("stroke", "none");

    // Create a force simulation
    const simulation = d3
      .forceSimulation(graphData.nodes)
      .force(
        "link",
        d3
          .forceLink(graphData.links)
          .id((d) => d.id)
          .distance(30)
      )
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(dimensions.boundedWidth / 2, dimensions.boundedHeight / 2))
      .force("collide", d3.forceCollide().radius(40))
      .force("x", d3.forceX())
      .force("y", d3.forceY());

    // Create links
    const link = graphGroup
      .append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(graphData.links)
      .join("line")
      .attr("stroke-width", 1)
      .attr("marker-end", "url(#arrowhead)"); // Add arrowhead to links


     // Create self-loop links
     const selfLoopLinks = graphGroup.append("g")
     .selectAll("path.loop")
     .data(graphData.links.filter(d => d.source === d.target))
     .join("path")
     .attr("class", "loop")
     .attr("fill", "none")
     .attr("stroke", "#999")
     .attr("stroke-width", 1)
     .attr("marker-end", "url(#arrowhead)");

    // Create nodes
    const node = graphGroup
      .append("g")
      .selectAll("g")
      .data(graphData.nodes)
      .join("g")
      .attr("cursor", "pointer");

    // Append circles to nodes
    node
      .append("circle")
      .attr("r", 5)
      .attr("fill", "steelblue")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1);

    // Append labels to nodes
    node
      .append("text")
      .text((d) => d.name)
      .attr("x", 18)
      .attr("y", 5)
      .style("font-size", "0.8rem")
      .style("pointer-events", "none");

    // Dragging behavior
    const drag = (simulation) => {
      function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.1).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      }

      function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }

      function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }

      return d3
        .drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
    };

    node.call(drag(simulation));

    // Update positions on each tick of the simulation
    simulation.on("tick", () => {
       link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      node.attr("transform", (d) => `translate(${d.x},${d.y})`);

      // Update self-loop link positions
       selfLoopLinks.attr("d", (d) => {
          const radius = 20;
          const dx = d.target.x;
          const dy = d.target.y;
          return `M${dx},${dy} A${radius},${radius} 0 1,1 ${dx - 0.01},${dy}`;
       });
    });
  };

  const clearCanvas = () => {
    const rootGroup = d3.select(canvasRef.current).select("g#root-group");
    rootGroup.selectAll("g").remove();
  };

  useEffect(() => {
    if (graphData === null) return;
    clearCanvas();
    drawGraph();
  }, [graphData, author]);

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

export default AuthorGraph;
