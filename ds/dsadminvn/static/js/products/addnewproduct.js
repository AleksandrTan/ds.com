/*
* Identifier for debug mode(if true - form submited on server)
* */
var is_validate_js = true;
$.validator.setDefaults( {
			submitHandler: function () {
			    if (is_validate_js){
			    	$( "#add_new_product" ).submit();
                }
     		}
		} );
$(document).ready(function () {
//Change sizes for select maincategory
    $('#maincategory' ).change(function () {
    	$.get(
              "/adminnv/sizetable/ajax/getsizes/"+$(this).val()+"/",
              onAjaxSuccess
            );
    	var parentElementTable = $('#height_size_id');
        function onAjaxSuccess(data)
        {
            if (data.length == 0){
                parentElementTable.empty();
                var trElem = '<tr><td style="color: red;">Нет размеров для отображения!</td></tr>';
                parentElementTable.append(trElem);
            }
            else {
                parentElementTable.empty();
                var optionsElement = '';

                for(var i = 0; i <= data.length - 1; i++){
                    optionsElement = optionsElement + '<option name="'+data[i].height+'" value="'+data[i].height+'">'+data[i].height+'</option>';
                }

                var new_size = '<tr><td><div class="form-group"><select class="form-control" name="height[]">'+optionsElement+'</select></div></td><td><div class="form-group">' +
                    '<input class="form-control" placeholder="Колличество" name="count_height[]" value="1"></div></td><td><div class="form-group">'+
                    '<button type="button" class="btn btn-sm btn-danger form-control" data-deletes="delete_size">Удалить Размер</button></div></td></tr>';

                parentElementTable.append(new_size);
            }
        }
    });
//Add sizes fields
    $('#add_size_fields').click(function () {
        $('#height_size_id tr:last-child').clone(true).appendTo($('#height_size_id'));
    });
//Remove size field
    $('#height_size_id').on('click', '[data-deletes=delete_size]', function () {
        if ($('#height_size_id').children('tr').length == 1){
            return false;
        }
        $(this).parents('tr').remove();
    });

//Check isset articul
$('#articul').blur(function () {
   $.get(
        "/adminnv/products/checkarticul/"+$(this).val()+"/",
        onAjaxSuccess
   );
   function onAjaxSuccess(data) {
       if(data.status){
           $('#isset_articul').modal();
       }
   };
});

//Validations form

    $( "#add_new_product" ).validate( {
				rules: {
					articul: {
						required: true,
						maxlength: 30
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
						maxlength: "Не более 30 символов"
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
