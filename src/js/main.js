var map;
var year;
var projection;
var threshold;
var path;
var color;
var svg;
var features;
var world;
var indices;
var migration;
var tooltip, tooltipDot;
var MARGIN = {top: 20, right: 120, bottom: 130, left: 80};
var plotWidth, plotHeight;

/**
 * Execute once page has been fully loaded.
 */
$(function() {
  tooltip = d3.select("body")
          .append("div")
          .attr("class", "tooltip hidden");

  plotWidth = getPlotWidth();
  plotHeight = getPlotHeight();

  var width = d3.select("#map").node().getBoundingClientRect().width,
      height = d3.select("#map").node().getBoundingClientRect().height;

  svg = d3.select("#map")
      .append("svg")
      .style("cursor", "move");

  svg.attr("viewBox", "50 10 " + width + " " + height)
      .attr("preserveAspectRatio", "xMinYMin");

  var zoom = d3.zoom()
      .on("zoom", function () {
          var transform = d3.zoomTransform(this);
          map.attr("transform", transform);
      });

  svg.call(zoom);

  // year filter
  year = 2008;
  // migration volumn filter
  threshold = 0.00025;

  // geoMercator projection
  projection = d3.geoMercator() //d3.geoOrthographic()
      .scale(120)
      .translate([width / 2, height / 1.5]);

  // geoPath projection
  path = d3.geoPath().projection(projection);

  //colors for index metrics
  color = d3.scaleThreshold()
      .domain([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 110, 120])
      .range(["#3f51b5", "#2196f3", "#03a9f4", "#00bcd4", "#009688", "#4caf50", "#8bc34a", "#cddc39", "#ffeb3b", "#ffc107", "#ff9800", "#ff5722"]);

  // loading json stuffs
  d3.queue()
    .defer(d3.json, "src/data/50m.json")
    .defer(d3.json, "src/data/country_features.json")
    .defer(d3.json,"src/data/migrate.json")
    .await(function (error, world_data, country_features, migration_data) {
        if (error) {
            console.error('Oh dear, something went wrong: ' + error);
        }
        else {
          world = world_data;
          indices = country_features;
          migration = migration_data;
          createFeatures();
          draw();
        }
    });

    d3.select("#year-selector")
    .property('value', year)
    .on("input", function() {
      d3.select("#selected-year").html(this.value);
      year = this.value;
      update();
    });
    d3.select("#selected-year").html(year);

    d3.select("#threshold-selector")
    .property('value', threshold)
    .on("input", function() {
      d3.select("#selected-threshold").html(this.value);
      threshold = this.value;
      update();
    });
    d3.select("#selected-threshold").html(threshold);
});

function draw() {
  updateFeatures();
  drawMap();
  drawPlots();
}

function update() {
  map.remove();
  // d3.selectAll("g > *").remove();
  tooltip.classed("hidden", true);
  draw();
}

function createFeatures() {
  features = topojson.feature(world, world.objects.countries).features;
  indicesByYear = {2006: {}, 2007: {}, 2008: {}, 2009: {}, 2010: {}, 2011: {}, 2012: {}, 2013: {}, 2014: {}, 2015: {}, 2016: {}, 2017: {}};

  indices.forEach(function (d) {
    indicesByYear[d.year][d.iso] = {
        hdi_value: d['hdi_value'],
        hdi_rank: d['hdi_rank'],
        fgi_value: d['fgi_value'],
        fgi_rank: d['fgi_rank'],
        hfi_value: d['hfi_value'],
        hfi_rank: d['hfi_rank'],
        population: d['population'],
        clustering_coeff: d['clustering_coeff'],
        sorted_tri: d['sorted_tri'],
        indegree_centrality: d['indegree_centrality'],
        outdegree_centrality: d['outdegree_centrality'],
        closeness_centrality: d['closeness_centrality'],
        out_closeness_centrality: d['out_closeness_centrality'],
        betweenness_centrality: d['betweenness_centrality'],
        eigenvector_centrality: d['eigenvector_centrality'],
        eigenvector_centrality_out: d['eigenvector_centrality_out'],
        index: d['index'],
        nxc: d['nxc'],
        outflow: d['outflow'],
        inflow: d['inflow'],
        share: d['share'],
        asylum_outflow: d['asylum_outflow'],
        asylum_inflow: d['asylum_inflow']
    }
  });
}

