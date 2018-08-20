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

    this.addRowProduct = function (data_product) {
        alert(data_product.articul);
        this.preloader.css({'display':'none', 'opacity': '0.5'});
    }
    
    this.deleteRowProduct = function () {
        
    }
}
