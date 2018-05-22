var margin = {
	top: 20,
	right: 20,
	bottom: 35,
	left: 50
};

var width  = 500 - margin.left - margin.right;
var height = 250 - margin.top - margin.bottom;

var range = logspace(0,3,5000);

var x = d3.scale.log()
	.domain([1, range[range.length-1].toFixed()])
	.range([0, width]);

var xGrid = d3.svg.axis()
	.scale(x)
	.orient("bottom")
	.ticks(5)
	.tickSize(-height, -height, 0)
	.tickFormat("");

var magY = d3.scale.linear()
	.domain([0, 7])
	.range([height, 0]);

var magXAxis1 = d3.svg.axis()
	.scale(x)
	.orient("bottom")
	.ticks(1,"0.1s")
	.innerTickSize(-6)
	.outerTickSize(0)
	.tickPadding(7)
	.tickFormat("");

var magYAxis1 = d3.svg.axis()
	.scale(magY)
	.orient("left")
	.ticks(5)
	.innerTickSize(-6)
	.outerTickSize(0)
	.tickPadding(7);

var magXAxis2 = d3.svg.axis()
	.scale(x)
	.orient("top")
	.ticks(5)
	.innerTickSize(-6)
	.tickPadding(-20)
	.outerTickSize(0)
	.tickFormat("");

var magYAxis2 = d3.svg.axis()
	.scale(magY)
	.orient("left")
	.ticks(5)
	.innerTickSize(6)
	.tickPadding(-20)
	.outerTickSize(0)
	.tickFormat("");

var magYGrid = d3.svg.axis()
	.scale(magY)
	.orient("left")
	.ticks(5)
	.tickSize(-width, -width, 0)
	.tickFormat("");

var magLine = d3.svg.line()
	.x(function(d) { return x(d.x); })
	.y(function(d) { return magY(d.y); })
	.interpolate("linear");
  
var magZoom = d3.behavior.zoom()
	.x(x)
	.y(magY)
	.scaleExtent([1, 1])
	.on("zoom",redraw);
	
var phsY = d3.scale.linear()
	.domain([0, 45])
	.range([height, 0]);

var phsXAxis1 = d3.svg.axis()
	.scale(x)
	.orient("bottom")
	.ticks(1,"0.1s")
	.innerTickSize(-6)
	.outerTickSize(0)
	.tickPadding(7);

var phsYAxis1 = d3.svg.axis()
	.scale(phsY)
	.orient("left")
	.ticks(5)
	.innerTickSize(-6)
	.outerTickSize(0)
	.tickPadding(7);

var phsXAxis2 = d3.svg.axis()
	.scale(x)
	.orient("top")
	.ticks(5)
	.innerTickSize(-6)
	.tickPadding(-20)
	.outerTickSize(0)
	.tickFormat("");

var phsYAxis2 = d3.svg.axis()
	.scale(phsY)
	.orient("left")
	.ticks(5)
	.innerTickSize(6)
	.tickPadding(-20)
	.outerTickSize(0)
	.tickFormat("");

var phsYGrid = d3.svg.axis()
	.scale(phsY)
	.orient("left")
	.ticks(5)
	.tickSize(-width, -width, 0)
	.tickFormat("");

var phsLine = d3.svg.line()
	.x(function(d) { return x(d.x); })
	.y(function(d) { return phsY(d.y); })
	.interpolate("linear");
  
var phsZoom = d3.behavior.zoom()
	.x(x)
	.y(phsY)
	.scaleExtent([1, 1])
	.on("zoom",redraw);

// Create plot
var plotMag = d3.select("#plotmag").append("svg")
	.attr("width",width + margin.left + margin.right)
	.attr("height",height + margin.top + margin.bottom)
	.append("g")
	.attr("transform","translate(" + margin.left + "," + margin.top + ")")
	.call(magZoom);
  
// Append x grid
plotMag.append("g")
	.attr("class","x grid")
	.attr("transform","translate(0," + height + ")")
	.call(xGrid);

// Append y grid
plotMag.append("g")
	.attr("class","y grid")
	.call(magYGrid);

// Append x axis
plotMag.append("g")
	.attr("class","x1 axis")
	.attr("transform","translate(0," + height + ")")
	.call(magXAxis1);

// Append additional X axis
plotMag.append("g")
	.attr("class","x2 axis")
	.attr("transform","translate(" + [0, 0] + ")")
	.call(magXAxis2);

// Append y axis
plotMag.append("g")
	.attr("class","y1 axis")
	.call(magYAxis1);

// Append additional y axis
plotMag.append("g")
	.attr("class","y2 axis")
	.attr("transform","translate(" + [width, 0] + ")")
	.call(magYAxis2);

// Add x axis label
/*
plotMag.append("text")
	.attr("transform","translate(" + (width / 2) + "," + (height + margin.bottom - 5) + ")")
	.style("font-size","15")
	.style("text-anchor","middle")
	.text("Frequency [Hz]");
*/

// Add y axis label
plotMag.append("text")
	.attr("transform", "rotate(-90)")
	.attr("y",0 - margin.left)
	.attr("x",0 - (height / 2))
	.attr("dy", "1em")
	.style("font-size","15")
	.style("text-anchor", "middle")
	.text("Magnitude [dB]");

