$(document).ready(function () {
//Set count num in stock
    $('#size' ).change(function () {
    	$('#in_stock').text(sizecount[$(this).val()]);
    	$('#count_num').val('');
    });
//Set count_num value
    $('#count_num').on('click keyup', function () {
       if (parseInt($(this).val()) > parseInt($('#in_stock').text())){
            $('#is_deleted_ctr').modal();
            $(this).val('');
        }
    });
//Set lost_num value
    $('#lost_num').on('click keyup', function () {
    	var start_price = $('#start_price').val();
        $('#price_table').text(start_price - $(this).val());
    });

//Validations form
    $( "#seil_product" ).validate( {
				rules: {
					count_num: {
						required: true,
						maxlength: 30
					},
				},
				messages: {
					count_num: {
						required: "Пожалуйста введите колличество",
						maxlength: "Не более 30 символов"
					},
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
