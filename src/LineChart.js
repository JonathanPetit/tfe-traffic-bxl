import React, { useRef, useEffect, useState } from "react";
import * as d3 from 'd3'
import { select, line } from "d3";
import { useDataApi } from './api.js'

const LineChart = ({width, height, url, dataset}) => {
  const [{ data, isLoading, isError }, doFetch] = useDataApi(
	  url, { hits: [] });
  const svgRef = useRef();
    
  useEffect(() => {
    if(data[dataset]) {
      console.log(data[dataset])
      const margin = 200;
      width = width - 2 * margin;
      height = height - 2 * margin;
      const svg = select(svgRef.current);

      const chart = svg.append('g')
        .attr('transform', `translate(${margin}, ${margin})`);
      
      const yScale = d3.scaleLinear()
        .range([height, margin])
        .domain([0, d3.max(data[dataset], d => d.percent_gain)]).nice();
    
      svg.append('g')
        .attr("transform", `translate(${margin}, 0)` )
        .call(d3.axisLeft(yScale));
      
      const xScale = d3.scaleLinear()
        .range([margin, width])
        .domain([0, d3.max(data[dataset], d => d.percent_influent)]).nice();
      
      svg.append('g')
        .attr('transform', `translate(0, ${height})`)
        .call(d3.axisBottom(xScale));
        // Add the line
      svg.append("path")
			  .datum(data[dataset])
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2)
        .attr("d", d3.line()
        .x(function(d) { return xScale(d.percent_influent) })
        .y(function(d) { return yScale(d.percent_gain) }))
      
      svg.append('g')
        .attr('class', 'grid')
        .attr('transform', `translate(${margin}, 0)`)
        .attr("fill-opacity", 0.3)
        .call(d3.axisLeft()
          .scale(yScale)
          .tickSize(-width+margin, 0, 0)
          .tickFormat(''))
      
      svg.append('g')
          .attr('class', 'grid')
          .attr('transform', `translate(0, ${margin})`)
          .attr("fill-opacity", 0.3)
          .call(d3.axisBottom()
            .scale(xScale)
            .tickSize(height-margin, 0, 0)
            .tickFormat(''))

      svg.append('text')
        .attr('x', -(height / 2) - margin/2)
        .attr('y', 2*margin / 2.4)
        .attr('transform', 'rotate(-90)')
        .attr('text-anchor', 'middle')
        .text("Gain de voitures en RBC (%)")

      svg.append('text')
				.attr('x', width/2 + margin/2)
				.attr('y', height + margin/4)
				.attr('text-anchor', 'middle')
				.text("Diminution voitures de sociétés (%)")
      
    }
  });

  return <svg width={width} height={height} ref={svgRef}></svg>;   
}
  
export default LineChart;