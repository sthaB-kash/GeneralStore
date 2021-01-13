$('#inputSearch').keyup(function(){
        //alert($(this).val());
        /*var xmlhttp = new XMLHTTPRequest();
        xmlhttp.onreadystatechange = function(){
            document.getElementById('searched-data').innerHTML = xmlhttp.responseText;
        }
        xmlhttp.open('GET', 'search?data='+$(this).val(), true)
        xmlhttp.send();*/

        $.ajax({
            url: '/search/',
            type: 'get',
            data: { 'data': $(this).val()},
            success: function(response){
                $('#searched-data').html(response);
            }
        });
     });
