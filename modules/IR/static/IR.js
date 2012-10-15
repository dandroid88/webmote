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

function searchLIRC(deviceID) {
    $.mobile.loadingMessage = 'Searching, may take up to a few minutes...';
    $.mobile.showPageLoadingMsg();

    $.ajax({
        url: '/ir/searchLIRC/' + deviceID + '/',
        async: true,
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        dataType: 'text',
        success: function(returned) {
            $.mobile.hidePageLoadingMsg();
            var matches = $.parseJSON(returned);
            if (matches.length) {
                var select = $('#selectRemoteModel');
                for (i = 0; i < matches.length; i++) {
                    selected = ''
                    if (!i) {
                        selected = 'selected="selected"';
                    }
                    select.append('<option value="' + matches[i] + '"' + selected + '>' + matches[i].split('/').pop() + '</option>');
                }
                select.selectmenu('refresh', true);
                $('#searchLIRC').hide();
                $('#addActions').fadeIn();
                $('#matches').fadeIn();
                if (matches.length > 1) {
                    alert('There were multiple remotes found that matched. Select the one that matches your remote control or device\'s model number.  Alternatively you may record additional commands manually which may narrow down the set of matches.');           
                }
            } else {
                $.mobile.hidePageLoadingMsg();
                alert('Unfortunately no matches were found. You will have to record your commands manually.');
            }
        },
        error: function(returned) {
            $.mobile.hidePageLoadingMsg();
            alert('Oh dear, something went wrong searching LIRC.');
        }
    });
}

function addActions(deviceID) {
    $.mobile.loadingMessage = 'Adding commands from LIRC.';
    $.mobile.showPageLoadingMsg();
    $.ajax({
        url: '/ir/addFromLIRC/' + deviceID + '/',
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify($('#selectRemoteModel').find("option:selected").val()),
        dataType: 'text',
        success: function(result) {
            $.mobile.hidePageLoadingMsg();
            alert('Succesfully added new actions.');
            location.reload(true);
        },
        error: function(returned) {
            $.mobile.hidePageLoadingMsg();
            alert('Oh dear, something went wrong adding actions from LIRC');
        }
    });
}
