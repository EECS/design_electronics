//This module needs the following three variables defined to function properly: UPDATE
//  range - List of values to be used to create the x-axis of the graph.
//  db_mag_data - This is a list of values that is the same size as the range variable that defines the 
//                the magnitude data of the transfer function in decibels to be plotted.
//  phase_data - This is a list of values that is the same size as the range variable that defines the 
//                the phase data of the transfer function in degrees to be plotted.

function BodePlot(mags, mags_min, mags_max, phases, phases_min, phases_max, mag_plot_div, phase_plot_div)
{
    this.mags= mags;
    this.mags_min = mags_min;
    this.mags_max = mags_max;
    this.phases = phases;
    this.phases_min = phases_min;
    this.phases_max = phases_max;
    this.mag_plot_div = mag_plot_div;
    this.phase_plot_div = phase_plot_div;
    this.margin = {
        top: 20,
        right: 20,
        bottom: 35,
        left: 50
    };

    this.width = 500 - this.margin.left - this.margin.right;
    this.height = 250 - this.margin.top - this.margin.bottom;

    this.x = d3.scale.log()
                .domain([1, range[range.length-1].toFixed()])
                .range([0, this.width]);

    this.xGrid = d3.svg.axis()
                    .scale(this.x)
                    .orient("bottom")
                    .ticks(5)
                    .tickSize(-this.height, -this.height, 0)
                    .tickFormat("");

    // Variable that sets the magnitude data range y axis data range.
    // Dynamically re-sizes based upon transfer function maximum and minimum.
    if(this.mags.length > 0){
        if(this.mags_min == this.mags_max){
            this.magY = d3.scale.linear()
                .domain([this.mags_min-10, this.mags_max+10])
                .range([this.height, 0]);
        }else{
            this.magY = d3.scale.linear()
                .domain([this.mags_min, this.mags_max])
                .range([this.height, 0]);
        }
    }else{
        this.magY = d3.scale.linear()
            .domain([-20, 20])
            .range([this.height, 0]);
    }

    this.magXAxis1 = d3.svg.axis()
                        .scale(this.x)
                        .orient("bottom")
                        .ticks(1,"0.1s")
                        .innerTickSize(-6)
                        .outerTickSize(0)
                        .tickPadding(7);

    this.magYAxis1 = d3.svg.axis()
                        .scale(this.magY)
                        .orient("left")
                        .ticks(5)
                        .innerTickSize(-6)
                        .outerTickSize(0)
                        .tickPadding(7);

    this.magXAxis2 = d3.svg.axis()
                        .scale(this.x)
                        .orient("top")
                        .ticks(5)
                        .innerTickSize(-6)
                        .tickPadding(-20)
                        .outerTickSize(0)
                        .tickFormat("");

    this.magYAxis2 = d3.svg.axis()
                        .scale(this.magY)
                        .orient("left")
                        .ticks(5)
                        .innerTickSize(6)
                        .tickPadding(-20)
                        .outerTickSize(0)
                        .tickFormat("");

    this.magYGrid = d3.svg.axis()
                        .scale(this.magY)
                        .orient("left")
                        .ticks(5)
                        .tickSize(-this.width, -this.width, 0)
                        .tickFormat("");

    this.magLine = d3.svg.line()
                        .x(function(d) { return this.x(d.x); })
                        .y(function(d) { return this.magY(d.y); })
                        .interpolate("linear");

    // Variable that sets the phase data y axis data range.
    // Dynamically re-sizes based upon transfer function maximum and minimum.
    if(this.phases.length > 0){
        if(this.phases_min == this.phases_max){
            this.phsY = d3.scale.linear()
                .domain([-45, 45])
                .range([this.height, 0]);

        }else{
            this.phsY = d3.scale.linear()
                .domain([this.phases_min, this.phases_max])
                .range([this.height, 0]);

        }
    }else{
        this.phsY = d3.scale.linear()
            .domain([-45, 45])
            .range([this.height, 0]);

    }
    this.phsXAxis1 = d3.svg.axis()
        .scale(this.x)
        .orient("bottom")
        .ticks(1,"0.1s")
        .innerTickSize(-6)
        .outerTickSize(0)
        .tickPadding(7);

    this.phsYAxis1 = d3.svg.axis()
        .scale(this.phsY)
        .orient("left")
        .ticks(5)
        .innerTickSize(-6)
        .outerTickSize(0)
        .tickPadding(7);

    this.phsXAxis2 = d3.svg.axis()
        .scale(this.x)
        .orient("top")
        .ticks(5)
        .innerTickSize(-6)
        .tickPadding(-20)
        .outerTickSize(0)
        .tickFormat("");

    this.phsYAxis2 = d3.svg.axis()
        .scale(this.phsY)
        .orient("left")
        .ticks(5)
        .innerTickSize(6)
        .tickPadding(-20)
        .outerTickSize(0)
        .tickFormat("");

    this.phsYGrid = d3.svg.axis()
        .scale(this.phsY)
        .orient("left")
        .ticks(5)
        .tickSize(-this.width, -this.width, 0)
        .tickFormat("");

    this.phsLine = d3.svg.line()
        .x(function(d) { return this.x(d.x); })
        .y(function(d) { return this.phsY(d.y); })
        .interpolate("linear");

    this.magZoom = d3.behavior.zoom()
        .x(this.x)
        .y(this.magY)
        .scaleExtent([1, 1])
        .on("zoom",this.redraw);

    this.phsZoom = d3.behavior.zoom()
        .x(this.x)
        .y(this.phsY)
        .scaleExtent([1, 1])
        .on("zoom",this.redraw);

    // Create plot
    this.plotMag = d3.select("#"+this.mag_plot_div).append("svg")
        .attr("width",this.width + this.margin.left + this.margin.right)
        .attr("height",this.height + this.margin.top + this.margin.bottom)
        .append("g")
        .attr("transform","translate(" + this.margin.left + "," + this.margin.top + ")")
        .call(this.magZoom);

    // Create plot
    this.plotPhs = d3.select("#"+this.phase_plot_div).append("svg")
        .attr("width",this.width + this.margin.left + this.margin.right)
        .attr("height",this.height + this.margin.top + this.margin.bottom)
        .append("g")
        .attr("transform","translate(" + this.margin.left + "," + this.margin.top + ")")
        .call(this.phsZoom);
}

