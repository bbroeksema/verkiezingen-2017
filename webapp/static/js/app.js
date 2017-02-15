var btn = document.getElementById('button_submit');
var input = document.getElementById('input_query');

function render(data) {
    data = data.sort(function(a, b) { return b[1] - a[1]; })
    var radarData = { labels : data.map(function(d) { return d[0]; }),
        datasets : [
            {
                label: "Uw termen komen overeen met",
                fillColor : "rgba(220,220,220,0.5)",
                strokeColor : "rgba(220,220,220,1)",
                data : data.map(function(d) { return d[1]; })
            }
        ]
    }
    var ctx = document.getElementById("radarChart").getContext("2d");
    var myRadarChart = new Chart(ctx, {
        type: 'radar',
        data: radarData,
        options: {
            scale: {
                ticks: {
                    beginAtZero: true
                }
            }
        }
    });
}

btn.addEventListener('click', function(event) {
    var query = "{ \"text\": \"" + input.value + "\" }"

    d3.request("/fit")
        .header("Content-Type", "application/json")
        .on("error", function(error) { console.log(error); })
        .on("load", function(xhr) { render(JSON.parse(xhr.responseText)); })
        .post(query);
});