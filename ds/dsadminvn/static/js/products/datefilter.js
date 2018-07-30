$(function() {

  $('#date_with').daterangepicker({
      autoUpdateInput: false,
      singleDatePicker: true,
      locale: {
          cancelLabel: 'Clear'
      }
  });

  $('#date_with').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('YYYY-MM-DD'));
  });

  $('#date_with').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });

});

$(function() {

  $('#date_by').daterangepicker({
      autoUpdateInput: false,
      singleDatePicker: true,
      locale: {
          cancelLabel: 'Clear'
      }
  });

  $('#date_by').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('YYYY-MM-DD'));
  });

  $('#date_by').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });

});