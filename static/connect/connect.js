$(document).ready(function() {
    $(document).on('show.bs.modal', '.modal', function () {
        $(this).appendTo('body');
      });
});