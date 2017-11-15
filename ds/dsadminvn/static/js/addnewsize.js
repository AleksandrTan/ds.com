/*
* Identifier for debug mode(if true - form submited on server)
* */
var is_validate_js = true;
$.validator.setDefaults( {
			submitHandler: function () {
			    if (is_validate_js){
			    	$('#hellopreloader_preload').css({'display':'block', 'opacity': '0.5'});
                    $( "#add_new_s" ).submit();
                }
     		}
		} );
$(document).ready(function () {
//Show/hide help block for input tags
    $('input').on('click', function () {
        $(this).parent().parent().next().show()
    });

    $('input').blur(function(){
        $(this).parent().parent().next().hide()
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
//Show count entered simbols for textarea tag
    $("textarea").keyup(function() {
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

//Show count entered simbols for fotos block
    $('#fotos_div').mousemove(function(){
      $('#fotos_info').show();
    });

    $('#fotos_div').mouseleave(function(){
      $('#fotos_info').hide();
    });

//Validations form

    $( "#add_new_s" ).validate( {
				rules: {
					autor: {
						required: true,
						maxlength: 30
					},
					caption: {
						required: true,
						maxlength: 50
					},
					description: {
						required: true,
						maxlength: 1000
					},
					full_adress: {
					    required: false,
						maxlength: 100
					},
					meta_info: {
					    required: false,
						maxlength: 500
					},

				},
				messages: {
					autor: {
						required: "Пожалуйста введите автора",
						maxlength: "Не более 30 символов"
					},
					caption: {
						required: "Пожалуйста введите заголовок",
						maxlength: "Не более 50 символов"
					},
					description: {
						required: "Пожалуйста введите описание",
						maxlength: "Не более 1000 символов"
					},
                    full_adress: {
					   maxlength: "Не более 100 символов"
					},
					meta_info: {
					    maxlength: "Не более 500 символов"
					},
				},
				errorElement: "em",
				errorPlacement: function ( error, element ) {
					// Add the `help-block` class to the error element
					error.addClass( "help-block" );

					// Add `has-feedback` class to the parent div.form-group
					// in order to add icons to inputs
					element.parents( ".form-control-wrap" ).addClass( "has-feedback" );

					if ( element.prop( "type" ) === "checkbox" ) {
						error.insertBefore( element.parent( "label" ) );
					} else {
						error.insertBefore( element );
					}

					// Add the span element, if doesn't exists, and apply the icon classes to it.
					if ( !element.next( "span" )[ 0 ] ) {
						$( "<span class='glyphicon glyphicon-remove form-control-feedback'></span>" ).insertBefore( element );
					}
				},
				success: function ( label, element ) {
					// Add the span element, if doesn't exists, and apply the icon classes to it.
					if ( !$( element ).next( "span" )[ 0 ] ) {
						$( "<span class='glyphicon glyphicon-ok form-control-feedback'></span>" ).insertBefore( $( element ) );
					}
				},
				highlight: function ( element, errorClass, validClass ) {
					$( element ).parents( ".form-control-wrap" ).addClass( "has-error" ).removeClass( "has-success" );
					$( element ).next( "span" ).addClass( "glyphicon-remove" ).removeClass( "glyphicon-ok" );
				},
				unhighlight: function ( element, errorClass, validClass ) {
					$( element ).parents( ".form-control-wrap" ).addClass( "has-success" ).removeClass( "has-error" );
					$( element ).next( "span" ).addClass( "glyphicon-ok" ).removeClass( "glyphicon-remove" );
				}
			} );
})
