function searchForTransceiver() {
    $('#addTransceiverForm').fadeOut();
    $.mobile.loadingMessage = 'Searching for a new transciever!';
    $.mobile.showPageLoadingMsg();
    //First make a request to read in all serial commands and look for ID_REQUEST
    $.ajax({
        url: '/ir/transceiverSearch/',
        timeout : 10000,
        async: true,
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        dataType: 'text',
        success: function(returned) {
            type = $.parseJSON(returned).deviceType;
            // This if statement doesn't work for some reason
            if (type.length > 1) {
                $.mobile.hidePageLoadingMsg();
                $('input[readonly="True"]').val(type);
                $('#addTransceiverForm').fadeIn();
            } else {
                alert('returned empty');
            }
        },
        error: function(returned) {
            $.mobile.hidePageLoadingMsg();
            alert('No transceiver found!');
        }
    });
}
