var tooltip;

/**
 * Execute once page has been fully loaded.
 */
$(function() {
  tooltip = d3.select("body")
    .append("div")
    .attr("class", "tooltip hidden");
});

function showTooltip(d, label, offset_xy = [10,-35]) {
  var mouse = [d3.event.pageX, d3.event.pageY]
  tooltip.classed("hidden", false)
    .attr("style", "left:"+(mouse[0]+offset_xy[0])+"px;top:"+(mouse[1]+offset_xy[1])+"px")
    .html(label);
};

function hideTooltip() {
  tooltip.classed("hidden", true);
}