// Clip path
plotMag.append("defs").append("clipPath")
	.attr("id", "clip")
	.append("rect")
	.attr("width", width)
	.attr("height", height);
  
plotMag.append("rect")
	.attr("width", width)
	.attr("height", height);
	
// Create plot
var plotPhs = d3.select("#plotphs").append("svg")
	.attr("width",width + margin.left + margin.right)
	.attr("height",height + margin.top + margin.bottom)
	.append("g")
	.attr("transform","translate(" + margin.left + "," + margin.top + ")")
	.call(phsZoom);
  
// Append x grid
plotPhs.append("g")
	.attr("class","x grid")
	.attr("transform","translate(0," + height + ")")
	.call(xGrid);

// Append y grid
plotPhs.append("g")
	.attr("class","y grid")
	.call(phsYGrid);

// Append x axis
plotPhs.append("g")
	.attr("class","x1 axis")
	.attr("transform","translate(0," + height + ")")
	.call(phsXAxis1);

// Append additional X axis
plotPhs.append("g")
	.attr("class","x2 axis")
	.attr("transform","translate(" + [0, 0] + ")")
	.call(phsXAxis2);

// Append y axis
plotPhs.append("g")
	.attr("class","y1 axis")
	.call(phsYAxis1);

// Append additional y axis
plotPhs.append("g")
	.attr("class","y2 axis")
	.attr("transform","translate(" + [width, 0] + ")")
	.call(phsYAxis2);

// Add x axis label  
plotPhs.append("text")
	.attr("transform","translate(" + (width / 2) + "," + (height + margin.bottom - 5) + ")")
	.style("font-size","15")
	.style("text-anchor","middle")
	.text("Frequency [Hz]");

// Add y axis label
plotPhs.append("text")
	.attr("transform", "rotate(-90)")
	.attr("y",0 - margin.left)
	.attr("x",0 - (height / 2))
	.attr("dy", "1em")
	.style("font-size","15")
	.style("text-anchor", "middle")
	.text("Phase [deg]");

// Clip path
plotPhs.append("defs").append("clipPath")
	.attr("id", "clip")
	.append("rect")
	.attr("width", width)
	.attr("height", height);
  
plotPhs.append("rect")
	.attr("width", width)
	.attr("height", height);

function redraw() {
	plotMag.select(".x1.axis").call(magXAxis1);
	plotMag.select(".y1.axis").call(magYAxis1);
	plotMag.select(".x2.axis").call(magXAxis2);
	plotMag.select(".y2.axis").call(magYAxis2);
	plotMag.select(".x.grid").call(xGrid);
	plotMag.select(".y.grid").call(magYGrid);

	plotPhs.select(".x1.axis").call(phsXAxis1);
	plotPhs.select(".y1.axis").call(phsYAxis1);
	plotPhs.select(".x2.axis").call(phsXAxis2);
	plotPhs.select(".y2.axis").call(phsYAxis2);
	plotPhs.select(".x.grid").call(xGrid);
	plotPhs.select(".y.grid").call(phsYGrid);
	
	var dataMag = [];
	var dataPhs = [];
	var data1 = [];
	var data2 = [];
	var data3 = [];

	for (var i = 0; i < range.length; i++) {
		data1.push({
			x: range[i],
			y: leadlag(range[i])
		});

		data2.push({
			x: range[i],
			y: mag2db(math.abs(leadlag(range[i])))
		});
		
		data3.push({
			x: range[i],
			y: rad2deg(angle(leadlag(range[i])))
		});
	}

	dataMag.push({data: data2, width: 1, color: 'blue', stroke: "0,0", legend: "Magnitude" });
	
	var seriesMag = plotMag.selectAll(".line").data(dataMag);
	
	seriesMag.enter().append("path");

	seriesMag.attr("class","line")
		.attr("d",function(d) { return magLine(d.data); })
		.attr("stroke-width", function(d) { return d.width; })
		.style("stroke", function(d) { return d.color; })
		.style("stroke-dasharray", function(d) { return d.stroke; });

	dataPhs.push({data: data3, width: 1, color: 'blue', stroke: "0,0", legend: "Phase" });
	
	var seriesPhs = plotPhs.selectAll(".line").data(dataPhs);
	
	seriesPhs.enter().append("path");

	seriesPhs.attr("class","line")
		.attr("d",function(d) { return phsLine(d.data); })
		.attr("stroke-width", function(d) { return d.width; })
		.style("stroke", function(d) { return d.color; })
		.style("stroke-dasharray", function(d) { return d.stroke; });
		
	plotPhs.selectAll('.x1.axis>.tick')  // find all the x axis ticks and loop
		.each(function(d,i){
			if (d3.select(this).select('text').text() === ""){ // if they have no label
				d3.selectAll('.x.grid>.tick:nth-child(' + (i + 1) + ')') // get the corresponding grid line
					.style("stroke-dasharray", "3,3"); // and make it dashed
			}
		});
}

$(function() {
	redraw();
});