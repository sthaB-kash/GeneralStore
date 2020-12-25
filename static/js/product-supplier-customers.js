    function dynamicValues(){
        var s_value = 140;//Number($('.s-value').html());
        var c_value = 5040, p_value = 4000;
        var s_incr = getIncrement(s_value);
        var c_incr = getIncrement(c_value), p_incr = getIncrement(p_value);
        var init_s_value = 0, init_c_value= 0, init_p_value = 0;
        $('.s-value').html(init_s_value);
        $('.c-value').html(init_c_value);
        $('.p-value').html(init_p_value);

        //console.log(s_value);
        var stop_s = setInterval(function(){
            $('.s-value').html(init_s_value+=s_incr);
            if(init_s_value >= s_value){
                init_s_value = s_value;
                clearInterval(stop_s);
                $('.s-value').html(s_value)
            }
        }, ((s_value < 100) ? 50: (s_value <500)? 20: (s_value<1000)?10:(s_value<2000)?5:2));
        var stop_c = setInterval(function(){
            $('.c-value').html(init_c_value+=c_incr);
            if(init_c_value >= c_value){
                init_c_value = c_value;
                clearInterval(stop_c);
                $('.c-value').html(c_value)
            }
        },((c_value < 100) ? 50: (c_value <500)? 20: (p_value<1000)?10:(c_value<2000)?5:2));
        var stop_p = setInterval(function(){
            $('.p-value').html(init_p_value+=p_incr);
            if(init_p_value >= p_value){
                init_p_value = p_value;
                clearInterval(stop_p);
                $('.p-value').html(p_value)
            }
        },((p_value < 100) ? 50: (p_value <500)? 20: (p_value<1000)?10:(p_value<2000)?5:2));
        //setTimeout(function(){clearInterval(stop)},2000);

    }
    //function to return increment value for each
    function getIncrement(val){
        if(val>100 && val<500)
            incr = 3;
        else if(val>=500 && val<1000)
            incr = 4;
        else if(val >= 1000 && val<2000)
            incr = 5;
        else if(val>=2000)
            incr = 10;
        else
            incr = 2;

        return incr;
    }

    dynamicValues();
    $('#products-tab').click(function(){
        dynamicValues();
    })