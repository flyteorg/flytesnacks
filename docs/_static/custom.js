function resizePlotly() {
    var plotly = jQuery( ".plotly-graph-div" )
    plotly.attr("style", "height: 100%; width: 100%;")
    window.dispatchEvent(new Event('resize'));
    plotly.addClass("show");
}

jQuery(document).ready(function() {
    // make sure that plotly plots only take 100% of the width of the container
    resizePlotly()
})
