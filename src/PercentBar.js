import React, { useRef, useEffect, useState } from "react";
import * as d3 from 'd3'
import { select } from "d3";
import { useDataApi } from './api.js'
import {invers_districts} from './map_utils'


const PercentBar = ({width, height, url, dataset, title, scale}) => { 
  	const [{ data, isLoading, isError }, doFetch] = useDataApi(
		url, { hits: [] });
	const svgRef = useRef();
	
	useEffect(() => {
		if(data[dataset]) {
		const margin = 200;
		width = width - 2 * margin;
		height = height - 2 * margin;
		const svg = select(svgRef.current);
		
		const chart = svg.append('g')
    		.attr('transform', `translate(${margin}, ${margin})`);
		
		const yScale = d3.scaleLinear()
    		.range([height, 0])
			.domain([0, scale]);
		
		chart.append('g')
			.call(d3.axisLeft(yScale));

		function a(name) {
			if(invers_districts[name]) {
				return invers_districts[name]
			} else { return name}
		}
		
		const xScale = d3.scaleBand()
    		.range([0, width])
    		.domain(data[dataset].map((s) => a(s.name)))
			.padding(0.2);

		chart.append('g')
    		.attr('transform', `translate(0, ${height})`)
			.call(d3.axisBottom(xScale))
			.selectAll("text")
			.attr("x", 9)
			.attr("y", -5)
    		.attr("transform", "rotate(90)")
			.style("text-anchor", "start");
		
		chart.selectAll()
			.data(data[dataset])
			.enter()
			.append('rect')
			.attr('x', (s) => xScale(a(s.name)))
			.attr('y', (s) => yScale(s.percent))
			.attr('height', (s) => height - yScale(s.percent))
			.attr('width', xScale.bandwidth())
			.attr("fill", "rgb(15, 157, 232)")
			.attr("fill-opacity", 0.7)
			
		
		chart.append('g')
			.attr('class', 'grid')
			.call(d3.axisLeft()
				.scale(yScale)
				.tickSize(-width, 0, 0)
				.tickFormat(''))
		
		svg.append('text')
				.attr('x', -(height / 2) - margin)
				.attr('y', 2*margin / 2.4)
				.attr('transform', 'rotate(-90)')
				.attr('text-anchor', 'middle')
				.text("Nombre de travailleurs entrants (%)")
			
		svg.append('text')
				.attr('x', width / 2 + margin)
				.attr('y', margin-20)
				.attr('text-anchor', 'middle')
				.text(title)
			
		}
	});


  return <svg width={width} height={height} ref={svgRef}></svg>;   
}

export default PercentBar;