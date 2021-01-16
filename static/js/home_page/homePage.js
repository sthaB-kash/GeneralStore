
        var timer = setInterval(move, 30);
        var left = 0;
        function move(){
             left += 2;
             if(left<=931){
                supplierContainer.scrollLeft = left;
             }else{
                left = 0;
             }
        }
        function pause(){
            clearInterval(timer);
        }
        const supplierContainer = document.querySelector('.supplier-container');
        //console.log(theDiv.scrollLeft);
        $('.supplier').mouseover(pause);
        $('.supplier').mouseout(setTimer);

        function setTimer(){
            timer = setInterval(move, 30);
        }

        $('.move-left').click(function(){
            if(left<931)
                left += 100;
        });

        $('.move-right').click(function(){
            if(left>50)
                left -= 100;
        });
        $('.move-right').mouseover(function(){
            //$(this).css('padding', '20px');
        });

        //-------------------------------------------------------------------
        //when mouse hover to show product btn then stop animation and vice-versa

        $('.view-product-btn').mouseover(animationResumeStop);
        $('.view-product-btn').mouseout(animationResumeStop);

        //---------------------------------------------------------------
        $('.close-btn').click(function(){

        });


        //when modal is dismissed
        $('#productDetails').on('hidden.bs.modal', function (e) {
            setTimer();
            console.log(e);
            //animation resume
            animationResumeStop();
        });


        function animationResumeStop(){
            $('.view-product-btn').toggleClass('animate');
            $('.view-product-btn span').toggleClass('animate-text');
        }
        // show available products
        $('.view-product-btn').click(function(){
            //alert('clicked');

            $('#productDetails').modal('show');
            //stop animation
            clearInterval(timer);
            animationResumeStop();


            /*try{
                $('#back-div').remove();
                //console.log($('#back-div'));

            }catch(e){
                 console.log(e);
                 console.log(e.name);
                 console.log(e.message);
            }finally{
                const backDiv = document.createElement('div');
                document.querySelector('body').appendChild(backDiv);
                backDiv.classList.add('back-div');
                backDiv.id = 'back-div';

                const okBtn = document.createElement('button');
                const okBtnText = document.createTextNode('OK');
                okBtn.appendChild(okBtnText);
                backDiv.appendChild(okBtn);

                $(backDiv).css({
                    'position': 'absolute',
                    'top': '0',
                    'left': '0',
                    'width': '100%',
                    'height':'100vh',
                    'background': 'rgba(0,0,0, 0.6)',
                    'z-index': '5'
                });

            }*/

        });