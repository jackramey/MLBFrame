/**
 * Created by jack on 6/30/17.
 */

var ctx = document.getElementById('myChart').getContext('2d');

$(function() {

  $('.list-group-item').on('click', function() {
    $('.glyphicon', this)
      .toggleClass('glyphicon-chevron-right')
      .toggleClass('glyphicon-chevron-down');
  });

});

$(document).ready(function() {
    var querystring = '?' + window.location.href.split('?')[1];
    $.ajax({url: "/differentials" + querystring, success: function(result){
        var json = $.parseJSON(result);
        var my_datasets = json.data.map(function (team_data) {
            return {
                label: team_data.team.abbrev,
                borderColor: team_data.team.color,
                fill: false,
                lineTension: 0,
                data: team_data.differentials
            }
        });
        var team_data = json.data[0].team;
        var line_data = json.data[0].differentials;
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'line',
            // The data for our dataset
            data: {
                labels: _.range(line_data.length),
                datasets: my_datasets
            },
            // Configuration options go here
            options: {
                scales: {
                    xAxes: [{
                        ticks: {
                            autoSkip: true,
                            maxTicksLimit: 10
                        }
                    }]
                }
            }
        });

    }});
});
