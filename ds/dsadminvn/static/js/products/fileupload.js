window.URL = window.URL || window.webkitURL;

/*
* Download main imgage
* */
//Add main imgage
function handleMainFileImg(files){
    if (files[0].size > 5000000){
        alert('Максимальный размер файла 5 МБ');
        console.log(files);
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
        alert('Неправильное расширение файла');
    }
}
//Show window for download file/Delete selected image
$('#add_main_file_img').on("click", function (e) {
    $('#main_photo_path').click();
    e.preventDefault(); // prevent navigation to "#"
});

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
$('input[data-images=imgages-product]').change(function () {
    if ($(this)[0].files[0].size > 5000000){
        alert('Максимальный размер файла 5 МБ');
        //console.log(files);
        return false;
    }
    if ($(this)[0].files[0].type == 'image/jpg' || $(this)[0].files[0].type == 'image/png' || $(this)[0].files[0].type == 'image/jpeg'){
        var img = document.createElement("img");
        img.style.width="106px";
        img.style.height = "90px";
        $(this).prev('a').removeAttr("data-anothe").children('span').removeClass('fa-plus-circle');
        $(this).prev('a').prepend(img);
        //$(this).unbind();
        var reader = new FileReader();
    //download file
        reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
    //read file in string base64
        reader.readAsDataURL($(this)[0].files[0]);
        console.log(this.files);
    }
    else{
        alert('Неправильное расширение файла');
        return false;
    }
});