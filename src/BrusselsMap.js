import React, { useRef, useEffect, useState } from "react";
import { select } from "d3";

import { useDataApi } from './api.js'
import { generateColors } from './utils.js'
import { stations, brussels, getTitle, init_map, scale_bar } from './map_utils.js'


const BrusselsMap = ({width, height, geojson, url_api, dataset, title}) => { 
  const [{ data, isLoading, isError }, doFetch] = useDataApi(
    url_api,
    { hits: [] },
  );
  const [colors, setColors] = useState(generateColors([250, 0, 0], [255, 254, 254], 5))
  const svgRef = useRef()

  useEffect(() => {
    const svg = select(svgRef.current);


    const map = init_map(width-400, height-100, geojson);

    const g = svg.append("g")
      .selectAll("path")
      .data(geojson.features)
      .enter()
      .append("path")
      .attr("d", map.path)
      .attr("name", function(d) {return d.properties.NAME_FRE;})
      .attr("stroke", "rgb(100,100,100)")
      .attr("transform", "translate(" + 0 + "," + 40 + ")")
      .style("fill", function(d) {return getColor(d.properties.NAME_FRE);})
      .style("fill-opacity", 1)
    

    const s = stations(svg, map.path);
    s.attr("transform", "translate(" + 0 + "," + 40 + ")");
    const t = getTitle(svg, title, width/4, 150);
    const bxl = brussels(svg, map.path)

    const scale = scale_bar(width, height, map.projection, 0.02, 0.8);
    svg.append("g").call(scale);

    const x_legend = 600;
    const y_legend = 250;
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
      .attr("fill", "rgb(255, 254, 254)")
      .attr("stroke-width", 1)
      .attr("stroke", "rgb(0,0,0)")
      .attr("fill-opacity", 1)

    svg.append("text")
      .attr("x", x_legend+x_text_padding)
      .attr("y", y_legend+y_text_padding)
      .style("fill", "rgb(0,0,0)")
      .style("font-family", "sans-serif")
      .text('< 0.5%');

    svg.append("rect")
      .attr("x", x_legend+x_padding)
      .attr("y", y_legend+y_rect_padding)
      .attr("width", 30)
      .attr("height", 15)
      .attr("fill", "rgb(254, 203, 203)")
      .attr("fill-opacity", 1)

    svg.append("text")
      .attr("x", x_legend+x_text_padding)
      .attr("y", y_legend+2*y_text_padding)
      .style("fill", "rgb(0,0,0)")
      .style("font-family", "sans-serif")
      .text('0.5-1%');
    
    svg.append("rect")
      .attr("x", x_legend+x_padding)
      .attr("y", y_legend+1.75*y_rect_padding)
      .attr("width", 30)
      .attr("height", 15)
      .attr("fill", "rgb(253, 152, 152)")
      .attr("fill-opacity", 1)

    svg.append("text")
      .attr("x", x_legend+x_text_padding)
      .attr("y", y_legend+3*y_text_padding)
      .style("fill", "rgb(0,0,0)")
      .style("font-family", "sans-serif")
      .text('1-1.5%');
    
    svg.append("rect")
      .attr("x", x_legend+x_padding)
      .attr("y", y_legend+2.5*y_rect_padding)
      .attr("width", 30)
      .attr("height", 15)
      .attr("fill", "rgb(252, 102, 102)")
      .attr("fill-opacity", 1)

    svg.append("text")
      .attr("x", x_legend+x_text_padding)
      .attr("y", y_legend+4*y_text_padding)
      .style("fill", "rgb(0,0,0)")
      .style("font-family", "sans-serif")
      .text('1.5-2%');
    
      svg.append("rect")
      .attr("x", x_legend+x_padding)
      .attr("y", y_legend+3.2*y_rect_padding)
      .attr("width", 30)
      .attr("height", 15)
      .attr("fill", "rgb(251, 51, 51)")
      .attr("fill-opacity", 1)

    svg.append("text")
      .attr("x", x_legend+x_text_padding)
      .attr("y", y_legend+5*y_text_padding)
      .style("fill", "rgb(0,0,0)")
      .style("font-family", "sans-serif")
      .text('>2%');
    
    
    svg.append("circle")
      .attr("cx", x_legend+2*x_padding)
      .attr("cy", y_legend+4.1*y_rect_padding)
      .attr("r", 8)
      .attr("fill", "rgb(10, 10, 10)")
      .attr("fill-opacity", 0.7)
    
    svg.append("text")
      .attr("x", x_legend+x_text_padding)
      .attr("y", y_legend+6*y_text_padding)
      .style("fill", "rgb(0,0,0)")
      .style("font-family", "sans-serif")
      .text('Principales gares')

    const legend = svg.append("rect")
      .attr("x", x_legend)
      .attr("y", y_legend)
      .attr("width", 200)
      .attr("height", 7*y_text_padding)
      .attr("stroke-width", 3)
      .attr("stroke", "rgb(0,0,0)")
      .attr("fill-opacity", 0)
  });

  const getColor = (name) => {
    if(data[dataset]) {
      for (let i = 0; i < data[dataset].length; i++) {
          if(data[dataset][i]["name"] == name) {
            var percent = data[dataset][i]["percent"]/0.5
            console.log(Math.round(percent))
            if (Math.round(percent) < 5){
              return colors[Math.round(percent)]
            } else {
              return colors[3]
            }
            
          }
        }
      }
  };

  return <svg width={width} height={height} ref={svgRef}></svg>;   
}

export default BrusselsMap;

/*
  const getColor = (name) => {
    if(data[dataset]) {
      for (let i = 0; i < data[dataset].length; i++) {
          if(data[dataset][i]["name"] == name) {
            var percent = data[dataset][i]["percent"]
            if (Math.floor(percent/2) < 5){
              return colors[Math.floor(percent/2)]
            } else {
              return colors[4]
            }
            
          }
        }
      }
  };
  */