function updateFeatures() {
  features.forEach(function (d) {
      d.details = indicesByYear[year][d.id] ? indicesByYear[year][d.id] : {};
  });
}

function drawMap() {
    migration_features = migrate(features, migration, year);

    map = svg.append("g");
    // draw map
    map.append("g")
        .selectAll("path")
        .data(features)
        .enter().append("path")
        .attr("name", function (d) {
            return d.properties.name;
        })
        .attr("id", function (d) {
            return d.id;
        })
        .attr("d", path)
        .style("fill", function (d) {
            return d.details && d.details['fgi_value'] ? color(d.details['fgi_value']) : undefined;
        })
        .on('mouseover', function (d) {
            d3.select(this)
                .style("stroke", "white")
                .style("stroke-width", 1)
                .style("cursor", "pointer");

            label = d.properties.name;
            if (d.details['hdi_value'] && d.details['hdi_rank']) {
              label += "<br>" + "HDI: " + d.details['hdi_value'] + " (" + d.details['hdi_rank'] + ")"
            }
            if (d.details['fgi_value'] && d.details['fgi_rank']) {
              label += "<br>" + "FGI: " + d.details['fgi_value'] + " (" + d.details['fgi_rank'] + ")"
            }
            showTooltip(d, label);
        })
        .on('mouseout', function (d) {
            d3.select(this)
                .style("stroke", null)
                .style("stroke-width", 0.25);
            tooltip.classed("hidden", true);
        });

    // draw middle of country
    // map.append("g")
    //     .selectAll("circle.central")
    //     .data(features)
    //     .enter()
    //     .append("circle")
    //     .attr("name", function(d) { return d.properties.name;})
    //     .attr("id", function(d) { return 'middle_' + d.id;})
    //     .attr("r", 2)
    //     .attr("cx", function(d) { return d.pos.x; })
    //     .attr("cy", function(d) { return d.pos.y; })
    //     .style("fill", "white")
    //     .style("opacity", 0.6)
    //     .style("stroke", "#252525")
    //     .on('click', selected)
    //     .on("mousemove", showTooltip)
    //     .on("mouseout",  function(d,i) {
    //         tooltip.classed("hidden", true);
    //     });

    // draw edge
    drawarcs(map, migration_features);
}

function drawarcs(svg, migration) {
    var arcs = svg.selectAll('path.datamaps-arc').data(migration);
    min_migration = threshold;
    max_migration = 0;
    migration.forEach(function(d){
        if (d.share > max_migration){
            max_migration = d.share;
        };
    });
    var pop_scale = d3.scaleLinear().domain([min_migration, max_migration]).range([1,100])
	arcs
		.enter()
		.append('path')
		.attr('class','arc')
		.attr('d', function(d) {
			var origin = [d.source.x, d.source.y];
			var dest = [d.target.x, d.target.y];
            var mid = [ (origin[0] + dest[0]) / 2, (origin[1] + dest[1]) / 2];
            var size = pop_scale(d.share);

			//define handle points for Bezier curves. Higher values for curveoffset will generate more pronounced curves.
			var curveoffset = 20,
				midcurve = [mid[0]+curveoffset, mid[1]-curveoffset]

			// the scalar variable is used to scale the curve's derivative into a unit vector
			scalar = Math.sqrt(Math.pow(dest[0],2) - 2*dest[0]*midcurve[0]+Math.pow(midcurve[0],2)+Math.pow(dest[1],2)-2*dest[1]*midcurve[1]+Math.pow(midcurve[1],2));

			// define the arrowpoint: the destination, minus a scaled tangent vector, minus an orthogonal vector scaled to the d.value variable
			arrowpoint = [
				dest[0] - ( 0.5*size*(dest[0]-midcurve[0]) - size*(dest[1]-midcurve[1]) ) / scalar ,
				dest[1] - ( 0.5*size*(dest[1]-midcurve[1]) - size*(-dest[0]+midcurve[0]) ) / scalar
			];

			// move cursor to origin
			return "M" + origin[0] + ',' + origin[1]
			// smooth curve to offset midpoint
				+ "S" + midcurve[0] + "," + midcurve[1]
			//smooth curve to destination
				+ "," + dest[0] + "," + dest[1]
			//straight line to arrowhead point
				+ "L" + arrowpoint[0] + "," + arrowpoint[1]
			// straight line towards original curve along scaled orthogonal vector (creates notched arrow head)
				+ "l" + (0.3*size*(-dest[1]+midcurve[1])/scalar) + "," + (0.3*size*(dest[0]-midcurve[0])/scalar)
				// smooth curve to midpoint
				+ "S" + (midcurve[0]) + "," + (midcurve[1])
				//smooth curve to origin
				+ "," + origin[0] + "," + origin[1]
		});

	arcs.exit()
		.transition()
		.style('opacity', 0)
		.remove();

};

