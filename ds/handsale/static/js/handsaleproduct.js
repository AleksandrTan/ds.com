$(document).ready(function () {
    if ($('#price').val() == 0){
        $('#not_price').text('Внимание!!!Для этого товара не указана цена!!!').show();
        $('#sell_product_div').hide();
    }

// //Set count num in stock
//     $('#size' ).change(function () {
//     	$('#in_stock').text(sizecount[$(this).val()]);
//     	$('#count_num').val('');
//     	if (sizecount[$(this).val()] == 0){
//     	    $('#count_num').hide();
//     	    $('#sale_but').hide();
//         }
//         else {
//     	    $('#count_num').show();
//     	    $('#sale_but').show();
//         }
//     });
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
    	var price_discount_hidden = $('#price_discount_hidden').val();

    	if (parseInt($(this).val()) < 0){
    	    alert("Должно быть БОЛЬШЕ 0!!!!!");
    	    $(this).val('');
    	    return false;
        }

    	if (parseInt($('#discount').text()) > 0){
            $('#price_discount').text(price_discount_hidden - $(this).val());
		}
		else {
    		$('#price_table').text(start_price - $(this).val());
		}
    });

//Validations form
    $( "#seil_product" ).validate( {
				rules: {
					count_num: {
						required: true,
						maxlength: 30,
                        min: 0
					},
                    lost_num: {
						maxlength: 30,
                        min: 0
					}
				},
				messages: {
					count_num: {
						required: "Пожалуйста введите колличество",
						maxlength: "Не более 30 символов",
                        min: "Больше 0!!!"
					},
                    lost_num: {
						maxlength: "Не более 30 символов",
                        min: "Больше 0!!!"
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
