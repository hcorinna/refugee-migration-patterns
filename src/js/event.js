var refresh_matrix = function(year){
    $('#matrix_grid').empty();
    $('#matrix_legend').empty();
    d3.queue()
    .defer(d3.json, "src/data/matrix.json")
    .await(function (error, data) {
        if (error) {
            console.error('Oh dear, something went wrong: ' + error);
        } else {
            cols = [];
            Object.keys(data[year][0]).forEach(function(col){
                if (col != 'index'){
                    cols.push(col);
                };
            });
            drawMatrix(data[year], cols);
        };
    });
};

var refresh_scatter = function(year){
    $('#scatter_first').empty();
    $('#scatter_second').empty();
    d3.queue()
    .defer(d3.json, "src/data/scatter.json")
    .await(function (error, data) {
        if (error) {
            console.error('Oh dear, something went wrong: ' + error);
        } else {
            var graph_data = [
                {
                    svg_css: '#scatter_first',
                    x_field: 'eigenvector_centrality',
                    y_field: 'closeness_centrality',
                    x_label: 'Eigenvector Centrality (In)',
                    y_label: 'Closeness Centrality (In)'
                },
                {
                    svg_css: '#scatter_second',
                    x_field: 'eigenvector_centrality_out',
                    y_field: 'out_closeness_centrality',
                    x_label: 'Eigenvector Centrality (Out)',
                    y_label: 'Closeness Centrality (Out)'
                }
            ];
            graph_data.forEach(function(graph){
                drawscatter(
                    data[year], 
                    graph.svg_css, 
                    graph.x_field, 
                    graph.y_field,
                    graph.x_label,
                    graph.y_label
                    );
            });
        };
    });
};


var refresh_power = function(year){
    console.log(year);
    src = 'src/media/' + year + '_powerlaw.png';
    $('#power_plot').attr('src', src);
};

var refresh_degree = function(year){
    src = 'src/media/' + year + '_degree_distribution.png';
    $('#degree_plot').attr('src', src);
};

var refresh_year = function(year){
    refresh_matrix(year);
    refresh_power(year);
    refresh_degree(year);
    refresh_scatter(year);
};