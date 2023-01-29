var input_year_month;
var report = {
    list: function () {
        var parameters = {
            'action': 'search',
            'year': input_year_month.datetimepicker('date').format("YYYY"),
            'month': input_year_month.datetimepicker('date').format("MM"),
        };
        $.ajax({
            url: pathname,
            data: parameters,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (request) {
                console.log(request);
                if (!request.hasOwnProperty('error')) {
                    Highcharts.chart('chart', {
                        title: {
                            text: 'Gráfico de los mejores clientes'
                        },
                        subtitle: {
                            text: ''
                        },
                        exporting: false,
                        yAxis: {
                            min: 0,
                            title: {
                                text: 'Valores'
                            }
                        },
                        xAxis: {
                            categories: request.categories
                        },
                        series: [{
                            type: 'column',
                            name: 'Total',
                            colorByPoint: true,
                            data: request.series,
                            showInLegend: false
                        }]
                    });
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            }
        });
    }
};

$(function () {
    input_year_month = $('input[name="year_month"]');

    input_year_month.datetimepicker({
        viewMode: 'years',
        format: 'MM/YY',
        useCurrent: false,
        locale: 'es',
        date: new Date(),
    });

    input_year_month.on('change.datetimepicker', function (e) {
        report.list();
    });

    report.list();
});