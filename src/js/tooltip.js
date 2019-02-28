var tooltip;

/**
 * Execute once page has been fully loaded.
 */
$(function() {
  tooltip = d3.select("body")
    .append("div")
    .attr("class", "tooltip hidden");
});

/**
 * Shows the tooltip. There is just one for the whole page
 * @param  {String} label The label to display
 * @param  {Array} offset_xy Distance to the mouse pointer (x and y value)
 */
function showTooltip(label, offset_xy = [10,-35]) {
  var mouse = [d3.event.pageX, d3.event.pageY]
  tooltip.classed("hidden", false)
    .attr("style", "left:"+(mouse[0]+offset_xy[0])+"px;top:"+(mouse[1]+offset_xy[1])+"px")
    .html(label);
};

/**
 * Hides the tooltip
 */
function hideTooltip() {
  tooltip.classed("hidden", true);
}
