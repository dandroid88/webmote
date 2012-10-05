function remoteButton(buttonID, actionID) {
    if ($('#edit_remote_slider').find("option:selected").val() == 'on') {
        window.location = '/button/' + buttonID + '/';
    } else {
        $.ajax({
            url: '/runAction/' + actionID + '/',
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

function saveNewButton() {
    url = '/button' + document.URL.split('button')[1];
    $.mobile.loadingMessage = 'Saving Button';
    $.mobile.showPageLoadingMsg();

    var data = [$('#id_action').find("option:selected").val(), 
                $('#id_name').val(),
                $('#id_icon').find("option:selected").val()];
    
    // Post this data to backend
    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        dataType: 'text',
        success: function(result) {
            $.mobile.hidePageLoadingMsg();
            window.location = "/remote/" + url.split('/')[2] + '/';
        }
    });
}
