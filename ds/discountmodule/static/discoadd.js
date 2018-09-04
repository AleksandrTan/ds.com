/*
* Identifier for debug mode(if true - form submited on server)
* */
var is_validate_js = true;
$.validator.setDefaults( {
    submitHandler: function () {
	       		       if (is_validate_js){
			               $( "#add_new_product" ).submit(function (e) {
			                                            $('#hellopreloader_preload').css({'display':'block', 'opacity': '0.5'});
			                                            var form = this;
                                                        form.submit();
                            });
                    }
     		 }
		});
$(document).ready(function () {

//Check isset articul
$('#articul').blur(function () {
   if ($(this).val() != ''){
       $.get(
        "/adminnv/products/checkarticul/"+$(this).val()+"/",
        onAjaxSuccess
       );
       function onAjaxSuccess(data) {
           if(data.status){
           	   $('#articul').val('');
               $('#modal_content').text('').text('Введенный артикул уже существует!Выберите другой');
               $('#modal_alarm').modal();
           }
       }
   }

});

//Check isset modelss
$('#modelss').blur(function () {
    if ($(this).val() != ''){
       $.get(
        "/adminnv/products/checkmodelss/"+$(this).val()+"/",
        onAjaxSuccess
       );
       function onAjaxSuccess(data) {
           if(data.status){
           	   $('#modelss').val('');
               $('#modal_content').text('').text('Введенная модель уже существует!Выберите другую');
               $('#modal_alarm').modal();
           }
       }
   }

});
//Show count entered simbols for input tags
    $("input").keyup(function() {
        $(this).next('[data-num = count_simbols]').next('span').css('display', 'block').children('em').text(this.value.length);
        if (this.value.length > parseInt($(this).next('[data-num = count_simbols]').data( "count" ))){
            $(this).next('[data-num = count_simbols]').next('span').css('color', 'red').children('em').text(this.value.length);
        }
        else{
            $(this).next('[data-num = count_simbols]').next('span').css('color', 'green').children('em').text(this.value.length);
        }
        if(this.value.length == 0){
            $(this).next('[data-num = count_simbols]').next('span').css('display', 'none');
        }
    });

//Validations form

    $( "#add_new_product" ).validate( {
				rules: {
					articul: {
						required: true,
						maxlength: 6
					},
					pre_barcode: {
						required: true,
						maxlength: 5,
                        number: true
					},
					price: {
						//required: true,
						number: true,
						maxlength: 50
					},
					wholesale_price: {
						number: true,
						maxlength: 50
					},
					purshase_price: {
					    number: true,
						maxlength: 50
					},
					meta_info: {
					    required: false,
						maxlength: 500
					},
					caption:{
						required: true,
						maxlength: 100
					}

				},
				messages: {
					articul: {
						required: "Пожалуйста введите артикул",
						maxlength: "Не более 6 символов"
					},
                    pre_barcode: {
						required: "Пожалуйста введите штрих-код",
						maxlength: "Не более 5 символов",
                        number: 'Должно быть числом!'
					},
					price: {
						number: 'Должно быть числом!',
						maxlength: "Не более 50 символов"
					},
					wholesale_price: {
						number: 'Должно быть числом!',
						maxlength: "Не более 50 символов"
					},
                    purshase_price: {
					   number: 'Должно быть числом!',
					   maxlength: "Не более 50 символов"
					},
					meta_info: {
					    maxlength: "Не более 500 символов"
					},
					caption: {
						required: "Пожалуйста введите заголовок",
						maxlength: "Не более 100 символов"
					}
				},
                errorClass: "alert-danger",
				highlight: function ( element, errorClass, validClass ) {
					$( element ).parents( ".form-group" ).addClass( "has-error" ).removeClass( "has-success" );
					$( element ).next( "label" ).addClass( "glyphicon-remove" ).removeClass( "glyphicon-ok" );
				},
				unhighlight: function ( element, errorClass, validClass ) {
					$( element ).parents( ".form-group" ).addClass( "has-success" ).removeClass( "has-error" );
					$( element ).next( "span" ).addClass( "glyphicon-ok" ).removeClass( "glyphicon-remove" );
				}
			} );
});

