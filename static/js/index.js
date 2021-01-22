
var generalStore = document.querySelector('.generalStore');
var tabContent = document.querySelector('.nav-content');
var products = document.querySelector(".products");
var nav = document.querySelector('.nav-tabs');
var insertProduct = document.querySelector('.add');


/*hide general-store content on page load*/
document.querySelector('.general-store').style.display = "none";
nav.addEventListener('click',function(){
    document.querySelector('.tab-content').style.display = "block";
    document.querySelector('.general-store').style.display = "none";
});


generalStore.addEventListener('click',showHide);

function showHide(){
    let navLinks = document.querySelectorAll('.nav-link');
    document.querySelector('.general-store').style.display = "block";
    document.querySelector('.tab-content').style.display = "none";
    for(navLink of navLinks){
        navLink.classList.remove("active");
    }
}


//add new product
//insertProduct.addEventListener('click', addProduct);
/*function addProduct(){
    let data = document.querySelector('.table-data');
    let tr = document.createElement('tr');
    let sn= data.childElementCount;
    let tdSn = document.createElement('td');
    let tdName = document.createElement('td');
    let tdEntryDate = document.createElement('td');

    data.appendChild(tr);
    tdSn.appendChild(document.createTextNode((sn+1).toString()));
    tr.appendChild(tdSn);

    tdName.appendChild(document.createTextNode("abc"));
    tr.appendChild(tdName);
}*/



//delete confirmation
function deleteProduct(id, name){
    //const choice = confirm('Are you sure to delete this product?', name);
    document.querySelector('#deleteMsg').innerHTML = "<strong>"+name+"</strong>";
    $('#del-product').attr('href', '');
    //document.querySelector('#del-product').href
 }


 // for notification
 $('.notification').click(function(){
    //alert('im clicked');
    $.ajax({
        url: '/notification/',
        type: 'get',
        success: function(response){
            $('.notification-box').html(response);

            $('.notification-box').css('display', 'inline-block');
        }
    });
 });

//hide .notification-box when clicked outside of it
 function handler(event) {
      event.stopPropagation();
 }
$(".notification-box").click(handler);

$('body').click(function(){
    if (document.querySelector('.notification-box').style.display == 'inline-block'){
        $('.notification-box').html('');
        $('.notification-box').css('display', 'none');
    }
});