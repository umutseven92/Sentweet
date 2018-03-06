
function drawChart(result) {
    var res = htmlDecode(result).replace(/'/g, "\"");
    var obj = JSON.parse(res);

    var ctx = document.getElementById("result_chart").getContext('2d');

    var result_chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(obj),
            datasets:[{
                label: 'Compound Score',
                backgroundColor: '#008000',
                borderColor:'#008000',
                data: Object.values(obj),
                fill: false
            }]
        }
    })
}

function htmlDecode(input){
  var e = document.createElement('div');
  e.innerHTML = input;
  return e.childNodes[0].nodeValue;
}