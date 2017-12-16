$(document).ready(function () {
    $('#size' ).change(function () {
    	$('#in_stock').text(sizecount[$(this).val()]);
    });
})
