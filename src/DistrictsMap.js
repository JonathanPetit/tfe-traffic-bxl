import React, { useRef, useEffect, useState } from "react";
import * as d3 from 'd3'
import { select } from "d3";
import { geoMercator, geoPath } from "d3-geo";
import { geoScaleBar } from 'd3-geo-scale-bar'

import { useDataApi } from './api.js'
//import { generateColors } from './utils.js'

import { railway, autoroutes, getTitle } from './map_utils.js'


const DistrictsMap = ({width, height, geojson}) => { 
  const [{ data, isLoading, isError }, doFetch] = useDataApi(
    'http://127.0.0.1:5002/citiesWithoutRBC',
    { hits: [] },
  );
  const svgRef = useRef()

  useEffect(() => {
    const projection = geoMercator().fitSize([width, height], geojson);
    const path = geoPath(projection);
    const svg = select(svgRef.current);

    const g = svg.append("g")
      .selectAll("path")
      .data(geojson.features)
      .enter()
      .append("path")
      .attr("d", path)
      .attr("name", function(d) {return d.properties.name;})
      .attr("stroke", "rgb(100,100,100)")
      .style("fill", "rgb(250,250,250)")
      .style("fill-opacity", 1);
    
    const r = railway(svg, path);
    const a = autoroutes(svg, path);
    const t = getTitle(svg, "Navetteurs entrants en Région Bruxelloise", width/4, 70);
		
		if(data["cities"]) {
      svg.selectAll("myCircles")
        .data(data["cities"])
        .enter()
        .append("circle")
        .attr("cx", function(d) {return projection([d.longitude, d.latitude])[0]})
        .attr("cy", function(d) {return projection([d.longitude, d.latitude])[1]})
        .attr("r", function(d) {return getRadius(d.people)})
        .style("fill", "rgb(10, 10, 10)")
        .attr("stroke-width", 3)
        .attr("fill-opacity", .7)
      
    const scaleBar = geoScaleBar()
        .projection(projection)
        .size([width, height])
        .label("Kilomètres")
        .left(.02)
        .top(.80)
    
    svg.append("g").call(scaleBar);
  }

    const x_legend = 10;
    const y_legend = height*0.6;
    const x_padding = 10;
    const y_padding = 10;
    const x_text_padding = 50;
    const y_text_padding = 25;
    const y_rect_padding = 35;

    svg.append("rect")
      .attr("x", x_legend+x_padding)
      .attr("y", y_legend+y_padding)
      .attr("width", 30)
      .attr("height", 15)
      .attr("fill", "rgb(20,220,60)")
      .attr("fill-opacity", 1)

    svg.append("text")
      .attr("x", x_legend+x_text_padding)
      .attr("y", y_legend+y_text_padding)
      .style("fill", "rgb(0,0,0)")
      .style("font-family", "sans-serif")
      .text('Autoroutes');

    svg.append("rect")
      .attr("x", x_legend+x_padding)
      .attr("y", y_legend+y_rect_padding)
      .attr("width", 30)
      .attr("height", 15)
      .attr("fill", "rgb(220,20,60)")
      .attr("fill-opacity", 1)

    svg.append("text")
      .attr("x", x_legend+x_text_padding)
      .attr("y", y_legend+2*y_text_padding)
      .style("fill", "rgb(0,0,0)")
      .style("font-family", "sans-serif")
      .text('Lignes ferroviaires');
    
    svg.append("circle")
      .attr("cx", x_legend+2*x_padding)
      .attr("cy", y_legend+2*y_rect_padding)
      .attr("r", 2)
      .attr("fill", "rgb(10, 10, 10)")
      .attr("fill-opacity", 0.7)
    
    svg.append("text")
      .attr("x", x_legend+x_text_padding)
      .attr("y", y_legend+3*y_text_padding)
      .style("fill", "rgb(0,0,0)")
      .style("font-family", "sans-serif")
      .text('500-1000 navetteurs entrants');
    
    svg.append("circle")
      .attr("cx", x_legend+2*x_padding)
      .attr("cy", y_legend+2.7*y_rect_padding)
      .attr("r", 4)
      .attr("fill", "rgb(10, 10, 10)")
      .attr("fill-opacity", 0.7)
    
    svg.append("text")
      .attr("x", x_legend+x_text_padding)
      .attr("y", y_legend+4*y_text_padding)
      .style("fill", "rgb(0,0,0)")
      .style("font-family", "sans-serif")
      .text('1000-2000 navetteurs entrants');

    svg.append("circle")
      .attr("cx", x_legend+2*x_padding)
      .attr("cy", y_legend+3.4*y_rect_padding)
      .attr("r", 8)
      .attr("fill", "rgb(10, 10, 10)")
      .attr("fill-opacity", 0.7)
    
    svg.append("text")
      .attr("x", x_legend+x_text_padding)
      .attr("y", y_legend+5*y_text_padding)
      .style("fill", "rgb(0,0,0)")
      .style("font-family", "sans-serif")
      .text('2000-4000 navetteurs entrants');
    
    svg.append("circle")
      .attr("cx", x_legend+2*x_padding)
      .attr("cy", y_legend+4.1*y_rect_padding)
      .attr("r", 12)
      .attr("fill", "rgb(10, 10, 10)")
      .attr("fill-opacity", 0.7)
    
    svg.append("text")
      .attr("x", x_legend+x_text_padding)
      .attr("y", y_legend+6*y_text_padding)
      .style("fill", "rgb(0,0,0)")
      .style("font-family", "sans-serif")
      .text('>4000 navetteurs entrants');
    
    const legend = svg.append("rect")
      .attr("x", x_legend)
      .attr("y", y_legend)
      .attr("width", 350)
      .attr("height", 7*y_text_padding)
      .attr("stroke-width", 3)
      .attr("stroke", "rgb(0,0,0)")
      .attr("fill-opacity", 0)
  });


  const getRadius = (people) => {
    if(data["cities"]) {
      if(Math.ceil(people/500) === 1) {
        return 0
      }
      return Math.ceil(people/500)
    }
  };

  return <svg width={width} height={height} ref={svgRef}></svg>;   
}

export default DistrictsMap;