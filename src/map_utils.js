import { geoMercator, geoPath } from "d3-geo";
import { geoScaleBar } from 'd3-geo-scale-bar';
import * as d3 from 'd3'

import way from "./geojson/railway.json";
import routes from "./geojson/autoroutes.json";
import gares from "./geojson/gare.json";
import bxl from "./geojson/brussels.json";

export const colors_districts = {
	"Province de Liège": "#0D8000",
	"Province de Namur": "#3B9F00",
  	"Province de Hainaut": "#78BF00",
	"Province de Brabant wallon": "#C4DF00",
	"Province de Luxembourg":"#FFE000",
	"Province de Brabant flamand":"#FF7F2A",
	"Province de Limbourg": "#FF545C",
	"Province d’Anvers": "#FF7EC5",
	"Province de Flandre orientale": "#FFA8FF",
	"Province de Flandre occidentale": "#E9D2FF"
};

export const districts = {
    "Bruxelles": "Région de Bruxelles-Capitale",
    "Liège": "Province de Liège",
    "Namur": "Province de Namur",
    "Hainaut":"Province de Hainaut",
    "Brabant Wallon": "Province de Brabant wallon",
    "Luxembourg": "Province de Luxembourg",
    "Brabant Flammand": "Province de Brabant flamand",
    "Limbourg": "Province de Limbourg",
    "Anvers": "Province d’Anvers",
    "Flandre Orientale": "Province de Flandre orientale",
    "Flandre Occidentale": "Province de Flandre occidentale"     
};

export const invers_districts = {
    "Région de Bruxelles-Capitale":"Bruxelles",
    "Province de Liège": "Liège",
    "Province de Namur": "Namur",
    "Province de Hainaut": "Hainaut",
    "Province de Brabant wallon": "Brabant Wallon",
    "Province de Luxembourg":"Luxembourg",
    "Province de Brabant flamand":"Brabant Flammand",
    "Province de Limbourg": "Limbourg",
    "Province d’Anvers": "Anvers",
    "Province de Flandre orientale": "Flandre Orientale",
    "Province de Flandre occidentale": "Flandre Occidentale"
};

export function init_map(width, height, base) {
    const projection = geoMercator().fitSize([width, height], base);
    const path = geoPath(projection);

    return {
        projection,
        path
    };
}

export function brussels(svg, path) {
    const r = svg.append("g")
        .selectAll("path")
        .data(bxl.features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("stroke-width", 1.7)
        .attr("stroke", "rgb(10, 10, 10)")
        .attr("transform", "translate(" + 0 + "," + 40 + ")")
        .attr("stroke-opacity", 0.5)
        .attr("fill-opacity", 0);

    return r;
};

export function railway(svg, path) {
    const r = svg.append("g")
        .selectAll("path")
        .data(way.features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("stroke-width", 1)
        .attr("stroke", "rgb(255, 10, 10)")
        .attr("stroke-opacity", 0.7)
        .attr("fill-opacity", 0);

    return r;
};

export function autoroutes(svg, path) {
    const a = svg.append("g")
        .selectAll("path")
        .data(routes.features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("stroke-width", 3)
        .attr("stroke", "rgb(20,220,60)")
        .attr("stroke-opacity", .3)
        .attr("fill-opacity", 0);

    return a;
};

export function stations(svg, path) {
    const r = svg.append("g")
        .selectAll("path")
        .data(gares.features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("stroke-width", 5)
        .attr("stroke", "rgb(10, 10, 10)")
        .attr("stroke-opacity", 0.7)
        .attr("fill-opacity", 1);

return r;
}

export function getTitle(svg, name, x, y) {
    const t = svg.append("text")
        .attr("x", x)
        .attr("y", y)
        .style("fill", "rgb(0,0,0)")
        .style("font-family", "sans-serif")
        .style("font-size", "x-large")
        .text(name);

    return t;
};

export function scale_bar(width, height, projection, x, y) {
    const scaleBar = geoScaleBar()
        .projection(projection)
        .size([width, height])
        .label("Kilomètres")
        .left(x)
        .top(y);
    
    return scaleBar;
}

export function grid(chart, left, axe, width) {
    chart.append('g')
		.attr('class', 'grid')
		.attr('transform', `translate(${left}, 0)`)
		.call(d3.axisLeft()
		.scale(axe)
		.tickSize(-width + left, 0, 100)
		.tickFormat(''))
}
