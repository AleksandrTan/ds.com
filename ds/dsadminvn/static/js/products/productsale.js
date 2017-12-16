$(document).ready(function () {
    $('#size' ).change(function () {
    	$('#in_stock').text(sizecount[$(this).val()]);
    });
//Set count_num value
    $('#count_num').keyup(function () {
        if ($(this).val() > $('#in_stock').text()){
            $('#is_deleted_ctr').modal();
            $(this).val(0);
        }
    });
//Set lost_num value
    $('#lost_num').change(function () {
        var start_price = $('#start_price').val();
        $('#price').text(start_price - $(this).val());
    })
});
