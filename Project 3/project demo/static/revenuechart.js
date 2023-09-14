console.log("js connected")
const svg_ = d3.select('#revenuechart')
const width = svg_.attr('width');
const height = svg_.attr('height');
const margin = 30;
const radius = Math.min(width, height) / 2 - margin
const svg = svg_.append("g")
.attr("transform", `translate(${width/2}, ${height/2})`);

var monthURL = revenueMonthDataUrl  
var yearURL = revenueYearDataUrl


var arcGenerator = d3.arc()
    .innerRadius(0)
    .outerRadius(radius)

const pie = d3.pie()
    .value(function(d) {return d.value; })
    .sort(function(a, b) { return d3.ascending(a.key, b.key);} )
  
function update(dataUrl) {
    var data = d3.json(dataUrl).then(function(data){
        var color = d3.scaleOrdinal()
            .domain(data)
            .range(["#cde3e0", "#b7d6d0"]);
        // Compute the position of each group on the pie:
        const data_ready = pie(data);
        
            // map to data
        const u = svg.selectAll("path")
        .data(data_ready)
        
        u
        .join('path')
        // .transition()
        // .duration(1000)
        .attr('d', arcGenerator)
        .attr('fill', function(d){ return(color(d.data.type)) })
        .attr("stroke", "black")
        .style("stroke-width", "2px")

        const t = svg.selectAll("text")
        .data(data_ready)
        t
        .join('text')
        .text(function(d){ return d.data.type})
        .attr("transform", function(d) { return "translate(" + arcGenerator.centroid(d) + ")";  })
        .style("text-anchor", "middle")
        .style("font-size", 17)
    });
};

update(monthURL)
