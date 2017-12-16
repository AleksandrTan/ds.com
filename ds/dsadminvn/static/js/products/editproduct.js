/**
 * Created by user on 04.12.2017.
 */

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
        if ($('#count_sizes').val() <=  $('#count_sizes_add').val()){
    	    return false;
        }
        $('#height_size_id tr:last-child').clone(true).appendTo($('#height_size_id'));
    	$('#count_sizes_add').val(parseInt($('#count_sizes_add').val()) + 1);

    });
//Remove size field
    $('#height_size_id').on('click', '[data-deletes=delete_size]', function () {
        if ($('#height_size_id').children('tr').length == 1){
            return false;
        }
        $(this).parents('tr').remove();
        $('#count_sizes_add').val(parseInt($('#count_sizes_add').val()) - 1);
    });

//Check isset articul
$('#articul').blur(function () {
   if ($(this).val() != ''){
       if ($(this).val() == $('#articul_product_hidden').val()){
           return false;
       }
       else {
            $.get(
                "/adminnv/products/checkarticul/"+$(this).val()+"/",
                onAjaxSuccess
           );
           function onAjaxSuccess(data) {
               if(data.status){
                   $('#modal_content').text('').text('Введенный артикул уже существует!Выберите другой');
                   $('#modal_alarm').modal();
               }
           };
       };
   };
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
					},

				},
				messages: {
					articul: {
						required: "Пожалуйста введите артикул",
						maxlength: "Не более 30 символов"
					},
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

