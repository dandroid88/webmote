function searchForTransceiver() {
    $('#addTransceiverForm').fadeOut();
    $.mobile.loadingMessage = 'Searching for a new transciever!';
    $.mobile.showPageLoadingMsg();
    //First make a request to read in all serial commands and look for ID_REQUEST
    url = '/transceiverSearch/' + $('#typeTitle').text().split(" ")[0] + '/' + $('#portInput').val();
    $.ajax({
        url: url,
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
                $('#id_type').val(type);
                $('#id_type').attr('readonly', true);
                $('#transceiverSearch').fadeOut();
                $('#resetTransceivers').fadeOut();
                $('#id_usbPort').val($('#portInput').val());
                $('#addTransceiverForm').fadeIn();
            } else {
                $.mobile.hidePageLoadingMsg();
                alert('No transceiver found!');
            }
        },
        error: function(returned) {
            $.mobile.hidePageLoadingMsg();
            alert('No transceiver found!');
        }
    });
}

