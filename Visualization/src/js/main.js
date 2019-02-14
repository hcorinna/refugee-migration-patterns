var width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0),
    height = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);

var svg = d3.select("#map")
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

var map = svg.append("g");
    //.attr("class", "map");

d3.queue()
    .defer(d3.json, "src/data/50m.json")
    .defer(d3.json, "src/data/population.json")
    .await(function (error, world, data) {
        if (error) {
            console.error('Oh dear, something went wrong: ' + error);
        }
        else {
            drawMap(world, data);
            drawarcs(map);
        }
    });

function drawMap(world, data) {
    // geoMercator projection
    var projection = d3.geoMercator() //d3.geoOrthographic()
        .scale(130)
        .translate([width / 2, height / 1.5]);

    // geoPath projection
    var path = d3.geoPath().projection(projection);

    //colors for population metrics
    var color = d3.scaleThreshold()
        .domain([10000, 100000, 500000, 1000000, 5000000, 10000000, 50000000, 100000000, 500000000, 1500000000])
        .range(["#a29bfe", "#e0ecf4", "#bfd3e6", "#9ebcda", "#8c96c6", "#8c6bb1", "#88419d", "#810f7c", "#4d004b"]);

    var features = topojson.feature(world, world.objects.countries).features;
    var populationById = {};

    data.forEach(function (d) {
        populationById[d.country] = {
            total: +d.total,
            females: +d.females,
            males: +d.males
        }
    });
    features.forEach(function (d) {
        d.details = populationById[d.properties.name] ? populationById[d.properties.name] : {};
    });

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
            return d.details && d.details.total ? color(d.details.total) : undefined;
        })
        .on('mouseover', function (d) {
            d3.select(this)
                .style("stroke", "white")
                .style("stroke-width", 1)
                .style("cursor", "pointer");
        })
        .on('mouseout', function (d) {
            d3.select(this)
                .style("stroke", null)
                .style("stroke-width", 0.25);
        });
}

var tradedata = [
  {
 			destination: {latitude: -23.3, longitude: 132.2},
 			name: 'Australia',
 			trade: 5
 	},{
      destination: { latitude: -28.5, longitude: 24.7 },
      name: 'South Africa',
      trade : 6
  },{
      destination: { latitude: 31.7, longitude: 106.2 },
      name: 'China',
      trade : 16
  },{
      destination: { latitude: 36.1, longitude: 127.7 },
      name: 'S. Korea',
      trade: 8
  },{
      destination: { latitude: 53.6, longitude: -2.3},
      name: 'Great Britain',
      trade: 12
  },{
      destination: { latitude: 61.2, longitude: 9.7144087 },
      name: 'Norway',
      trade: 2
  },{
      destination: { latitude: 61.6, longitude: 15.4 },
      name: 'Sweden',
      trade: 5
  },{
      destination: { latitude: 64.93, longitude: -19.02},
      name: 'Iceland',
      trade: 15
  },{
      destination: { latitude: 20.9, longitude: -101.5 },
      name: 'Mexico',
      trade: 15
  },{
      destination: { latitude: -14.0, longitude: -47.643501 },
      name: 'Brazil',
      trade: 12
 },{
      destination: {  latitude: 55.86, longitude: -112.1 },
      name: 'Canada',
      trade: 32
  }
];

function drawarcs(svg) {
    var projection = d3.geoMercator() //d3.geoOrthographic()
        .scale(130)
        .translate([width / 2, height / 1.5]);

        var path = d3.geoPath().projection(projection);
	var arcs = svg.selectAll('path.datamaps-arc').data( tradedata, JSON.stringify );
        console.log(arcs);
	arcs
		.enter()
		.append('path')
		.attr('class','arc')
		.attr('d', function(datum) {
			var origin = projection([-69.445469,45.253783]);
			var dest = projection([datum.destination.longitude, datum.destination.latitude]);
			var mid = [ (origin[0] + dest[0]) / 2, (origin[1] + dest[1]) / 2];

			//define handle points for Bezier curves. Higher values for curveoffset will generate more pronounced curves.
			var curveoffset = 20,
				midcurve = [mid[0]+curveoffset, mid[1]-curveoffset]

			// the scalar variable is used to scale the curve's derivative into a unit vector
			scalar = Math.sqrt(Math.pow(dest[0],2) - 2*dest[0]*midcurve[0]+Math.pow(midcurve[0],2)+Math.pow(dest[1],2)-2*dest[1]*midcurve[1]+Math.pow(midcurve[1],2));

			// define the arrowpoint: the destination, minus a scaled tangent vector, minus an orthogonal vector scaled to the datum.trade variable
			arrowpoint = [
				dest[0] - ( 0.5*datum.trade*(dest[0]-midcurve[0]) - datum.trade*(dest[1]-midcurve[1]) ) / scalar ,
				dest[1] - ( 0.5*datum.trade*(dest[1]-midcurve[1]) - datum.trade*(-dest[0]+midcurve[0]) ) / scalar
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
				+ "l" + (0.3*datum.trade*(-dest[1]+midcurve[1])/scalar) + "," + (0.3*datum.trade*(dest[0]-midcurve[0])/scalar)
				// smooth curve to midpoint
				+ "S" + (midcurve[0]) + "," + (midcurve[1])
				//smooth curve to origin
				+ "," + origin[0] + "," + origin[1]
		});

	arcs.exit()
		.transition()
		.style('opacity', 0)
		.remove();

}
