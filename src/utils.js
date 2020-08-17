function getRGBString(rgb_list) {
    let color;
    if(rgb_list.length === 4) {
      color = 'rgb(' + rgb_list[0] + ', ' + rgb_list[1] + ', ' + rgb_list[2] + ', ' + rgb_list[3] + ')';
    } else {
      color = 'rgb(' + rgb_list[0] + ', ' + rgb_list[1] + ', ' + rgb_list[2] + ')';
    }
    return color;
  }


export function generateColors(colorStart, colorEnd, colorCount) {
	var start = colorStart;    
	var end = colorEnd;    
	var len = colorCount;
	var alpha = 0.0;

	var colors = [];
	for(var i = 0; i < len; i++) {
		var c = [];
		c[0] = Math.round(start[0] * alpha + (1 - alpha) * end[0]);
		c[1] = Math.round(start[1] * alpha + (1 - alpha) * end[1]);
        c[2] = Math.round(start[2] * alpha + (1 - alpha) * end[2]);
        alpha += (1.0/len);
		colors.push(getRGBString(c));
	}

	return colors;
}

export function getSeries(data, districts) {
	var series = [];
	var count_cities = []
	for(var d in districts) {
		var district = [];
		for(var c in data["resident"]) {
			if(data["resident"][c][districts[d]] > 0) {
				var city = [];
				city["name"] = data["resident"][c]["name"];
				city["district"] = districts[d]

				if(data["resident"][c]["name"] in count_cities) {
					city["begin"] = count_cities[data["resident"][c]["name"]]
					city["end"] = count_cities[data["resident"][c]["name"]] + data["resident"][c][districts[d]]
					count_cities[data["resident"][c]["name"]] += data["resident"][c][districts[d]]
				} else {
					city["begin"] = 0
					city["end"] = data["resident"][c][districts[d]]
					count_cities[data["resident"][c]["name"]] = data["resident"][c][districts[d]]
				}
				district.push(city)
			}
		}	
		series.push(district)
	}	
	return series;				
}