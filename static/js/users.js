$('#users').click(function(){
    $.ajax({
        url: '/users/',
        type: 'get',
        data: {},
        success: function(response){
            $('.user-info').html(response);
        }
    });
});

