/*
* Identifier for debug mode(if true - form submited on server)
* */
var product_data={};

$( "#add_new_modelss" ).submit(function (e) {
                                  // if ($('#name').val() == '' || $('#caption').val() == ''){
			                       //   $('#modal_content').text('Введите название или заголовок модели!!!');
                                  //    $('#modal_alarm').modal();
                                  //    return false;
                                  // }

			                      this.submit();
                            });

$(document).on('click', '[data-check-product]', function(event) {
               // $('#hellopreloader_preload').css({'display':'block', 'opacity': '0.5'});
               var sub = new ValidateProduct(event, $(this).closest("tr"), $(this));
               sub.init();
           });

function ValidateProduct(e, obj, but) {
    this.e = e;
    this.obj = obj;
    this.product_data_lists = $('#product_data_lists');
    this.articulobj = this.obj.find('[data-articul = "articul"]');
    this.articul = this.obj.find('[data-articul = "articul"]').val();
    this.barcodeobj = this.obj.find('[data-pre-barcode = "pre-barcode"]');
    this.barcode = this.obj.find('[data-pre-barcode = "pre-barcode"]').val();
    this.heightobj = this.obj.find('[data-height="height"]');
    this.height = this.obj.find('[data-height="height"]').val();
    this.count = this.obj.find('[data-count="count"]').val();
    this.data_deletes = this.obj.find('[data-deletes="delete_size"]');
    this.modal_alarm = $('#modal_alarm');
    this.alarm_text = $('#modal_content');
    this.add_product_button = $('#add_product_fields');
    this.count_sizes = $('#count_sizes').val();
    this.count_sizes_add = $('#count_sizes_add').val();

    this.init = function () {
        $('#flag_checked').val(0);
        if (this.checkFilledData()){
            this.validate();
            if($('#flag_checked').val() == 1){
                // $('#hellopreloader_preload').css({'display':'none'});
                return false;
            }
        }
        else {
            return false;
        }
        if (this.count_sizes > this.count_sizes_add && $('#flag_checked').val() == 0){
            this.add_product_button.show();
            but.removeClass('btn-primary').addClass('btn-success');
            but.text('Проверено');
            but.removeAttr("data-check-product");
        }
        if (this.count_sizes == this.count_sizes_add && $('#flag_checked').val() == 0){
            but.removeClass('btn-primary').addClass('btn-success');
            but.text('Проверено');
            but.removeAttr("data-check-product");
        }
       
        //add data product in object list(validation clear)
        if ($('#flag_checked').val() == 0){
            this.addDataProduct();
            this.product_data_lists.val(JSON.stringify(product_data));
            this.data_deletes.attr('data-is-delpr', this.articul);
            $('#save_product').show();
            // $('#hellopreloader_preload').css({'display':'none'});
            console.log(JSON.stringify(product_data));
        }
    };

    this.validate = function () {
        this.checkArticul();
        this.checkBarcode();
        this.checkHeight();
        this.checkCount();
    };

    this.checkFilledData = function () {
        if (this.articul != '' && this.barcode != '' && this.height != '' && this.count != ''){
            return true;
        }
        else {
            this.alarm_text.text('Введите все данные товара!!!');
            this.modal_alarm.modal();
            $('#flag_checked').val(1);
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
            $('#flag_checked').val(1);
            return false;
        }
        else {
            return true;
        }
    };

    this.checkIssetArticulDB = function () {
        if ($('#flag_checked').val() == 1){
            return false;
        }
        thet = this;
        $.ajax({
                url: "/adminnv/products/checkarticul/"+this.articul+"/",
                success: onAjaxSuccesss,
                async: false
            });
        function onAjaxSuccesss(data) {
            if(data.status){
                thet.articulobj.val('');
                thet.alarm_text.text('').text('Введенный артикул уже существует!Выберите другой');
                thet.modal_alarm.modal().modal();
                $('#flag_checked').val(1);
                return false;
            }
            else {
                return true;
            }
        }

    }.bind(this);

    this.checkBarcode = function () {
        if ($('#flag_checked').val() == 1){
            return false;
        }
        this.checkIssetBarcodePrew();
        this.checkIssetBarcodeDB();
    };

    this.checkIssetBarcodePrew = function () {
        for (key in product_data){
            if (this.barcode == product_data[key].barcode) {
                this.barcodeobj.val('');
                this.alarm_text.text('').text('Введенный штрихкод уже существует!Выберите другой');
                this.modal_alarm.modal().modal();
                $('#flag_checked').val(1);
                return false;
            }
            else {
                 continue;
            }
        }
    };

    this.checkIssetBarcodeDB = function () {
        thet = this;
        if ($('#flag_checked').val() == 1){
            return false;
        }
        if (thet.barcode.length != 5){
            thet.barcodeobj.val('');
            thet.alarm_text.text('').text('Штрих-код - 5 цифр!!!!');
            thet.modal_alarm.modal().modal();
            $('#flag_checked').val(1);
            return false;
        }
        $.ajax({
            url:"/adminnv/products/checkprebarcode/"+this.barcode+"/",
            success: onAjaxSuccesss,
             async: false
            }
        );
        function onAjaxSuccesss(data) {
            if(data.status){
                thet.barcodeobj.val('');
                thet.alarm_text.text('').text('Введенный штрих-код уже существует!Выберите другой');
                thet.modal_alarm.modal().modal();
                $('#flag_checked').val(1);
                return false;
            }
            else {
                return true;
            }
        }
    };

    this.checkHeight = function () {
        if ($('#flag_checked').val() == 1){
            return false;
        }
        for (key in product_data){
            if (this.height == product_data[key].height) {
                this.heightobj.val('');
                this.alarm_text.text('').text('Внимание дублирование размера!!! Выберите другой размер!!!');
                this.modal_alarm.modal().modal();
                $('#flag_checked').val(1);
                return false;
            }
            else {
                 continue;
            }
        }
    };

    this.checkCount = function () {
        if ($('#flag_checked').val() == 1){
            return false;
        }
        if(this.count == '' || parseInt(this.count) < 0 ){
            this.alarm_text.text('').text('Введите правильное колличество товара!');
            this.modal_alarm.modal().modal();
            $('#flag_checked').val(1);
            return false;
        }
        else {
            return true;
        }
    };

    this.addDataProduct = function () {
        product_data[this.articul] = {};
        product_data[this.articul].articul = this.articul;
        product_data[this.articul].barcode = this.barcode;
        product_data[this.articul].height = this.height;
        product_data[this.articul].count = this.count;
    }
}
$(document).ready(function () {

//Changes maincategory
    $('#maincategory' ).change(function () {
    	$('#height_size_id').empty();
        product_data = {};
        $('#product_data_lists').val('');
        $('#count_sizes_add').val('0');
        $('#add_product_fields').show();
        console.log(product_data);
    });

//Add product fields
    $('#add_product_fields').click(function () {
        if ($('#count_sizes').val() <=  $('#count_sizes_add').val()){
    	    return false;
        }
        var maincategory_id = $('#maincategory' ).val();
        var parentElementTable = $('#height_size_id');
        $.get(
              "/adminnv/sizetable/ajax/getsizes/"+maincategory_id+"/",
              onAjaxSuccess
            );
        function onAjaxSuccess(data)
        {
            if (data.length == 0){
                var trElem = '<tr><td style="color: red;">Нет размеров для отображения!</td></tr>';
                $('#save_product').hide();
                parentElementTable.append(trElem);
            }
            else {
                var optionsElement = '';

                for(var i = 0; i <= data.length - 1; i++){
                    optionsElement = optionsElement + '<option name="'+data[i].height+'" value="'+data[i].height+'">'+data[i].height+'</option>';
                }

                var new_size = '<tr><td><input class="form-control" placeholder="Артикул" name="articul[]" type="text" value="" data-articul="articul"' +
                    ' maxlength="6" required></td><td><input class="form-control" placeholder="Штрих-код" name="pre_barcode[]" type="number" value="" ' +
                    'data-pre-barcode="pre-barcode" maxlength="5" required ></td><td><div class="form-group"><select class="form-control" name="height[]"' +
                    ' data-height="height" required><option name="" value=""></option>'+optionsElement+'</select></div></td><td style="width: 15%">' +
                    '<div class="form-group"><input class="form-control"' +
                    'name="count[]" value="" maxlength="5" type="number" data-count="count" required></div></td><td><div class="form-group">' +
                    '<button type="button" class="btn btn-sm btn-primary form-control" data-check-product="1">Проверить</button></div></td>' +
                    '<td><div class="form-group"><button type="button" class="btn btn-sm btn-danger form-control" data-deletes="delete_size">' +
                    'Удалить</button></div></td></tr>';

                parentElementTable.append(new_size);
                $('#save_product').hide();
                $('#add_product_fields').hide();
                $('#count_sizes').val(data.length);
            }
        }
    	$('#count_sizes_add').val(parseInt($('#count_sizes_add').val()) + 1);

    });

//Remove product field
    $('#height_size_id').on('click', '[data-deletes=delete_size]', function () {
        delete product_data[$(this).attr('data-is-delpr')];
        $('#product_data_lists').val(JSON.stringify(product_data));
        $(this).parents('tr').remove();
        console.log(product_data);
        $('#count_sizes_add').val(parseInt($('#count_sizes_add').val()) - 1);
        if ($('#count_sizes').val() <=  $('#count_sizes_add').val()){
    	    return false;
        }
        $('#add_product_fields').show();
        if ($('#count_sizes').val()>=  $('#count_sizes_add').val()){
            $('#save_product').show();
        }
    });

//Check isset modelss
$('#name').blur(function () {
    if ($(this).val() != ''){
       $.get(
        "/adminnv/products/checkmodelss/"+$(this).val()+"/",
        onAjaxSuccess
       );
       function onAjaxSuccess(data) {
           if(data.status){
           	   $('#name').val('');
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
});
