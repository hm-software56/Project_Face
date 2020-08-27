setTimeout(function () {
    $.ajax({
        url: '/getdata',
        dataType: "json",
        success: function (data) {
            $("#result_person").html(data.result)
        },
    });
    return false
}, 100000000);