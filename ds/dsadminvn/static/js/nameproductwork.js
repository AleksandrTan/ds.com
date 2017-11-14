$(document).ready( function(){
/*
* Add new main category data
* */
  $('#add_new_np').click(function () {

          var new_name = $('#new_name_np').val();

          if(new_name == ''){
              alert('Enter correct data for new type!!!');
              return false;
          }
          $.get(
              "/adminnv/nameproduct/ajax/addnewproduct/",
              {
                  name: new_name,

              },
              onAjaxSuccess
            );
            function onAjaxSuccess(data)
            {
              if (data.status){
                 var new_type = '<tr><td class="text-center">'+new_name+'</td><td class="text-center"><button type="button"'+
                                    'class="btn btn-sm btn-danger" data_info = "'+data.id+'">False</button></td><td class="text-center">'+
                                    ''+data.name_url+'</td><td class="text-center"><a type="button" data_delete="delete" id="'+data.id+'"'+
                                    'class="btn btn-sm btn-danger" href="/adminnv/nameproduct/deletenp/'+data.id+'/">Delete</a></td>';

                  $('#np_list').append(new_type);
                  $('#new_name_np').val('');
              }
            }

  });
/*
* Changes 'is_active' field for main category
* */
  $("tbody").on("click", "button", function () {
    if($(this).attr('data_info')){
          var that = $(this)
          $.get(
              "/adminnv/nameproduct/ajax/isactivenp/"+$(this).attr("data_info")+"/",
              onAjaxIsActive
            );
            function onAjaxIsActive(data)
            {
              if (data.status == true){
                  that.text("True").removeClass("btn-danger").addClass("btn-success")
              }
              else{
                  that.text("False").removeClass("btn-success").addClass("btn-danger")
              }
            }
      }
  });


/*
* Delete main category
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

/*
* Form Change max_num/paid_num add free sentence for 'max_num'/'paid_num' field Category
* */

$("tbody").on("click", "button", function () {
        if($(this).attr('data-change')) {
            $('#num_max_id').val($(this).attr('data-change'));
            $('#key_field').val('max_num');
            $('#change_max_num_modal').modal();
        }
        else if ($(this).attr('data-change-num')){
            $('#num_max_id').val($(this).attr('data-change-num'));
            $('#key_field').val('paid_num');
            $('#change_max_num_modal').modal();
        }
    });

/*
* Change max_num/paid_num
* */
  $('#save_type_chenge').click(function () {
          var new_num = $('#new_num_max').val();
          var id = $('#num_max_id').val();
          var name_field = $('#key_field').val();
          //console.log(/^\d+$/.test(new_num));return false;
          //console.log(new_num.match(/^[-\+]?\d+/));return false;
          if(new_num == '' || new_num.match(/^[-\+]?\d+/) == null){
              alert('Enter correct data for new num!!!');
              return false;
          }
          $.get(
              "/ctr/ajaxctr/newnum/",
              {
                  num: new_num,
                  id:id,
                  name_field:name_field
              },
              onAjaxSuccess
            );
            function onAjaxSuccess(data)
            {
              if (data.status){
                    $('#change_max_num_modal').modal('hide');
                    if (name_field == 'max_num'){
                        $('#cat_'+id).text(new_num);
                    }
                    else {
                        $('#paid_'+id).text(new_num);
                    }
             }
            }
});
