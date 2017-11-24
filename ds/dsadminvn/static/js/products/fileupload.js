window.URL = window.URL || window.webkitURL;

/*
* Download main imgage
* */
//Add main imgage
function handleMainFile(files){
    if (files[0].size > 5000000){
        alert('Максимальный размер файла 5 МБ');
        return false;
    }
    if (files[0].type == 'image/jpg' || files[0].type == 'image/png' || files[0].type == 'image/gif' || files[0].type == 'image/jpeg'){
        var img = document.createElement("img");
        img.style.width="106px";
        img.style.height = "90px";
        document.getElementById('main_file_select').insertBefore(img, document.getElementById('before_img'));
        var reader = new FileReader();
    //download file
        reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
    //read file in string base64
        reader.readAsDataURL(files[0]);
        $('#before_img').css({'font-size':'23px', 'top':'22px', 'left':'12px', 'color':'red'})
                        .removeClass('fa-plus-circle')
                        .addClass('fa-minus-circle')
                        .attr('title', 'Удалить фото');
        $('#main_img_isset').val(1);
    }
    else{
        alert('Неправильное расширение файла');
    }
}
//Show window for download file/Delete selected image
$('#main_file_select').on("click", function (e) {
    if ($('#before_img').hasClass('fa-minus-circle')){
            $('#before_img').css({'font-size':'41px', 'top':'50px', 'left':'50px', 'color':'#0e76bd'})
                            .removeClass('fa-minus-circle')
                            .addClass('fa-plus-circle')
                            .attr('title', 'Добавить фото')
                            .prev('img').remove();
            $('#main_img_isset').val(0);
            return false;
    }
    else{
        $('#main_file_img').click();
        e.preventDefault(); // prevent navigation to "#"
    }
});

/*
* Download another images
* */

$('[data-anothe=anothe_img]').on("click", function (e) {
   $(this).children('img').remove();
   var data_json_img = $.parseJSON($('#othe_img_isset').val());
   var num_img = parseInt($(this).next().attr('data-num-img'));
   data_json_img[num_img] = 0;
   $('#othe_img_isset').val(JSON.stringify(data_json_img));
   console.log(data_json_img);
   $(this).next().click();
   e.preventDefault(); // prevent navigation to "#"
});

$('input[data-anothe=other_img]').change(function () {
    if ($(this)[0].files[0].size > 5000000){
        alert('Максимальный размер файла 5 МБ');
        return false;
    }
    if ($(this)[0].files[0].type == 'image/jpg' || $(this)[0].files[0].type == 'image/png' || $(this)[0].files[0].type == 'image/gif' || $(this)[0].files[0].type == 'image/jpeg'){
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
        var data_json_img = $.parseJSON($('#othe_img_isset').val());
        var num_img = parseInt($(this).attr('data-num-img'));
        data_json_img[num_img] = 1;
        $('#othe_img_isset').val(JSON.stringify(data_json_img));
        console.log(data_json_img);
    }
    else{
        alert('Неправильное расширение файла');
    }
});
// var SomeCl = {
// 	count: 0,
//   init: function(){
//   	$('#images').change(this.onInputChange);
//   },
//   onInputChange: function() {
//   	SomeCl.addM(this.files);
//   },
//   addM: function(files) {
// 		for(var i=0;i<4;i++) {
//
//
//       if(files[i].type.substr(0,5) == 'image') {
//       (function(file) {
// 					var reader = new FileReader();
//           var info = {
// 					name: files[i].name,
// 					size: files[i].size,
// 					type: files[i].type,
// 					preview: '/newtest/resources/images/dvlogo.png'
// 				};
// 					reader.onload = function(e) {
//           	SomeCl.count++;
// 						info.preview = e.target.result;
// 						console.log(SomeCl.count + " -")
// 						SomeCl.processM(info);
// 					};
// 					reader.readAsDataURL(files[i]);
//           })(files[i]);
// 				}else{
// 					this.processFile(info);
// 				}
//     }
//   },
//   processM: function(file) {
//   	console.log(file);
//     $('.container').append('11111111111111111<br>');
//   },
// }
// SomeCl.init();