window.todolists = {};
window.todolists.initialize = function () {
    $('input[name="text"]').on('keypress', function() {
        $('.has-error').hide();
    });

    if ($('.has-error').is(':visible')){
        $('input[name="text"]').val('');
    }

    $('input[name="text"]').focus();
    $('input[name="text"]').select();
}
