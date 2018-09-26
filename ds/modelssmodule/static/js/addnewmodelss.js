/*
* Identifier for debug mode(if true - form submited on server)
* */
var product_data={1111:{articul:1111, barcode:00001}, 2222:{articul:2222, barcode:00001}};
var flag_checked = 0;

$(document).on('click', '[data-check-product]', function(event) {
               var sub = new ValidateProduct(event, $(this).closest("tr"));
                   sub.init();
           });

function ValidateProduct(e, obj) {
    this.e = e;
    this.obj = obj;
    this.product_data_lists = $('#product_data_lists').val();
    this.articulobj = this.obj.find('[data-articul = "articul"]');
    this.articul = this.obj.find('[data-articul = "articul"]').val();
    this.barcodeobj = this.obj.find('[data-pre-barcode = "pre-barcode"]');
    this.barcode = this.obj.find('[data-pre-barcode = "pre-barcode"]').val();
    this.height = this.obj.find('[data-height="height"]').val();
    this.count = this.obj.find('[data-count="count"]').val();
    this.modal_alarm = $('#modal_alarm');
    this.alarm_text = $('#modal_content');
    this.add_product_button = $('#add_product_fields');
    this.count_sizes = $('#count_sizes').val();
    this.count_sizes_add = $('#count_sizes_add').val();

    this.init = function () {
        // if (this.checkFilledData()){
        //     this.validate();
        // }
        flag_checked = 0;
        this.validate();
    };

    this.validate = function () {
        //this.checkArticul();
        this.checkBarcode();
    };

    this.checkFilledData = function () {
        if (this.articul != '' && this.barcode != '' && this.height != '' && this.count != ''){
            return true;
        }
        else {
            this.alarm_text.text('Введите все данные товара!!!');
            this.modal_alarm.modal();
            return false;
        }
    };

    this.checkArticul = function () {
        this.checkIssetArticulPrew();
        this.checkIssetArticulDB();
    };

    this.checkIssetArticulPrew = function () {
        if (this.articul in product_data) {
            this.articulobj.val('');
            this.alarm_text.text('').text('Введенный артикул уже существует!Выберите другой');
            this.modal_alarm.modal().modal();
            flag_checked = 1;
            return false;
        }
        else {
            return true;
        }
    };

    this.checkIssetArticulDB = function () {
        if (flag_checked == 1){
            return false;
        }
        thet = this;
        $.get(
        "/adminnv/products/checkarticul/"+this.articul+"/",
        onAjaxSuccesss
        );
        function onAjaxSuccesss(data) {
            if(data.status){
                thet.articulobj.val('');
                thet.alarm_text.text('').text('Введенный артикул уже существует!Выберите другой');
                thet.modal_alarm.modal().modal();
                flag_checked = 1;
                return false;
            }
            else {
                return true;
            }
        }

    }.bind(this);

    this.checkBarcode = function () {
        this.checkIssetBarcodePrew();
    };

    this.checkIssetBarcodePrew = function () {
        if (this.barcode == product_data[this.articul].barcode) {
            this.barcodeobj.val('');
            this.alarm_text.text('').text('Введенный штрихкод уже существует!Выберите другой');
            this.modal_alarm.modal().modal();
            flag_checked = 1;
            return false;
        }
        else {
            return true;
        }
    };

    this.checkIssetBarcodeDB = function () {

    };

    this.checkHeight = function () {

    };

    this.checkCount = function () {

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
