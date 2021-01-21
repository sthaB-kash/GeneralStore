$('#reports-tab').click(function(){
    $.ajax({
        url: '/reports/',
        type: 'get',
        //data: {},
        success: function(data){
            $('#all-reports').html(data);
        },
        error: function(){
            alert('something went wrong');
        }
    });
});


//$('.all-reports-div>div').mouseover(function(){
//    $(this).css({
//        'color': '#fff',
//        'background': 'rgb(67,109,201)'
//
//    });
//});