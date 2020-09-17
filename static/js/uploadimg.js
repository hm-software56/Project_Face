$(document).ready(function (e) {
    $('#upload').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles').files.length;

        if (ins < 5) {
            $('#msg').html('<span style="color:red">ທ່ານຕ້ອງເລຶອກຮູບຢ່າງໜ້ອຍ 5 ຮູບ</span>');
            return;
        }

        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles').files[x]);
        }

        $.ajax({
            url: 'uploadfile', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            beforeSend: function () {
                $("#done").html('<img src="static/default/loading.gif" class="rounded mx-auto d-block img-thumbnail img-fluid">')
                document.getElementById("close_pr").style.display = 'none';
            },
            success: function (data) {
                $("#done").html('<img src="static/default/done.jpg" class="rounded mx-auto d-block img-thumbnail img-fluid">')
                document.getElementById("next_reg").style.display = 'block';
                //$('#exampleModal').modal('hide');
                // $('body').removeClass('modal-open');
                //$('.modal-backdrop.show').css('opacity', '0');
                //$('.modal-backdrop').css('z-index', '-1', 'position', 'static');
            },
            error: function (response) {
                $('#msg').html(response.message); // display error response
            }
        });
        return false;
    });
});