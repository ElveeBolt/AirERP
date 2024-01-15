    new DataTable('#dataTable', {
        bLengthChange: false,
        bInfo: false,
        columnDefs: [
           {
               orderable: false,
               targets: -1
           }
        ],
        language: {
            paginate: {
                "first": "<<",
                "last": ">>",
                "next": ">",
                "previous": "<"
            },
            searchPlaceholder: "Search items..."
        },
    });

    $('[data-modal-toggle]').on('click', function (event) {
        var action = $(this).attr("data-modal-attr-action");
        var title = $(this).attr("data-modal-attr-title");
        $('#popup-modal form').attr('action', action);
        $('#popup-modal #title').text(title);
    });