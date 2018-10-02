/**
 * Created by user on 01.10.2018.
 */
var is_validate_js = true;
$.validator.setDefaults( {
    submitHandler: function () {
	       		       if (is_validate_js){
			               $( "#edit_modelss" ).submit(function (e) {
			                                            $('#hellopreloader_preload').css({'display':'block', 'opacity': '0.5'});
			                                            var form = this;
                                                        form.submit();
                            });
                    }
     		 }
		} );

$(document).ready(function () {
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

    $( "#edit_modelss" ).validate( {
				rules: {
					price: {
						//required: true,
						number: true,
						maxlength: 10
					},
					wholesale_price: {
						number: true,
						maxlength: 10
					},
					purshase_price: {
					    number: true,
						maxlength: 10
					},
					meta_info: {
					    required: false,
						maxlength: 500
					},
					caption:{
						required: true,
						maxlength: 100
					},
					discount: {
						//required: true,
						number: true,
						maxlength: 10
					},
					price_down: {
						//required: true,
						number: true,
						maxlength: 10
					},
					sale_price: {
						//required: true,
						number: true,
						maxlength: 10
					}

				},
				messages: {
					price: {
						number: 'Должно быть числом!',
						maxlength: "Не более 10 символов"
					},
					wholesale_price: {
						number: 'Должно быть числом!',
						maxlength: "Не более 10 символов"
					},
                    purshase_price: {
					   number: 'Должно быть числом!',
					   maxlength: "Не более 10 символов"
					},
					meta_info: {
					    maxlength: "Не более 500 символов"
					},
					caption: {
						required: "Пожалуйста введите заголовок",
						maxlength: "Не более 100 символов"
					},
					discount: {
						number: 'Должно быть числом!',
						maxlength: "Не более 10 символов"
					},
					price_down: {
						number: 'Должно быть числом!',
						maxlength: "Не более 10 символов"
					},
					sale_price: {
						number: 'Должно быть числом!',
						maxlength: "Не более 10 символов"
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