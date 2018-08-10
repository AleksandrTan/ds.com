$( "#found_product" ).submit(function (e) {
    $('#hellopreloader_preload').css({'display':'block', 'opacity': '0.5'});
    e.preventDefault();
    $.get(
        "/adminnv/products/barcode/getproduct/"+$('#barcode_articul').val()+"/",
        onAjaxSuccess
       );
       function onAjaxSuccess(data) {
           if(data.status){
               $('#hellopreloader_preload').css({'display':'none', 'opacity': '0.5'});
           	   alert(2000);
           }
           else {
               $('#hellopreloader_preload').css({'display':'none', 'opacity': '0.5'});
               alert(1000);
           }
       }
});

$( "#found_product" ).on('input', function (e) {
    if ($('#barcode_articul').val().length == 13){
        $(this).submit();
    }
});
