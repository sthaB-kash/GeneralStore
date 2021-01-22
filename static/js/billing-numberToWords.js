var num = {
            '1':'one',
            '2':'two',
            '3':'three',
            '4':'four',
            '5':'five',
            '6':'six',
            '7':'seven',
            '8':'eight',
            '9':'nine',
            '10':'ten'
        };

        var elevenToNineteen = {
            '11':'eleven', '12':'twelve', '13':'thirteen', '14':'fourteen', '15':'fifteen', '16':'sixteen', '17':'seventeen', '18':'eighteen', '19':'nineteen'
        };
        var tens = [
            'twenty', 'thirty', 'fourty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'
        ];


       //document.querySelector('.qty').addEventListener('input',
       function amountInWords(amt){
            console.log(amt);
            var amount = Number(amt).toFixed(2);
            amount = amount.split('.');
            var rupees = ''
            var paisa = '';
            if(amount.length===2)
                //console.log(amount[0],amount[1]);
                //for rupees
                n = Number(amount[0]);
                if(n===0)
                    rupees = '';
                else if(n<100){
                    rupees = returnValue(n) + " rupees";
                }
                else if(n<=999){
                    rupees = hundred(n);
                }
                else if(n<=99999){
                    rupees = thousand(n);
                }
                else if(n<=9999999){
                    rupees = returnValue(parseInt(n/100000))  + " lakha " + thousand(n%100000);
                }
                //for paisa
                n = Number(amount[1]);
                if(n===0)
                    paisa = '';
                else
                    paisa = returnValue(n) + ' paisa';

            //val.innerHTML = amount;
            //console.log(rupees + ' ' + paisa);
            return rupees + ' ' + paisa;
       }//);

       function returnValue(n){
           var value = 0;
            if(n<=10){
                value = n.toString();
                value = num[value];
            }
            else if (n<20){
                value = n.toString();
                value = elevenToNineteen[value];
            }
            else{
                var p1 = parseInt(n/10);
                var p2 = n%10;
                value = tens[p1-2];
                if(p2!=0)
                    value = value +'-'+ num[p2];
            }

           return value;
       }
       function hundred(n){
           //console.log("for hundred: "+n);
            if(n==0)
                rupees = 'rupees';
            else if(n<100)
                rupees =returnValue(n) + " rupees";
            else if(n%100!=0)
                rupees = returnValue(parseInt(n/100)) + " hundred " + returnValue(n%100) + " rupees";
            else{
                rupees = returnValue(parseInt(n/100)) + " hundred" + " rupees";
            }

            return rupees;
       }
       function thousand(n){
        //console.log("for thousand: "+n);
        if(n==0)
            rupees = 'rupees';
        else if(n<1000)
            rupees = hundred(n);
        else if(n%1000!=0)
            rupees = returnValue(parseInt(n/1000))  + " thousand " + hundred(n%1000);
        else
            rupees = returnValue(parseInt(n/1000)) + " thousand rupees";
        return rupees;

       }
