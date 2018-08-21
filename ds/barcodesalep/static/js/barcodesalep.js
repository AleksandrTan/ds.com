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

function FoundBarcode(e){
    this.e = e;
    this.barcode = $('#barcode_articul').val();
    this.preloader = $('#hellopreloader_preload');
    this.alertinfo = $('#alert_info');
    this.alertinfotext = $('#text_alert');
    this.parenttable = $('#products_list');
    this.totalForms = $('#id_form-TOTAL_FORMS');
    this.maxForms = $('#id_form-MAX_NUM_FORMS');
    this.minForms = $('#id_form-MIN_NUM_FORMS');


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
        new_product = '<tr><td class="text-center"><input type="hidden" name="products" value="'+product_data.id+'"/>' +
            '<input type="hidden" name="start_price" id="start_price" value="'+product_data.price+'"/>' +
            '<input type="hidden" name="price" id="price" value="'+product_data.price+'"/>'+product_data.articul+'</td>' +
            '<td class="text-center">'+product_data.category+'</td><td class="text-center">'+product_data.name+'</td>' +
            '<td class="text-center" id="price_table">'+product_data.price+'</td><td class="text-center">' +
            '<input name="lost_num" type="number" id="lost_num" value="0"></td><td class="text-center">'+product_data.size+'</td>' +
            '<td class="text-center" id="in_stock">'+product_data.count_num+'</td><td class="text-center">1</td><td>' +
            '<textarea name="description"  rows="5"></textarea></td><td>' +
            '<a type="button" class="btn btn-sm btn-primary form-control" id="save_exit" href="">Отмена</a></td></tr>';
        this.parenttable.append(new_product);
        this.preloader.css({'display':'none', 'opacity': '0.5'});
    };
    
    this.deleteRowProduct = function () {
        
    };
}
