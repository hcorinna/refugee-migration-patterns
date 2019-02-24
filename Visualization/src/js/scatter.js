var year = 2008

d3.queue()
    .defer(d3.json, "src/data/scatter.json")
    .await(function(error, data) {
        if (error) {
            console.error('Oh dear, something went wrong: ' + error);
        } else {
            var graph_data = [
                {
                    svg_css: '#scatter_first',
                    x_field: 'eigenvector_centrality',
                    y_field: 'closeness_centrality'
                },
                {
                    svg_css: '#scatter_second',
                    x_field: 'eigenvector_centrality_out',
                    y_field: 'out_closeness_centrality'
                }
            ];
            graph_data.forEach(function(graph){
                drawscatter(
                    data[year], 
                    graph.svg_css, 
                    graph.x_field, 
                    graph.y_field
                    );
            });
            
        };
    });

var drawscatter = function(data, svg_css, x_field, y_field){

    var scatter_tooltip = d3.select("div.scatter_tooltip");
    
    var dim_width = window.innerWidth/2.8,
    dim_height = window.innerHeight/2.8,
    margin = {top: dim_height/10, right: dim_width/10, bottom: dim_height/5, left: dim_width/5};
    width = dim_width - margin.left - margin.right,
    height = dim_height - margin.top - margin.bottom;

    var x = d3.scaleLinear()
    .range([0, width]);

    var y = d3.scaleLinear()
        .range([height, 0]);

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    var xAxis = d3.axisBottom(x);

    var yAxis = d3.axisLeft(y);

    x.domain(d3.extent(data, function(d) { return d[x_field]; })).nice();
    y.domain(d3.extent(data, function(d) { return d[y_field]; })).nice();

    var svg = d3.select(svg_css)
            .append("svg")
            .style("background-color", "whitesmoke")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
        .attr("class", "x scatter_axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("text")             
        .attr("transform", "translate(" + (width/2) + " ," + (height + margin.bottom * .9) + ")")
        .style("text-anchor", "middle")
        .text(x_field);

    svg.append("g")
        .attr("class", "y scatter_axis")
        .call(yAxis);

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text(y_field);

    svg.selectAll(".dot")
        .data(data)
        .enter().append("circle")
        .attr("class", "dot")
        .attr("r", 3.5)
        .attr("cx", function(d) { return x(d[x_field]); })
        .attr("cy", function(d) { return y(d[y_field]); })
        .style("fill", function(d) { return color(d.country); })
        .on("mouseover", function(d) {
            scatter_tooltip
                .transition()
                .duration(200)
                .style("opacity", .9);
            scatter_tooltip
                .text(d.country)
                .style("left", (d3.event.pageX + 5) + "px")
                .style("top", (d3.event.pageY - 28) + "px");
            })
        .on("mouseout", function(d) {
            scatter_tooltip
                .transition()
                .duration(500)
                .style("opacity", 0);
            });

    var legend = svg.selectAll(".legend")
        .data(color.domain())
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

};