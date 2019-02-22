var refresh_matrix = function(year){
    console.log(year);
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

var refresh_year = function(year){
    refresh_matrix(year);
};