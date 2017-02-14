var btn = document.getElementById('button_submit');
var input = document.getElementById('input_query');



btn.addEventListener('click', function(event) {
    var query = "{ \"text\": \"" + input.value + "\" }"

    d3.request("/fit")
        .header("Content-Type", "application/json")
        .on("error", function(error) { console.log(error); })
        .on("load", function(prediction) { console.log(prediction); })
        .post(query);
});