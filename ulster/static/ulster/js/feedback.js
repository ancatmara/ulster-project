$(document).on('submit', '.form', function(e) {
     $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: $(this).serialize(),
        success: function(html) {
        $(".form").clearForm();
        bootbox.alert({
          message: "<div class='alert'> Thank you!</div>", 
          backdrop: true
        });
        }
    });
    e.preventDefault();
});