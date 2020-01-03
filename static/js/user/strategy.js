
data_strategy=function(e,data){
    var strategy_list='';
    for(var perm_strategy in perm_strategy_list){
        var perm_strategy=perm_strategy_list[perm_strategy];
        if(e==undefined || e==''){
            strategy_list +='<li id="'+perm_strategy.id+'" value="'+perm_strategy.strategy_type_name+'"><p>'+perm_strategy.name+'</p><span>'+perm_strategy.remark+'</span></li>'
        }else if(e==perm_strategy.strategy_type_name && data==0){

            strategy_list +='<li id="'+perm_strategy.id+'" value="'+perm_strategy.strategy_type_name+'"><p>'+perm_strategy.name+'</p><span>'+perm_strategy.remark+'</span></li>'
        }else if(e==perm_strategy.name || e==perm_strategy.remark && data==1){

            strategy_list +='<li id="'+perm_strategy.id+'" value="'+perm_strategy.strategy_type_name+'"><p>'+perm_strategy.name+'</p><span>'+perm_strategy.remark+'</span></li>'
        }
    }
    $('.policy').html(strategy_list);
};
data_strategy();

layui.use(['form','table','element','layer'], function(){
    var form=layui.form;
    form.on('select(screening_strategy)', function(e){
        var data=0;
       data_strategy(e.value,data);
    });
    $('.search_user').click(function(){
        var this_value=$(this).prev('input').val();
        var data=1;
        data_strategy(this_value,data);
    });
    $(document).on('click','.policy li',function(){       //选择策略
        $(this).clone();
        var img='<img src="/static/image/bin.png" />';
        if(!$(this).hasClass('gray')){
            if($('.added').html()==''){
                $('.added,.permission_ul').html($(this).clone());

            }else{
                $('.added,.permission_ul').prepend($(this).clone());
            }
        }
        $(this).addClass('gray');
        $('.added li').append(img);

    });
    var server_tr=[];
    $('.server_tbody tr').each(function(){       //选择策略
        server_tr.push($(this).attr('id'));

    });
    /*$('.policy li').each(function(){       //选择策略
        for(var i=0;i<server_tr.length;i++){
            if(server_tr[i]==$(this).attr('id')){
                $(this).addClass('gray');
            }
            $(this).clone();
            var img='<img src="/static/image/bin.png" />';
            if(!$(this).hasClass('gray')){
                if($('.added').html()==''){
                    $('.added,.permission_ul').html($(this).clone());

                }else{
                    $('.added,.permission_ul').prepend($(this).clone());
                }
            }
            $(this).addClass('gray');
            $('.added li').append(img);
        }
    });*/

    $(document).on('click','.added li img',function(){       //删除策略
        // $(this).clone();
        var add_id=$(this).parent().attr('id');
        $('.policy li').each(function(){
            if($(this).attr('id')==add_id){
                $(this).removeClass('gray');
            }
        });
        $(this).parent('li').remove();

    });
});
