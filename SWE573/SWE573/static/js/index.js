$(window).on('load', function () {
    $('#loading').hide();
});

$('#main_form').submit(function(){
    $('#loading').show();
});

function drawEmptyChart() {
    var ctx = document.getElementById("result_chart").getContext('2d');

    var empty_chart = new Chart(ctx, {
        type: 'line'
    });
}

function drawChart(result) {
    var res = htmlDecode(result).replace(/'/g, "\"");
    var obj = JSON.parse(res);

    var neg_array = [];
    var pos_array = [];
    var neu_array = [];
    var comp_array = [];

    for (var i = 0; i < Object.keys(obj).length; i++) {
        pos_array[i] = Object.values(obj)[i]["pos"];
        neu_array[i] = Object.values(obj)[i]["neu"];
        comp_array[i] = Object.values(obj)[i]["compound"];
        neg_array[i] = Object.values(obj)[i]["neg"];
    }

    var ctx = document.getElementById("result_chart").getContext('2d');

    var result_chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(obj),
            datasets: [
                {
                    label: 'Positivity Score',
                    backgroundColor: '#008000',
                    borderColor: '#008000',
                    data: pos_array,
                    fill: false,
                },
                {
                    label: 'Negativity Score',
                    backgroundColor: '#ff0000',
                    borderColor: '#ff0000',
                    data: neg_array,
                    fill: false
                },
                /*
                {
                    label: 'Neutrality Score',
                    backgroundColor: '#a8adb4',
                    borderColor: '#a8adb4',
                    data: neu_array,
                    fill: false
                },
                */
                {
                    label: 'Compound Score',
                    backgroundColor: '#ffff00',
                    borderColor: '#ffff00',
                    data: comp_array,
                    fill: false
                }
            ]
        }
    })
}

function htmlDecode(input) {
    var e = document.createElement('div');
    e.innerHTML = input;
    return e.childNodes[0].nodeValue;
}