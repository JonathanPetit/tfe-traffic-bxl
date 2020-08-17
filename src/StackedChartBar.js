import React, { useRef, useEffect, useState } from "react";
import * as d3 from 'd3'
import { select } from "d3";
import { useDataApi } from './api.js';
import { getSeries } from './utils.js';
import { grid } from "./map_utils.js";


const StackedChartBar = ({width, height, url_api, colors, info}) => { 
  const [{ data, isLoading, isError }, doFetch] = useDataApi(
		url_api, { hits: [] });
	const svgRef = useRef();
	
	useEffect(() => {
		if(data["resident"]) {
			const margin = ({top: 100, right: 10, bottom: 200, left: 100})
			const svg = select(svgRef.current);

			const chart = svg.append('g')
    			.attr('transform', `translate(${margin}, ${margin})`);
		
			const yScale = d3.scaleLinear()
				.rangeRound([height - margin.bottom, margin.top])
				.domain([0, 40]);
			
			chart.append('g')
				.attr("transform", `translate(${margin.left},0)`)
				.call(d3.axisLeft(yScale));
			
			const xScale = d3.scaleBand()
    			.range([margin.left, width - margin.right])
    			.domain(data["resident"].map((s) => s.name))
				.padding(0.1);
		
			chart.append('g')
				.attr('transform', `translate(0, ${height - margin.bottom})`)
				.call(d3.axisBottom(xScale))
				.selectAll("text")
				.attr("x", 9)
				.attr("y", -5)
				.attr("transform", "rotate(90)")
				.style("text-anchor", "start");
			
			const series = getSeries(data, info);
			svg.append("g")
				.selectAll("g")
				.data(series)
				.join("g")
					.selectAll("rect")
					.data(d => d)
					.join("rect")
		  			.attr("x", (d, i) => xScale(d.name))
		  			.attr("y", d => yScale(d.end))
		  			.attr("height", d => yScale(d.begin) - yScale(d.end))
					.attr("width", xScale.bandwidth())
					.attr("fill", d => colors[d.district])
		  
			const gr = grid(chart, margin.left, yScale, width)
		
			svg.append('text')
				.attr('x', -height/2 + margin.bottom/2)
				.attr('y', margin.left-50)
				.attr('transform', 'rotate(-90)')
				.attr('text-anchor', 'middle')
				.text("Nombre de travailleurs entrants (%)")
			
			svg.append('text')
				.attr('x', width / 2 + margin.left)
				.attr('y', margin.top-20)
				.attr('text-anchor', 'middle')
				.text('Lieux de travail des navetteurs entrants')	

			const x_legend = 778;
			const y_legend = 100;
    		const x_padding = 10;
    		const y_padding = 20;
    		const x_text_padding = 50;
    		const y_text_padding = 20;
			const y_rect_padding = 35;
			
			var count = 1;


			const legend = svg.append("rect")
				.attr("x", x_legend)
				.attr("y", y_legend)
				.attr("width", 320)
				.attr("height", 11*y_text_padding)
				.attr("stroke-width", 3)
				.attr("stroke", "rgb(0,0,0)")
				.attr("fill", "rgb(255,255,255)")
				.attr("fill-opacity", 1)

			for(var i in colors) {
				svg.append("rect")
					.attr("x", x_legend+x_padding)
					.attr("y", y_legend+(count)*y_padding-10)
					.attr("width", 30)
					.attr("height", 15)
					.attr("fill", d => colors[i])
					.attr("stroke-width", 1)
					.attr("stroke", "rgb(0,0,0)")
					.attr("fill-opacity", 1)
		  
			  	svg.append("text")
					.attr("x", x_legend+x_text_padding)
					.attr("y", y_legend+15+(count)*y_text_padding-10)
					.style("fill", "rgb(0,0,0)")
					.style("font-family", "sans-serif")
					.text(i);
				count+=1
			} 

		}
	});


  return <svg width={width} height={height} ref={svgRef}></svg>;   
}

export default StackedChartBar;