$(function () {
    $('#predict_capture').bind('click', function () {
        $.ajax({
            url: '/predict?type=capture',
            //url: '/predict?type=webcam',
            dataType: "json",
            beforeSend: function () {
                $("#result").html('<img src="static/default/loading.gif" class="rounded mx-auto d-block img-thumbnail img-fluid">');
            },
            success: function (data) {
                $("#result").html(data.result)
                document.getElementById('name').value = '';
            },
        });
        return false;
    });

    $('#predict_webcame').bind('click', function () {
        $.ajax({
            url: '/predict?type=webcam',
            //url: '/predict?type=webcam',
            data: $('#form').serialize(),
            dataType: "json",
            beforeSend: function () {
                $("#result").html('<img src="static/default/loading.gif" class="rounded mx-auto d-block img-thumbnail img-fluid">')
            },
            success: function (data) {
                $("#result").html(data.result)
                document.getElementById('name').value = '';
            },
        });
        return false;
    });

    $('#predict_img').bind('click', function () {
        $.ajax({
            url: '/predict?type=img',
            dataType: "json",
            beforeSend: function () {
                $("#result").html('<img src="static/default/loading.gif" class="rounded mx-auto d-block img-thumbnail img-fluid">')
            },
            success: function (data) {
                $("#result").html(data.result)
                document.getElementById('name').value = '';
            },
        });
        return false;
    });

    $('#trainer').bind('click', function () {
        $.ajax({
            url: '/trainer',
            dataType: "json",
            beforeSend: function () {
                $("#result").html('<img src="static/default/loading.gif" class="rounded mx-auto d-block img-thumbnail img-fluid">')
            },
            success: function (data) {
                $("#result").html(data.result)
                document.getElementById('name').value = '';
            },
        });
        return false;
    });

    $('#clear').bind('click', function () {
        $.ajax({
            url: '/getdata?clear=True',
            dataType: "json",
            success: function (data) {
                $("#result_person").html(data.result)
            },
        });
        return false;
    });

    $('#img').bind('click', function () {
        document.getElementById('action').value = 'img';
    });
    $('#webcam').bind('click', function () {
        document.getElementById('action').value = 'webcam';
    });

    $('#form_dataset').on('submit', function (e) {
        $.ajax({
            type: 'post',
            url: '/setdataset',
            cache: false,
            data: $('#form_dataset').serialize(),
            beforeSend: function () {
                $("#result").html('<img src="static/default/loading.gif" class="rounded mx-auto d-block img-thumbnail img-fluid">')
            },
            success: function (data) {
                $("#result").html(data.result)
                document.getElementById('name').value = '';
                document.getElementById('action').value = '';
            }
        });
        e.preventDefault();
    });
});

function uploaimg(theForm) {
    $.ajax({
        type: 'post',
        url: '/setdataset',
        cache: false,
        data: $(theForm).serialize(),
        beforeSend: function () {
            $("#result").html('<img src="static/default/loading.gif" class="rounded mx-auto d-block img-thumbnail img-fluid">')
        },
        success: function (data) {
            $("#result").html(data.result);
        }
    });
}