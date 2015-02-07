/**
 * Created by jaha on 7.2.2015.
 */

var graphOptions = {
    series: {
        lines: {show: true},
        points: {show: true},
        color: "#b7003d"
    },
    xaxis: {
        mode: "time",
        timeformat: "%H:%M",
        timezone: "browser",

        font: {
            color: "#AAA",
            size: 12,
            weight: "normal"
        }
    },
    yaxis: {
        tickDecimals: 1,
        font: {
            color: "#AAA",
            size: 20,
            weight: "bold"
        }
    }
};

function plot_graph(sensor_id) {
    var selector;
    var plot;
    selector = "api/temperature?q={\"filters\":[{\"name\": \"sensor_id\", \"op\": \"eq\", \"val\": \""
    + sensor_id + "\"}], \"order_by\":[{\"field\": \"time\", \"direction\": \"desc\"}], \"limit\":16}";
    var graphValues = [[]];
    $.get(selector).success(function (data) {
        graphValues = new Array(data.objects.length);
        for (var i = 0; i < data.objects.length; i++) {
            graphValues[i] = [data.objects[i].time * 1000, data.objects[i].temperature.toFixed(1)];
        }
        plot = $.plot($("#" + sensor_id + "_graph"), [graphValues], graphOptions);
    });
}