// init all drawing map, circle and line
function migrate(world_data, migration_data, select_year){
    var country_data = [];
    world_data.forEach(function(d){
        all_coordinates = longest_coordinates(d.geometry.coordinates);
        middle_pos = middle_coordinates(all_coordinates);
        d['pos'] = {
          x:middle_pos.xy[0],
          y:middle_pos.xy[1],
          long:middle_pos.longlat[0],
          lat:middle_pos.longlat[1]
        };
        country_data.push(
        {
            id: d.id,
            name: d.properties.name,
            long: d.pos.long,
            lat: d.pos.lat,
            x: d.pos.x,
            y: d.pos.y
        }
        );
    });
    var country_map = d3.map(country_data, function(d){ return d.id});
    var movements = []
    migration_data.forEach(function(d){
        d = JSON.parse(d);
        if (d.year != parseInt(select_year) || d.share < parseFloat(threshold)){
          return
        };

        d.source = country_map.get(d['iso-origin']);
        d.target = country_map.get(d['iso-destination']);

        if (d.source == null || d.target == null){
          return
        };

        delete d['iso-origin'];
        delete d['iso-destination'];
        delete d.year;

        movements.push(d);

      });
    return movements;

};

// central coordinate of each map
function middle_coordinates(list_coordinates){
    var sum_x = 0;
    var count_x = 0;
    var sum_y = 0;
    var count_y =0;
    var loop = 0;
    list_coordinates.forEach(function(coordinate){
      loop = loop + 1;
      sum_x = sum_x + parseFloat(coordinate[0]);
      count_x = count_x + 1;
      sum_y = sum_y + parseFloat(coordinate[1]);
      count_y = count_y + 1;
    })

    return {
      longlat: [sum_x/count_x, sum_y/count_y],
      xy: projection([sum_x/count_x, sum_y/count_y])
    }
  };

// area of map which is biggest
function longest_coordinates(coordinates){
longest = []
coordinates.forEach(function(coordinate){
    if (coordinate.length == 0){
    return
    };
    if (coordinate.length == 1){
    compare_coordinate = coordinate[0];
    }else{
    compare_coordinate = coordinate;
    };
    if (longest.length < compare_coordinate.length){
    longest = compare_coordinate;
    };
});
return longest
};

// tooltip stuff
function showTooltip(d, label, offset_xy = [10,-35]) {
  var mouse = [d3.event.pageX, d3.event.pageY]
  tooltip.classed("hidden", false)
          .attr("style", "left:"+(mouse[0]+offset_xy[0])+"px;top:"+(mouse[1]+offset_xy[1])+"px")
          .html(label);
};

function selected() {
  d3.select('.selected').classed('selected', false);
  d3.select(this).classed('selected', true);
};

function getPlotWidth(selector) {
    return d3.select(".carousel-inner").node().getBoundingClientRect().width - MARGIN.left - MARGIN.right;
}

function getPlotHeight(selector) {
    return d3.select(".carousel-inner").node().getBoundingClientRect().height / 1.5 - MARGIN.top - MARGIN.bottom;
}

