/*
* Identifier for debug mode(if true - form submited on server)
* */
$(document).on('click', '[data-check-product]', function(event) {
               var sub = new ValidateProduct(event, $(this).closest("tr"));
                   sub.validate();
           });

function ValidateProduct(e, obj) {
    this.e = e;
    this.obj = obj;
    this.product_data_lists = $('#product_data_lists').val();
    this.articul = this.obj.find('[data-articul = "articul"]').val();
    this.barcode = this.obj.find('[data-pre-barcode = "pre-barcode"]').val();
    this.height = this.obj.find('[data-height="height"]').val();
    this.count= this.obj.find('[data-count="count"]').val();

    this.validate = function () {
        console.log(this.articul);
    }
}
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
                $('#save_product').hide();
                parentElementTable.append(trElem);
            }
            else {
                parentElementTable.empty();
                var optionsElement = '';

                for(var i = 0; i <= data.length - 1; i++){
                    optionsElement = optionsElement + '<option name="'+data[i].height+'" value="'+data[i].height+'">'+data[i].height+'</option>';
                }

                var new_size = '<tr><td><input class="form-control" placeholder="Артикул" name="articul[]" type="text" value="" maxlength="6" required></td><td>' +
                    '<input class="form-control" placeholder="Штрих-код" name="pre_barcode[]" type="number" value="" maxlength="5" required >' +
                    '</td><td><div class="form-group"><select class="form-control" name="size">'+optionsElement+'</select></div></td><td><div class="form-group">' +
                    '<input class="form-control" placeholder="Колличество" name="count_num" value="0"></div></td><td><div class="form-group">' +
                    '<button type="button" class="btn btn-sm btn-danger form-control" data-deletes="delete_size">Удалить</button></div></td></tr>';

                parentElementTable.append(new_size);
                $('#count_sizes').val(data.length);
                $('#count_sizes_add').val(1);
                $('#save_product').show();
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

//Check isset pre_barcode
$('#pre_barcode').blur(function () {
    if ($(this).val().length < 5){
        alert('Введите 5 чисел');
        return false;
    }
    if ($(this).val() != ''){
       $.get(
        "/adminnv/products/checkprebarcode/"+$(this).val()+"/",
        onAjaxSuccess
       );
       function onAjaxSuccess(data) {
           if(data.status){
           	   $('#pre_barcode').val('');
               $('#modal_content').text('').text('Введенный штрих-код уже существует!Выберите другой');
               $('#modal_alarm').modal();
           }
       }
   }

});

// //Check isset modelss
// $('#modelss').blur(function () {
//     if ($(this).val() != ''){
//        $.get(
//         "/adminnv/products/checkmodelss/"+$(this).val()+"/",
//         onAjaxSuccess
//        );
//        function onAjaxSuccess(data) {
//            if(data.status){
//            	   $('#modelss').val('');
//                $('#modal_content').text('').text('Введенная модель уже существует!Выберите другую');
//                $('#modal_alarm').modal();
//            }
//        }
//    }
//
// });

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
});
