var client = {
    list: function () {
        $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search'
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                {"data": "id"},
                {"data": "names"},
                {"data": "dni"},
                {"data": "birthdate"},
                {"data": "gender.name"},
                {"data": "state"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<span class="badge badge-success badge-pill">Activo</span>';
                        }
                        return '<span class="badge badge-danger badge-pill">Inactivo</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="' + pathname + 'update/' + row.id + '/" class="btn btn-warning btn-sm"><i class="fas fa-edit"></i></a> ';
                        if (row.state) {
                            buttons += '<a href="' + pathname + 'delete/' + row.id + '/" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></a> ';
                        }
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
    }
};

$(function () {
    client.list();
});
