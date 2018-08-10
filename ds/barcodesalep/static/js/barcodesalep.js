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
               thet.preloader.css({'display':'none', 'opacity': '0.5'});
           	   alert(2000);
           }
           else {
               thet.preloader.css({'display':'none', 'opacity': '0.5'});
               alert(1000);
           }
       }
    }
}
