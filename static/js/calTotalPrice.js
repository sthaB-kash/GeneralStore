//cal total price
/*
var qty = document.getElementById('inputQty');
var inputPrice = document.getElementById('inputPrice');
document.getElementById('inputPrice').addEventListener('keyup',calTotalPrice);
qty.addEventListener('keyup',calTotalPrice);
function calTotalPrice(){
    if (Number(inputPrice.value)>0){
        let totalPrice = Number(qty.value) * Number(inputPrice.value);
        document.getElementById('totalPrice').placeholder = totalPrice.toString();
        }
}
*/
$('.inputPrice').keyup(calTotalPrice);
$('.inputQty').keyup(calTotalPrice);
function calTotalPrice(){
    if(Number($('.inputPrice').val())>0){
        let totalPrice = Number($('.inputPrice').val()) * Number($('.inputQty').val())
        $('.totalPrice').val(totalPrice);
    }
}