BodePlot.prototype = {
    constructor: BodePlot,
    createGraphs: function()
    {
        // Append x grid
        this.plotMag.append("g")
            .attr("class","x grid")
            .attr("transform","translate(0," + this.height + ")")
            .call(this.xGrid);

        // Append y grid
        this.plotMag.append("g")
            .attr("class","y grid")
            .call(this.magYGrid);

        // Append x axis
        this.plotMag.append("g")
            .attr("class","x1 axis")
            .attr("transform","translate(0," + this.height + ")")
            .call(this.magXAxis1);

        // Append additional X axis
        this.plotMag.append("g")
            .attr("class","x2 axis")
            .attr("transform","translate(" + [0, 0] + ")")
            .call(this.magXAxis2);

        // Append y axis
        this.plotMag.append("g")
            .attr("class","y1 axis")
            .call(this.magYAxis1);

        // Append additional y axis
        this.plotMag.append("g")
            .attr("class","y2 axis")
            .attr("transform","translate(" + [this.width, 0] + ")")
            .call(this.magYAxis2);

        // Add x axis label
        this.plotMag.append("text")
            .attr("transform","translate(" + (this.width / 2) + "," + (this.height + this.margin.bottom - 5) + ")")
            .style("font-size","15")
            .style("text-anchor","middle")
            .text("Frequency [Hz]");

        // Add y axis label
        this.plotMag.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y",0 - this.margin.left)
            .attr("x",0 - (this.height / 2))
            .attr("dy", "1em")
            .style("font-size","15")
            .style("text-anchor", "middle")
            .text("Magnitude [dB]");

        // Clip path
        this.plotMag.append("defs").append("clipPath")
            .attr("id", "clip")
            .append("rect")
            .attr("width", this.width)
            .attr("height", this.height);

        this.plotMag.append("rect")
            .attr("width", this.width)
            .attr("height", this.height);

        // Append x grid
        this.plotPhs.append("g")
            .attr("class","x grid")
            .attr("transform","translate(0," + this.height + ")")
            .call(this.xGrid);

        // Append y grid
        this.plotPhs.append("g")
            .attr("class","y grid")
            .call(this.phsYGrid);

        // Append x axis
        this.plotPhs.append("g")
            .attr("class","x1 axis")
            .attr("transform","translate(0," + this.height + ")")
            .call(this.phsXAxis1);

        // Append additional X axis
        this.plotPhs.append("g")
            .attr("class","x2 axis")
            .attr("transform","translate(" + [0, 0] + ")")
            .call(this.phsXAxis2);

        // Append y axis
        this.plotPhs.append("g")
            .attr("class","y1 axis")
            .call(this.phsYAxis1);

        // Append additional y axis
        this.plotPhs.append("g")
            .attr("class","y2 axis")
            .attr("transform","translate(" + [this.width, 0] + ")")
            .call(this.phsYAxis2);

        // Add x axis label  
        this.plotPhs.append("text")
            .attr("transform","translate(" + (this.width / 2) + "," + (this.height + this.margin.bottom - 5) + ")")
            .style("font-size","15")
            .style("text-anchor","middle")
            .text("Frequency [Hz]");

        // Add y axis label
        this.plotPhs.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y",0 - this.margin.left)
            .attr("x",0 - (this.height / 2))
            .attr("dy", "1em")
            .style("font-size","15")
            .style("text-anchor", "middle")
            .text("Phase [deg]");

        // Clip path
        this.plotPhs.append("defs").append("clipPath")
            .attr("id", "clip")
            .append("rect")
            .attr("width", this.width)
            .attr("height", this.height);

        this.plotPhs.append("rect")
            .attr("width", this.width)
            .attr("height", this.height);
    },
    
    redraw: function()
    {
        // Get container div of graph to be re-drawn on initial page load.
        var div = this.mag_plot_div;
        var bode;

        //Div is not undefined on initial page load.
        if (div != undefined){
            //Select object associated with graph to update.
            graphs.forEach(function(element){
                if(element.mag_plot_div == div){
                    bode = element;
                }
            });
        //Div will be undefined on subsequent page loads, now need to
        //retrieve div from graph element.
        }else{
            div = this.parentElement.parentElement.id;
            //Select object associated with graph to update.
            graphs.forEach(function(element){
                if(element.mag_plot_div == div || element.phase_plot_div == div){
                    bode = element;
                }
            });
        }

        if(bode != undefined)
        {
            bode.plotMag.select(".x1.axis").call(bode.magXAxis1);
            bode.plotMag.select(".y1.axis").call(bode.magYAxis1);
            bode.plotMag.select(".x2.axis").call(bode.magXAxis2);
            bode.plotMag.select(".y2.axis").call(bode.magYAxis2);
            bode.plotMag.select(".x.grid").call(bode.xGrid);
            bode.plotMag.select(".y.grid").call(bode.magYGrid);

            bode.plotPhs.select(".x1.axis").call(bode.phsXAxis1);
            bode.plotPhs.select(".y1.axis").call(bode.phsYAxis1);
            bode.plotPhs.select(".x2.axis").call(bode.phsXAxis2);
            bode.plotPhs.select(".y2.axis").call(bode.phsYAxis2);
            bode.plotPhs.select(".x.grid").call(bode.xGrid);
            bode.plotPhs.select(".y.grid").call(bode.phsYGrid);
        
            var dataMag = [];
            var dataPhs = [];
            var magDataPoints = [];
            var phaseDataPoints = [];
        
            //Push magnitude and phase data into graph.
            for(var i = 0; i < range.length; i++)
            {
                phaseDataPoints.push({
                    x: range[i],
                    y: bode.phases[i]
                });
            
                magDataPoints.push({
                    x: range[i],
                    y: bode.mags[i]
                });
            }
        
            dataMag.push({data: magDataPoints, width: 1, color: 'blue', stroke: "0,0", legend: "Magnitude" });
        
            seriesMag = bode.plotMag.selectAll(".line").data(dataMag);
        
            seriesMag.enter().append("path");
        
            seriesMag.attr("class","line")
                .attr("d",function(d) { return bode.magLine(d.data); })
                .attr("stroke-width", function(d) { return d.width; })
                .style("stroke", function(d) { return d.color; })
                .style("stroke-dasharray", function(d) { return d.stroke; });
        
            dataPhs.push({data: phaseDataPoints, width: 1, color: 'blue', stroke: "0,0", legend: "Phase" });
        
            seriesPhs = bode.plotPhs.selectAll(".line").data(dataPhs);
        
            seriesPhs.enter().append("path");
        
            seriesPhs.attr("class","line")
                .attr("d",function(d) { return bode.phsLine(d.data); })
                .attr("stroke-width", function(d) { return d.width; })
                .style("stroke", function(d) { return d.color; })
                .style("stroke-dasharray", function(d) { return d.stroke; });
        }
    }
}

