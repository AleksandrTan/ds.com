/**
 * Created by user on 06.09.2018.
 */
$(document).ready( function(){
/*
* Delete discount
* */
    $("tbody").on("click", "a", function () {
        if($(this).attr('data_delete')){
            $('#is_deleted_ctr').modal();
            $('#delete_type').attr('data_id_type', $(this).attr('href'));
            return false;
         }
         return false;
    });

    $('#cancel_type').click(function () {
        $('#is_deleted_ctr').modal('hide');
        $('#delete_type').attr('data_id_type', '');
        return false;
    });


    $('#delete_type').click(function () {
        $('#is_deleted_ctr').modal('hide');
        var url = $(this).attr('data_id_type');
        $(location).attr('href',url);
    });
});