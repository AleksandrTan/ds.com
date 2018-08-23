$(document).ready(function () {
    $('#barcode_articul').focus();
})

$( "#found_product" ).submit(function (e) {
    barcodeGet = new FoundBarcode(e);
    barcodeGet.init();
});

$( "#found_product" ).on('input', function (e) {
    if ($('#barcode_articul').val().length == 13){
        $(this).submit();
    }
});

//Add new product
function FoundBarcode(e){
    this.e = e;
    this.barcode = $('#barcode_articul').val();
    this.barcode_articul = $('#barcode_articul');
    this.preloader = $('#hellopreloader_preload');
    this.alertinfo = $('#alert_info');
    this.alertinfotext = $('#text_alert');
    this.parenttable = $('#products_list');
    this.totalForms = $('#id_form-TOTAL_FORMS');
    this.maxForms = $('#id_form-MAX_NUM_FORMS');
    this.minForms = $('#id_form-MIN_NUM_FORMS');
    this.buttonCancellCeil = $('#cancel_ceil');
    this.total_amount_all = $('#total_amount_all');


    this.init = function () {
        e.preventDefault();
        this.preloader.css({'display':'block', 'opacity': '0.5'});
        this.getProduct();
    };

    this.getProduct = function () {
        thet = this;
        $.get(
        "/adminnv/products/barcode/getproduct/"+this.barcode+"/",
        onAjaxSuccess
       );
       function onAjaxSuccess(data) {
           if(data.status){
               thet.addRowProduct(data.data_product);
           }
           else {
               thet.alertinfotext.text('');
               thet.preloader.css({'display':'none', 'opacity': '0.5'});
               thet.alertinfotext.text('Произошла ошибка, либо товар не найден попробуйте еще раз!!!');
               thet.alertinfo.modal();
           }
       }
    };

    this.addRowProduct = function (product_data) {
        var count_tr = this.hasChildElements();
        var new_product = '<tr id="add_ptr-'+count_tr+'"><td class="text-center"><input type="hidden" ' +
            'id="id_form-'+count_tr+'-products" name="form-'+count_tr+'-products" value="'+product_data.id+'"/>' +
            '<input type="hidden" name="start_price" id="start_price'+count_tr+'" value="'+product_data.price+'"/>' +
            '<input type="hidden" name="price" id="price'+count_tr+'" value="'+product_data.price+'"/>'+product_data.articul+'</td>' +
            '<td class="text-center">'+product_data.category+'</td><td class="text-center">'+product_data.name+'</td>' +
            '<td class="text-center" id="price_table'+count_tr+'">'+product_data.price+'</td><td class="text-center">'+product_data.discount+'%</td>' +
            '<td class="text-center" id="price_discount-'+count_tr+'">'+product_data.price_discount+'</td>' +
            '<td><input id="id_form-'+count_tr+'-lost_num" name="form-'+count_tr+'-lost_num" type="number"></td><td class="text-center">'+product_data.size+'</td>' +
            '<td class="text-center" id="in_stock'+count_tr+'">'+product_data.count_num+'</td><td class="text-center">1</td><td>' +
            '<textarea name="description"  rows="5"></textarea></td><td>' +
            '<button type="button" class="btn btn-sm btn-danger form-control" data-delete-product="delete-product" ' +
            'data-count-id="'+count_tr+'">Отмена</button></td></tr>';
        this.parenttable.append(new_product);
        //change count forms
        this.totalForms.val(parseInt(this.totalForms.val()) + 1);
        this.barcode_articul.val('').focus();
        //calculate total sum
        this.calculationOfAmount(product_data.price_discount);
        //show button submit and total sum
        if (this.hasChildElements() == 1){
            this.buttonCancellCeil.show();
        }
        this.preloader.css({'display':'none', 'opacity': '0.5'});
    };

    this.hasChildElements = function() {
        return this.parenttable.find('tr').length;
    };
    
    this.calculationOfAmount = function (price_discount) {
        this.total_amount_all.text(parseInt(this.total_amount_all.text()) + price_discount);
        return true;
    }
}

//Delete product
$('#products_list').on('click', '[data-delete-product=delete-product]', function (e) {
    var deleteProduct = new DeleteProduct(e, $(this));
    deleteProduct.init();
});

function DeleteProduct(e, obj){
    this.e = e;
    this.obj = obj;
    this.barcode = $('#barcode_articul').val();
    this.barcode_articul = $('#barcode_articul');
    this.preloader = $('#hellopreloader_preload');
    this.alertinfo = $('#alert_info');
    this.alertinfotext = $('#text_alert');
    this.parenttable = $('#products_list');
    this.totalForms = $('#id_form-TOTAL_FORMS');
    this.maxForms = $('#id_form-MAX_NUM_FORMS');
    this.minForms = $('#id_form-MIN_NUM_FORMS');
    this.buttonCancellCeil = $('#cancel_ceil');
    this.total_amount_all = $('#total_amount_all');

    this.init = function () {
        e.preventDefault();
        this.preloader.css({'display':'block', 'opacity': '0.5'});
        this.deleteProduct();
    };

    this.deleteProduct = function () {
        var identificator = this.obj.attr('data-count-id');
         this.calculationOfAmount(identificator);
        $('#add_ptr-'+identificator).remove();
        this.totalForms.val(parseInt(this.totalForms.val()) - 1);
        if (this.hasChildElements() == 0){
                this.buttonCancellCeil.hide();
            }
        this.preloader.css({'display':'none', 'opacity': '0.5'});
    };

    this.hasChildElements = function() {
        return this.parenttable.find('tr').length;
    };

    this.calculationOfAmount = function (identificator) {
        this.total_amount_all.text(parseInt(this.total_amount_all.text()) - parseInt($('#price_discount-'+identificator).text()));
        return true;
    }
}