var output_impedance_bode = new BodePlot(mags_output_impedance, mags_min_output_impedance, mags_max_output_impedance, 
    phases_output_impedance, phase_min_output_impedance, phase_max_output_impedance, out_imped_mag_div, out_imped_phs_div);

var input_impedance_bode = new BodePlot(mags_input_impedance, mags_min_input_impedance, mags_max_input_impedance, 
        phases_input_impedance, phase_min_input_impedance, phase_max_input_impedance, in_imped_mag_div, in_imped_phs_div);

var input_output_bode = new BodePlot(mags_input_output_transfer, mags_min_input_output_transfer, mags_max_input_output_transfer, 
        phases_input_output_transfer, phase_min_input_output_transfer, phase_max_input_output_transfer, in_out_mag_div, in_out_phs_div);

var duty_output_bode = new BodePlot(mags_duty_output_transfer, mags_min_duty_output_transfer, mags_max_duty_output_transfer, 
        phases_duty_output_transfer, phase_min_duty_output_transfer, phase_max_duty_output_transfer, duty_out_mag_div, duty_out_phs_div);

output_impedance_bode.createGraphs();
input_impedance_bode.createGraphs();
input_output_bode.createGraphs();
duty_output_bode.createGraphs();

graphs = Array(output_impedance_bode, input_impedance_bode, input_output_bode, duty_output_bode);