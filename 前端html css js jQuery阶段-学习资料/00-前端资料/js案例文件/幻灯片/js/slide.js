$(function(){
    var $li = $('.slide_list li');
    var iLen = $li.length;
    var $points = $('.points');
    var $prev = $('.prev');
    var $next = $('.next');
    var iNowli = 0;
    var iPrevli = 0;
    var bIsmove = false;
    var oTimer = null;    

    // 除了第一张幻灯片，将其他的幻灯片放到右边去
    $li.not(':first').css({'left':760});

    //根据幻灯片的个数来动态创建小圆点
    for(var i=0;i<iLen;i++)
    {
        var $pli = $('<li>');
        if(i==0)
        {
            $pli.addClass('active');
        }
        $pli.appendTo( $points  );
    }

    var $pointli = $('.points li');

    $pointli.click(function(){
        iNowli = $(this).index();
        fnMove();
        $(this).addClass('active').siblings().removeClass('active');
    })


    $prev.click(function(){
        if(bIsmove)
        {
           return; 
        }
        bIsmove = true;
        iNowli--;
        fnMove();
        $pointli.eq(iNowli).addClass('active').siblings().removeClass('active');
    });

    $next.click(function(){
        if(bIsmove)
        {
           return; 
        }
        bIsmove = true;
        iNowli++;
        fnMove();
        $pointli.eq(iNowli).addClass('active').siblings().removeClass('active');
    });


    function fnAutoplay(){
        iNowli++;
        fnMove();
        $pointli.eq(iNowli).addClass('active').siblings().removeClass('active');
    }

    oTimer = setInterval(fnAutoplay,4000);

    $('.slide').mouseenter(function(){
        clearInterval(oTimer);
    })

    $('.slide').mouseleave(function(){
       oTimer = setInterval(fnAutoplay,4000);
    })


    function fnMove(){

        // 解决重复点击某个小圆点的bug
        if(iNowli==iPrevli)
        {
           return; 
        }

        //在第一张幻灯片再点击向左的按钮的时候
        if(iNowli<0)
        {
           iNowli = iLen-1;
           iPrevli = 0;
           $li.eq(iNowli).css({'left':-760});
           $li.eq(iNowli).animate({'left':0});
           $li.eq(iPrevli).animate({'left':760},function(){
               bIsmove = false;
           });
           iPrevli = iNowli;
           return;
        }

        //在最后一张幻灯片再点击向右的按钮的时候
        if(iNowli>iLen-1)
        {
           iNowli = 0;
           iPrevli = iLen-1;
           $li.eq(iNowli).css({'left':760});
           $li.eq(iNowli).animate({'left':0});
           $li.eq(iPrevli).animate({'left':-760},function(){
               bIsmove = false;
           });
           iPrevli = iNowli;
           return; 
        }

        //从小的往大的切换
        if(iNowli>iPrevli)
        {
            $li.eq(iNowli).css({'left':760});      
            $li.eq(iPrevli).animate({'left':-760});          
        }
        else //从大的往小的切换
        {
            $li.eq(iNowli).css({'left':-760});           
            $li.eq(iPrevli).animate({'left':760});           
        }

        $li.eq(iNowli).animate({'left':0},function(){
               bIsmove = false;
           });
        iPrevli = iNowli;
    }

})