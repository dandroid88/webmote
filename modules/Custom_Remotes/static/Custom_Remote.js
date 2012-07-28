function remoteButton(id) {
    if ($('#edit_remote_slider').find("option:selected").val() == 'on') {
        window.location = '/button/' + id + '/';
    } else {
        $.ajax({
            url: '/run_button/' + id + '/',
            type: 'GET',
        });
    }
}

$('#edit_remote_slider').change(function() {
    if ($(this).find("option:selected").val() == 'off') {
        $('.new_button').css('visibility', 'hidden');
    } else {
        $('.new_button').css('visibility', 'visible');
    }
});
