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
                $('#transceiverSearch').fadeOut();
                $('#resetTransceivers').fadeOut();
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

function recordAction(deviceID) {
    $.mobile.loadingMessage = 'Aim remote at transceiver and press the button you want to record!';
    $.mobile.showPageLoadingMsg();

    // Get new commands's name (check that it isn't missing)
    var actionName = $('#recordActionName').val();
    if (actionName == '') {
        $.mobile.hidePageLoadingMsg();
        alert('Please enter a name for the action.')
    } else {
        // POST request with the deviceID, the command's name
        $.ajax({
            url: '/ir/recordAction/',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify([deviceID, actionName]),
            dataType: 'text',
            success: function(result) {
                $.mobile.hidePageLoadingMsg();
                location.reload(true);
            }
        });
    }
}

function runAction(url) {
    $.ajax({
        url : url,
    });
}
