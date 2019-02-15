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

// year filter
var year = 2008;
// migration volumn filter
var threshold = 10000;

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

var tooltip = d3.select("#map")
        .append("div")
        .attr("class", "tooltip hidden");

// loading json stuffs
d3.queue()
    .defer(d3.json, "src/data/50m.json")
    .defer(d3.json, "src/data/population.json")
    .defer(d3.json,"src/data/migrate.json")
    .await(function (error, world, data, migration) {
        if (error) {
            console.error('Oh dear, something went wrong: ' + error);
        }
        else {
            drawMap(world, data, migration);
        }
    });

function drawMap(world, data, migration) {
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
    migration_features = migrate(features, migration, year);

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
            return d.details && d.details.total ? color(d.details.total) : undefined;
        })
        .on('mouseover', function (d) {
            d3.select(this)
                .style("stroke", "white")
                .style("stroke-width", 1)
                .style("cursor", "pointer");
            showTooltip(d);
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
        if (d.value > max_migration){
            max_migration = d.value;
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
            var size = pop_scale(d.value);

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
    var migration = []
    migration_data.forEach(function(d){
        d = JSON.parse(d);
        if (d.year != parseInt(select_year) || d.value < parseInt(threshold)){
          return
        };

        d.source = country_map.get(d.FROM);
        d.target = country_map.get(d.TO);

        if (d.source == null || d.target == null){
          return
        };

        delete d.FROM;
        delete d.TO;
        delete d.year;
        
        migration.push(d);
        
      });
    return migration;

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
function showTooltip(d, event) {
    label = d.properties.name;
    var mouse = d3.mouse(svg.node())
                .map( function(d) { return parseInt(d); } );
    tooltip.classed("hidden", false)
            .attr("style", "left:"+(mouse[0]/1.5)+"px;top:"+(mouse[1]/1.5)+"px")
            .html(label);
};

function selected() {
    d3.select('.selected').classed('selected', false);
    d3.select(this).classed('selected', true);
  };
