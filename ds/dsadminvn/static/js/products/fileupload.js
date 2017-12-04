window.URL = window.URL || window.webkitURL;

/*
* Download main imgage
* */
//Add main imgage
function handleMainFileImg(files){
    if (files[0].size > 5000000){
        $('#modal_content').text('').text('Максимально допустимый размер файла 5 МБ');
        $('#modal_alarm').modal();
        return false;
    }
    if (files[0].type == 'image/jpg' || files[0].type == 'image/png' || files[0].type == 'image/jpeg'){
        var reader = new FileReader();
    //download file
        reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(document.getElementById('main_photo'));
        $('#del_main_photo').show();
    //read file in string base64
        reader.readAsDataURL(files[0]);
    }
    else{
        $('#modal_content').text('').text('Неверное расширение файла!!!Допустимые расширения  jpeg, png, jpg');
        $('#modal_alarm').modal();
    }
}
//Show window for download file/Delete selected image
$('#add_main_file_img').on("click", function (e) {
    $('#main_photo_path').click();
    e.preventDefault(); // prevent navigation to "#"
});
//Delete main photo
$('#del_main_photo').click(function () {
    //clear FileList
    var $el = $('#main_photo_path');
    $el.wrap('<form>').closest('form').get(0).reset();
    $el.unwrap();
    $(this).hide();
    $('#main_photo').attr('src', '/media/nophoto.png');
});

/*
* Download another images
* */

//Show window for add file
$('[data-anothe=anothe_img]').on("click", function (e) {
   $(this).prev().click();
   e.preventDefault(); // prevent navigation to "#"
});

//Load file
$('input[data-images=imgages-product]').change(function () {
    if ($(this)[0].files[0].size > 5000000){
        $('#modal_content').text('').text('Максимально допустимый размер файла 5 МБ');
        $('#modal_alarm').modal();
        return false;
    }
    if ($(this)[0].files[0].type == 'image/jpg' || $(this)[0].files[0].type == 'image/png' || $(this)[0].files[0].type == 'image/jpeg'){
        var reader = new FileReader();
    //download file
        reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })($(this).parent().next().children()[0]);
    //read file in string base64
        reader.readAsDataURL($(this)[0].files[0]);
        $(this).parent().next().next().children().show();
    }
    else{
        $('#modal_content').text('').text('Неверное расширение файла!!!Допустимые расширения  jpeg, png, jpg');
        $('#modal_alarm').modal();
        return false;
    }
});

//Delete one of another photo
$('[data-delete-imgs=delete-imgs]').click(function () {
    //clear FileList
    $(this).parent().prev().children().attr('src', '/media/nophoto.png');
    var $el = $(this).parent().prev().prev().children('input');
    $el.wrap('<form>').closest('form').get(0).reset();
    $el.unwrap();
    $(this).hide();
});