const svg = d3.select('svg');
const WIDTH = svg.attr('width');
const HEIGHT = svg.attr('height');

const Scales = {
    linear: (min_value, max_value, start_pos, end_pos) => {
        return d3.scaleLinear()
                .range([start_pos, end_pos])
                .domain([min_value, max_value])
                .nice();
        },
    band: (months, start_pos, end_pos ) => {
        return d3.scaleBand()
                .range([start_pos, end_pos])
                .domain(months);
    }
}

let drawBars = (barChatLayer, data, xScale, yScale, barChartWidth, barChartHeight) => {
    let xAxis = d3.axisBottom(xScale);
    let yAxis = d3.axisLeft(yScale).ticks(5);
    barChatLayer.append('g')
        .attr("transform", "translate(0," + 2*(barChartHeight) + ")")
        .attr('class', 'x-axis')
        .call(xAxis)

    barChatLayer.append('g')
        .attr('class', 'y-axis')
        .call(yAxis);
    
    barChatLayer.selectAll('.bar')
        .data(data)
        .enter().append('rect')
        .attr('class', "bar")
        .attr("x", function(d){return xScale(d.month)})
        .attr('y', d => yScale(d.spending) )
        .attr('width', xScale.bandwidth())
        .attr('height', d => 2*barChartHeight-yScale(d.spending))
        .style('fill', '#cde3e0')
        .style('stroke', 'black')

    barChatLayer.append('g')
        .attr("class", 'axis-lable')
        .attr('transform', 'translate(0, -5)')
        .append("text")
        .style("text-anchor", 'middle')
        .text("Spending")
}

d3.json(spendingDataUrl).then(function(data){
    data.forEach(e => {
        e.spending = +e.spending;
      });

    console.log(data)
    const margin = {top: 100, bottom: 100, left: 100, right: 100}
    const width = WIDTH - margin.left-margin.right;
    const height = HEIGHT - margin.top;
    
    let months = data.map(d=>d.month)
    var xScale_bar = Scales.band(months, 0, width);
    const yScale_bar = Scales.linear(0, d3.max(data, (d)=> d.spending), height, 0);
    
    let barChartLayer = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + 50 +")");
    drawBars(barChartLayer, data, xScale_bar, yScale_bar, width, height/2);
});