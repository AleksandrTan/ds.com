/*
* Identifier for debug mode(if true - form submited on server)
* */
var is_validate_js = true;

$(document).ready(function () {

//Check isset articul
$('#articul').blur(function () {
   if ($(this).val() != ''){
       $.get(
        "/adminnv/products/checkarticul/"+$(this).val()+"/",
        onAjaxSuccess
       );
       function onAjaxSuccess(data) {
           if(!data.status){
           	   $('#articul').val('');
               $('#modal_content').text('').text('Такого артикула не существует!Выберите другой');
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
           if(!data.status){
           	   $('#modelss').val('');
               $('#modal_content').text('').text('Такой модели не существует!Выберите другую');
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

    $( "#filter_disco" ).validate( {
				rules: {
					disco_value: {
						required: true,
						maxlength: 6,
						number: true,
                        min: 0
					}
				},
				messages: {
					disco_value: {
						required: "Пожалуйста введите скидку",
						maxlength: "Не более 6 символов",
                        number: 'Должно быть числом!',
                        min: 'Блять больше 0!!!!'
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


    $( "#articul_disco" ).validate( {
				rules: {
					art_disco: {
						required: true,
						maxlength: 6,
						number: true,
                        min: 0
					},
                    articul:{
					    required: true
                    }
				},
				messages: {
					art_disco: {
						required: "Пожалуйста введите скидку",
						maxlength: "Не более 6 символов",
                        number: 'Должно быть числом!',
                        min: 'Блять больше 0!!!!'
					},
                    articul: {
					    required: "Пожалуйста введите Артикул",
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


    $( "#model_disco" ).validate( {
				rules: {
					mod_disco: {
                        required: true,
                        maxlength: 6,
                        number: true,
                        min: 0
                    },
                    modelss:{
					    required: true
                    }

				},
				messages: {
					mod_disco: {
						required: "Пожалуйста введите скидку",
						maxlength: "Не более 6 символов",
                        number: 'Должно быть числом!',
                        min: 'Блять больше 0!!!!'
					},
                    modelss:{
					    required: "Пожалуйста введите Модель",
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

