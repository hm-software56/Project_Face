$(document).ready(function (e) {
    $('#upload_img_detect').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles').files.length;

        if (ins < 1) {
            $('#msg').html('<span style="color:red">ທ່ານຕ້ອງເລຶອກຮູບຢ່າງໜ້ອຍ  ຮູບ</span>');
            return;
        }

        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles').files[x]);
        }

        $.ajax({
            url: 'uploadfiledetect', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            beforeSend: function () {
                $("#result").html('<img src="static/default/loading.gif" class="rounded mx-auto d-block img-thumbnail img-fluid">');
            },
            success: function (data) {
                $("#result").html(data.result);
                $('#modal_detect').modal('hide');
                $('body').removeClass('modal-open');
                $('.modal-backdrop.show').css('opacity', '0');
                $('.modal-backdrop').css('z-index', '-1');
            },
            error: function (response) {
                $('#msg').html(response.message); // display error response
            }
        });
        return false;
    });
});