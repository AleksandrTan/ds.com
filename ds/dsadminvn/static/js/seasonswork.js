$(document).ready( function(){
/*
* Add new main season data
* */
  $('#add_new_se').click(function () {

          var new_name = $('#new_name_se').val();

          if(new_name == ''){
              alert('Enter correct data for new type!!!');
              return false;
          }
          $.get(
              "/adminnv/seasons/ajax/addnew/",
              {
                  name: new_name,

              },
              onAjaxSuccess
            );
            function onAjaxSuccess(data)
            {
              if (data.status){
                  if ($('#se_list tr:last-child td:first-child').text() == ''){
                      var num_n = 1;
                  }
                  else{
                      var num_n = +$('#br_list tr:last-child td:first-child').text() + 1;
                  }

                  var new_type = '<tr><td>'+num_n+'</td><td class="text-center">'+new_name+'</td><td class="text-center"><button type="button"'+
                                    'class="btn btn-sm btn-danger" data_info = "'+data.id+'">False</button></td><td class="text-center">'+
                                    ''+data.name_url+'</td><td class="text-center"><a type="button" data_delete="delete" id="'+data.id+'"'+
                                    'class="btn btn-sm btn-danger" href="/adminnv/seasons/deletese/'+data.id+'/">Delete</a></td>';

                  $('#se_list').append(new_type);
                  $('#new_name_se').val('');
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
              "/adminnv/seasons/ajax/isactive/"+$(this).attr("data_info")+"/",
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