function drawScatterPlot(id, x, y, xLabel, yLabel) {
  var plot = d3.select(id)
      .append("g")
      .attr("transform", "translate(" + MARGIN.left + "," + MARGIN.top + ")");

  var xValue = function(d) { return d.details[x];};
  var yValue = function(d) {
    if (Array.isArray(y)) {
      var sum = 0;
      for (var i = 0; i < y.length; i++) {
        sum += d.details[y[i]];
      }
      return sum;
    }
    return d.details[y];
  };
  var xMap = function(d) { return xScale(xValue(d));};
  var yMap = function(d) { return yScale(yValue(d));};
  var xMin = d3.min(features, xValue),
      xMax = d3.max(features, xValue),
      xRange = xMax - xMin;
  var yMin = d3.min(features, yValue),
      yMax = d3.max(features, yValue),
      yRange = yMax - yMin;
  var xScale = d3.scaleLinear()
      .domain([xMin - xRange/10, xMax + xRange/8])
      .range([0, plotWidth]);
  var yScale = d3.scaleLinear()
      .domain([yMin - yRange/10, yMax + yRange/8])
      .range([plotHeight, 0]);
  var xAxis = d3.axisBottom(xScale)
      .ticks(5);
  var yAxis = d3.axisLeft(yScale)
      .ticks(5);

  // x-axis
  plot.append("g")
      .attr("class", "x axis-line")
      .attr("transform", "translate(0," + plotHeight + ")")
      .call(xAxis)
    .append("text")
      .attr("class", "x axis-label")
      .attr("x", plotWidth)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text(xLabel);

  // y-axis
  plot.append("g")
      .attr("class", "y axis-line")
      .call(yAxis)
    .append("text")
      .attr("class", "y axis-label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text(yLabel);

  plot.selectAll(".scatter-dot")
      .data(features)
    .enter().append("circle")
    .filter(function(d) { return xValue(d) && yValue(d) })
      .attr("class", "scatter-dot")
      .attr("r", 3.5)
      .attr("cx", xMap)
      .attr("cy", yMap)
      .style("fill", "#fff")
      .on("mouseover", function(d) {
        d3.select(this)
            .style("stroke", "#c0392b")
            .style("cursor", "pointer");

        var label = d.properties.name + "<br/> (x: " + xValue(d) + ", y: " + yValue(d) + ")";
        showTooltip(d, label);
      })
      .on("mouseout", function(d) {
        d3.select(this)
            .style("stroke", "#e67e22");
        tooltip.classed("hidden", true);
      });
}

function drawPlots() {
  $('[id*=hdi], [id*=fgi]').empty();
  var hdi_label = "Human Development Index (HDI)";
  var fgi_label = "Fragile States Index (FSI)";

  drawScatterPlot("#hdi-refugees-out", "hdi_value", "outflow", hdi_label, "Number of Refugees");
  drawScatterPlot("#hdi-refugees-in", "hdi_value", "inflow", hdi_label, "Number of Refugees");
  drawScatterPlot("#hdi-asylum-out", "hdi_value", "asylum_outflow", hdi_label, "Number of Asylum-Seekers");
  drawScatterPlot("#hdi-asylum-in", "hdi_value", "asylum_inflow", hdi_label, "Number of Asylum-Seekers");
  drawScatterPlot("#hdi-asylum-refugees-out", "hdi_value", ["asylum_outflow", "outflow"], hdi_label, "Number of Asylum-Seekers + Refugees");
  drawScatterPlot("#hdi-asylum-refugees-in", "hdi_value", ["asylum_inflow", "inflow"], hdi_label, "Number of Asylum-Seekers + Refugees");

  drawScatterPlot("#hdi-outdegree-centrality", "hdi_value", "outdegree_centrality", hdi_label, "Outdegree Centrality");
  drawScatterPlot("#hdi-indegree-centrality", "hdi_value", "indegree_centrality", hdi_label, "Indegree Centrality");
  drawScatterPlot("#fgi-outdegree-centrality", "fgi_value", "outdegree_centrality", fgi_label, "Outdegree Centrality");
  drawScatterPlot("#fgi-indegree-centrality", "fgi_value", "indegree_centrality", fgi_label, "Indegree Centrality");
}
