$(document).ready( function(){
/*
* Changes 'is_active' field for user data
* */
  $('#is_active_u').click(function () {
      $.get(
          "/users/ajaxuser/isactive/"+$(this).attr("data_info")+"/",
          onAjaxSuccess
        );
        function onAjaxSuccess(data)
        {
          if (data.status == true){
              $('#is_active_u').text("True").removeClass("btn-danger").addClass("btn-success")
          }
          else{
              $('#is_active_u').text("False").removeClass("btn-success").addClass("btn-danger")
          }
        }
  })
});
