$(document).ready(function() {

var w = window,
    d = document,
    e = d.documentElement,
    g = d.getElementsByTagName('body')[0],
    width = w.innerWidth || e.clientWidth || g.clientWidth,
    height = w.innerHeight|| e.clientHeight|| g.clientHeight;

var color = d3.scale.category20();

var zoomer = d3.behavior.zoom()
                .scaleExtent([0.1,10])
                .on("zoom", zoom);
				
			
function zoom() {
    console.log("zoom", d3.event.translate, d3.event.scale);
    svg.attr("transform", 
             "translate(" + d3.event.translate + ")" 
                + " scale(" + d3.event.scale + ")"
             );
}


var svg = d3.select("#chart").append("svg")
	.attr("width", width)
	.attr("height", height) 
    .append("g")
		.attr("class", "graph")
        .call(zoomer); 
		
var force = d3.layout.force()
    .gravity(0.05)
    .distance(500)
    .charge(-700)
    .size([width, height]);
	
d3.json("characters.json", function(error, json) {
  if (error) throw error;
  force
      .nodes(json.nodes)
      .links(json.links)
      .start();
	  
  var link = svg.selectAll(".link")
      .data(json.links)
    .enter().append("line")
      .attr("class", "link")
      .style("stroke-width", function(d) { return d.value; });
	  
  var gnodes = svg.selectAll('g.gnode')
     .data(json.nodes)
     .enter()
     .append('svg:g')
     .classed('gnode', true);
	 
  var node = gnodes.append("circle")
      .attr("class", "node")
      .attr("r", function(d){ return 10 * Math.sqrt(d.weight) ;})
      .style("fill", function(d) { return color(d.weight); })
	  .call(force.drag)
	  .on("dblclick", fade(0))
	  .on("click", fade(1));
  node.append("title")
      .text(function(d) { return d.name ; });
	  
  var labels = gnodes.append("text")
      .text(function(d) { return d.name; })
	  .style("font-size", "20px");
	  
  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });
    gnodes.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
	});
	
  var linkedByIndex = {};
    json.links.forEach(function(d) {
        linkedByIndex[d.source.index + "," + d.target.index] = 1;
    });

  function isConnected(a, b) {
    return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index] || a.index == b.index;
    }
	
		
  function fade(opacity) {
        return function(d) {
            gnodes.style("stroke-opacity", function(o) {
                thisOpacity = isConnected(d, o) ? 1 : opacity;
                this.setAttribute('fill-opacity', thisOpacity);
                return thisOpacity;
            });

            link.style("stroke-opacity", function(o) {
                return o.source === d || o.target === d ? 1 : opacity;
            });
        };
    }

  });
});