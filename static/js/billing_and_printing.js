//------------------------dynamic billing------------------------------------------
    $('#billing-tab').tab('show');
    $('#qrcode-billing').click(function(){
        $.ajax({
            url: '{% url "QrcodeBilling" %}',
            type: 'get',
            data: {},
            success: function(response){
                $('#qty-qrcode').html(response);
            }
        });

    });

    function autocompleteProduct(){
        $(".particular").autocomplete({
          source: "{% url 'products' %}"
        });
    }
    autocompleteProduct();
    $('.input-discount').keyup(function(){
        let dis_amt = $(this).val();
        $(this).css('color', '#000');
        if(Number(dis_amt)>0 && Number(dis_amt)<=100){
            $(this).val(dis_amt);
        }else{
            $(this).val('');
        }
    });
    function getQty(){
        $('.particular').blur(function(){
           let id;
           let me = $(this);
           var currentRow = $(this).closest("tr");
           $.ajax({
            url: '{% url "qty_and_price" %}',
            type: 'get',
            data : {'product' : $(this).val() },
            dataType: 'json',
            success: function(response){
                console.log(response);
                //console.log(me.val());
                if(response.qty){
                    me.css('border', 'none');
                    id='.qty-'+1;
                    //$(id).val(response.qty);
                   currentRow.find(".qty").on('input', function(){
                    var quantity = $(this).val();
                    if((quantity !=='')&& (quantity.indexOf('.') === -1)){
                        $(this).val(Math.max(Math.min(quantity, response.qty),1));
                    }
                    console.log(Math.floor(Math.max(Math.min(quantity, response.qty),1)));
                    $(this).val(Math.floor(Math.max(Math.min(quantity, response.qty),1)));
                   });
                   currentRow.find(".qty").attr({
                        "max": response.qty,
                        "min": 1
                   });
                   currentRow.find(".price").html(response.price.toFixed(2)); // get current row 2nd table cell TD value
                   $(currentRow.find('.qty')).keyup(function(){
                        currentRow.find('.total').html(
                            ($(this).val()*response.price).toFixed(2)
                        );
                         //$("#myTable").on('input', '.txtCal', function () {
                       var calculated_total_sum = 0;

                       $(".items .total").each(function () {
                           var get_qty_val = $(this).html();
                           if ($.isNumeric(get_qty_val)) {
                              calculated_total_sum += parseFloat(get_qty_val);
                              }
                        });
                        $('.total-amt').html(calculated_total_sum.toFixed(2));
                        var dis=0;
                        //5% discount
                        if(calculated_total_sum >= 8000 && calculated_total_sum<10000){
                            dis=0.05;
                            $('.input-discount').val(5);

                        }
                        //10% discount
                        else if(calculated_total_sum >= 10000 && calculated_total_sum<=20000){
                            dis = 0.1;
                            $('.input-discount').val(10);
                        }//15% discount
                        else if(calculated_total_sum >20000){
                            dis = 0.15;
                            $('.input-discount').val(15);
                        }//no discount
                        else{
                            dis = 0;
                        }
                        var discount_amt = calculated_total_sum*dis;
                        $('.dis-val').html(discount_amt.toFixed(2));
                        $('.g-total').html((calculated_total_sum - discount_amt).toFixed(2));
                        $('#amt-in-words').html(amountInWords());
                   });
                   PRINT = 1;

                }else{
                    console.log("not found");
                    me.css('border', '2px solid red');
                    PRINT = 0;
                    //console.log(me.val());
                }

             }
           });
        });
    }
    getQty();
    var tr=1;
    function checkForNewRow(){
        $('.last').keyup(function(e){
        $(this).removeClass('last');
        //alert($(this).attr('id'));
        if(tr==$(this).attr('id'))
            if(e.keyCode===13){
                newRow();
            }
        });
    }

    function bgColor(){
        $('.items input').blur(function(){
            $(this).addClass('bg-dark');
            $(this).addClass('text-white');
        });

        $('.items input').focus(function(){
            $(this).removeClass('bg-dark');
            $(this).removeClass('text-white');
            //$(this).parent().parent().addClass('text-white');
         });
    }
    bgColor();
    checkForNewRow();

    function newRow(){
        tr+=1;//alert(tr);
        $('tbody.items').append(
            '<tr>'+
                '<td>'+tr+'.</td>'+
                '<td class="text-left input-particulars">'+
                    '<input type="text" style="width:100%; border: none;" class="particular particular-'+tr+' bg-dark"/>'+
                '<span></span></td>'+
                '<td class="input-qty">'+
                    '<input type="number" style=" width: 100px; border: none" id="'+tr+'" class="last qty bg-dark qty-'+tr+'"/>'+
                  '<span></span></td>'+
                '<td class="text-right pr-5 input-price price price-'+tr+'">0.00</td>'+
                '<td class="text-right pr-5 total total-'+tr+'">0.00</td>'+
            '</tr>'
        );
        bgColor();
        checkForNewRow();
        autocompleteProduct();
        var focusParticular = ".particular-"+tr;
        $(focusParticular).focus();
        getQty();
   }
   $('.input-discount').blur(function(){
        $(this).addClass('bg-dark');
        $(this).addClass('text-white');
   });
   $('.input-discount').focus(function(){
        $(this).removeClass('bg-dark');
        $(this).removeClass('text-white');
   });
   //--------------dynamic billing end --------------------------

   //-------------- bill date&time ---script start---------------

   setInterval(function(){
        datetime = new Date();
        $('.bill-datetime').html(datetime.toLocaleString());
        //console.log(datetime.toLocaleString());
   },999);
   //---------------end bill date&time-----------

   //--------------print bill -----------------------------------
   $('#customer-name').on('input', function(){
        const namePattern = /^[ a-zA-Z.]+$/;
        let name = $(this).val().trim();
        if(name.length)
            testCustomerInfo(namePattern, name, "name", this);
   });
   $('#customer-address').on('blur', function(){
        const addressPattern = /^[a-zA-Z0-9 -,]{2,50}$/;
        let address = $(this).val().trim();
        if(address.length>0)
            testCustomerInfo(addressPattern, address, "address", this);
        else
            $('.error').text("");
   });
   $('#customer-contact').on('blur', function(){
        const contactPattern = /^[0-9]{10}$/;
        let contact = $(this).val().trim();
        if(contact.length>0)
            testCustomerInfo(contactPattern, contact, "contact", this);
        else
            $('.error').text("");
   });

   function testCustomerInfo(pattern, fieldName, errorMsg, field){
        if(!pattern.test(fieldName)){
            errorMsg = 'invalid ' + errorMsg;
            $('.error').text(errorMsg);
            $(field).css('color', 'red');
            $(field).focus();
            PRINT = 0;
        }else{
            $('.error').text('');
            $(field).css('color', '#000');
        }
   }

   var PRINT = 0;
   $('.print-btn').click(printContent);

   function printContent(){
        var item = document.querySelector('.particular');
        if($('#customer-name').val().length == 0){
            alert("Please enter the name of the customer.")
            $('#customer-name').focus();
        }else if(item.value.length == 0){
            alert("EMPTY BILL\nPlease enter an item for billing");
            item.focus();
       }else if(!PRINT){
            alert("incorrect details...");
       }else{
           $('.particular').each(function(){
                $(this).closest('td').find('span').text($(this).val());
                $(this).css('display', 'none');
           });
           $('.qty').each(function(){
                $(this).closest('td').find('span').text($(this).val());
                $(this).css('display', 'none');
           });
            window.print();
            deductQty();
            $('.particular').each(function(){
                $(this).closest('td').find('span').text('');
                $(this).css('display', 'inline-block');
            });
            $('.qty').each(function(){
                $(this).closest('td').find('span').text('');
                $(this).css('display', 'inline-block');
            });
        }
   }

   function deductQty(){
        var token = $('input[name=csrfmiddlewaretoken]').val();
        var bill = makeBill();
        //console.log(bill);
        bill = JSON.stringify(bill);
        $.ajax({
            url: '{% url "deduct-qty" %}',
            type: 'post',
            data: {'bill': bill, 'csrfmiddlewaretoken': token},
            dataType: 'json',
            success: function(response){
                console.log(response);
            }
        });

        //alert("deduct");
   }

   function makeBill(){
    name = $('#customer-name').val();
    address = $('#customer-address').val();
    contact = $('#customer-contact').val();
    date_time = $('.bill-datetime').html();
    var items=[];
    $('.items tr').each(
    function (){
        item = $(this).find('.particular').val();
        qty = $(this).find('.qty').val();
        price = $(this).find('.price').html();
        total = $(this).find('.total').html();
        item1 ={
            item: item,
            qty: qty,
            price: price,
            total: total
        }
        items.push(item1);
    });
    amt_in_words = $('#amt-in-words').html();
    total_amt = $('.total-amt').html();
    discount = $('.dis-val').html();
    grantTotal = $('.g-total').html();
    sold_by = $('#sold-by').html();
    bill = {
        name : name,address: address,contact:contact,date:date_time,
        particulars : items,
        total_amt : total_amt,
        discount: discount,
        grant_total: grantTotal,
        amt_in_words: amt_in_words,
        sold_by: sold_by
    };

    return bill;
  }

   //---------------print bill end ----------------------------