/**
 * Created by jack on 6/30/17.
 */

var ctx = document.getElementById('myChart').getContext('2d');

var chart = new Chart(ctx);

$(function () {
    $('.list-group-item').on('click', function () {
        $('.glyphicon', this)
            .toggleClass('glyphicon-chevron-right')
            .toggleClass('glyphicon-chevron-down');
    });
    $('#nlw').click(function () {
        location.href='/?division=nlw';
    });
    $('#nlc').click(function () {
        location.href='/?division=nlc';
    });
    $('#nle').click(function () {
        location.href='/?division=nle';
    });
    $('#alw').click(function () {
        location.href='/?division=alw';
    });
    $('#alc').click(function () {
        location.href='/?division=alc';
    });
    $('#ale').click(function () {
        location.href='/?division=ale';
    });
});

function updateChart(division) {
    var querystring = '?' + division;
    $.ajax({
        url: "/differentials" + querystring, success: function (result) {
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
                                min: 0,
                                maxTicksLimit: 20
                            }
                        }]
                    }
                }
            });

        }
    });
}

$(document).ready(function () {
    var querystring = '?' + window.location.href.split('?')[1];
    $.ajax({
        url: "/differentials" + querystring, success: function (result) {
            var json = $.parseJSON(result);
            var my_datasets = json.data.map(function (team_data) {
                return {
                    label: team_data.team.abbrev,
                    borderColor: team_data.team.color,
                    backgroundColor: team_data.team.color,
                    fill: false,
                    lineTension: 0,
                    data: team_data.differentials
                }
            });
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
                                min: 0,
                                maxTicksLimit: 20
                            }
                        }]
                    }
                }
            });

        }
    });
});
