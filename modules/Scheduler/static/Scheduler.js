$('.schedule-active').change(function() {
    id = $(this).attr('id').split('-')[2];
    data = $(this).find("option:selected").val()
    $.ajax({
        url: '/scheduler/editActive/' + id +'/',
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        dataType: 'text',
        success: function(result) {}
    });
});

