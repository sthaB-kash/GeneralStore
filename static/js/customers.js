$('#customers-tab').click(function(){
//alert("customer loaded");
    $.ajax({
        url: '/customer_details/',
        type: 'get',
        //data: {},
        success: function(data){
            $('#customer-details').html(data);
        },
        error: function(){
            alert('something went wrong');
        }
    });
});