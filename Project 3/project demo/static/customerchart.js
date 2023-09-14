console.log("js connected")
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

let drawBars1 = (barChatLayer, data, xScale, yScale, barChartWidth, barChartHeight) => {
    let xAxis = d3.axisBottom(xScale);
    let yAxis = d3.axisLeft(yScale).ticks(d3.max(data.map(d=>d.number_of_tickets)));
    barChatLayer.append('g')
        .attr("transform", "translate(0," + barChartHeight + ")")
        .attr('class', 'x-axis')
        .call(xAxis)

    barChatLayer.append('g')
        .attr('class', 'y-axis')
        .call(yAxis);
    
    barChatLayer.selectAll('.bar')
        .data(data)
        .enter().append('rect')
        .attr('class', "bar")
        .attr("x", function(d){return xScale(d.name)})
        .attr('y', d => yScale(d.number_of_tickets) )
        .attr('width', xScale.bandwidth())
        .attr('height', d => barChartHeight-yScale(d.number_of_tickets))
        .style('fill', '#cde3e0')
        .style('stroke', 'black')

    barChatLayer.append('g')
        .attr("class", 'axis-lable')
        .attr('transform', 'translate(0, -5)')
        .append("text")
        .style("text-anchor", 'middle')
        .text("Number of Tickets")
}

let drawBars2 = (barChatLayer, data, xScale, yScale, barChartWidth, barChartHeight) => {
    let xAxis = d3.axisBottom(xScale);
    let yAxis = d3.axisLeft(yScale).ticks(5);
    barChatLayer.append('g')
        .attr("transform", "translate(0," + (barChartHeight) + ")")
        .attr('class', 'x-axis')
        .call(xAxis)

    barChatLayer.append('g')
        .attr('class', 'y-axis')
        .call(yAxis);
    
    barChatLayer.selectAll('.bar')
        .data(data)
        .enter().append('rect')
        .attr('class', "bar")
        .attr("x", function(d){return xScale(d.name)})
        .attr('y', d => yScale(d.spending) )
        .attr('width', xScale.bandwidth())
        .attr('height', d => barChartHeight-yScale(d.spending))
        .style('fill', '#b7d6d0')
        .style('stroke', 'black')

    barChatLayer.append('g')
        .attr("class", 'axis-lable')
        .attr('transform', 'translate(0, -5)')
        .append("text")
        .style("text-anchor", 'middle')
        .text("Commission")
}

const margin = {top: 100, left: 100, right: 100, gap: 100}
const width = (WIDTH-margin.left-margin.right)/2;
const height = HEIGHT - margin.top;

d3.json(ticketDataUrl).then(function(data){
    data.forEach(e => {
        e.number_of_tickets = +e.number_of_tickets;
      });
    
    let names = data.map(d=>d.name)
    var xScale_bar = Scales.band(names, 0, width);
    const yScale_bar1 = Scales.linear(0, d3.max(data, (d)=> d.number_of_tickets), height, 0);
    
    let barChartLayer1 = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + 50 +")");
    
    drawBars1(barChartLayer1, data, xScale_bar, yScale_bar1, width, height);
});

d3.json(commissionDataUrl).then(function(data){
    data.forEach(e => {
        e.spending = +e.spending;
      });

    let names = data.map(d=>d.name)
    var xScale_bar = Scales.band(names, 0, width);
    const yScale_bar2 = Scales.linear(0, d3.max(data, (d)=> d.spending), height, 0);

    let barChartLayer2 = svg.append("g")
    .attr("transform", "translate(" + (margin.left + width + margin.gap) + "," + 50 +")");

    drawBars2(barChartLayer2, data, xScale_bar, yScale_bar2, width, height);
});