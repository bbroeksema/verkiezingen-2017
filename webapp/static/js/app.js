var btn = document.getElementById('button_submit');
var input = document.getElementById('input_query');

function renderPredicton(prediction) {
    data = prediction.sort(function (a, b) {
        return d3.ascending(a[1], b[1]);
    });

    var margin = { top: 15, right: 25, bottom: 15, left: 200 };
    var width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var svg = d3.select("#div_results").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var x = d3.scaleLinear()
        .range([0, width])
        .domain([0, d3.max(data, function (d) {
            return d[1];
        })]);

    var y = d3.scaleBand()
        .rangeRound([height, 0], .1)
        .domain(data.map(function (d) {
            return d[0];
        }));

    var yAxis = d3.axisLeft(y)
        .tickSize(0);

    var gy = svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)

    var bars = svg.selectAll(".bar")
        .data(data)
        .enter()
        .append("g")

    //append rects
    bars.append("rect")
        .attr("class", "bar")
        .attr("y", function (d) {
            return y(d[0]);
        })
        .attr("height", y.bandwidth())
        .attr("x", 0)
        .attr("width", function (d) {
            return x(d[1]);
        });
}

btn.addEventListener('click', function(event) {
    var query = "{ \"text\": \"" + input.value + "\" }"

    d3.request("/fit")
        .header("Content-Type", "application/json")
        .on("error", function(error) { console.log(error); })
        .on("load", function(xhr) { renderPredicton(JSON.parse(xhr.responseText)); })
        .post(query);
});