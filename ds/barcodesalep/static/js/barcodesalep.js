$( "#found_product" ).submit(function (e) {
    $('#hellopreloader_preload').css({'display':'block', 'opacity': '0.5'});
    return false;
});

$( "#found_product" ).on('input', function (e) {
    if ($('#barcode_articul').val().length == 13){
        $('#hellopreloader_preload').css({'display':'block', 'opacity': '0.5'});
    //alert(1000);
        return false;
    }
});
