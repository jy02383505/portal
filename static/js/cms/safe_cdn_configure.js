var page_list='/sec/admin_sec_user_list/page/';
console.log(parent_split)
var username=parent_split[parent_split.length-1];

layui.use(['form'], function() {
    var form = layui.form;
    var index_ado;
    var back_source_type = document.getElementsByName('back_source_type');  //服务商
    var appoint_token = document.getElementById('appoint_token');
    for(var i=0;i<back_source_type.length;i++){
        if(back_source_type[i].checked && back_source_type[i].value==gettext('默认')){
            appoint_token.disabled=true;
        }
    }
    form.on('radio(back_source_type)',function(data){
        if(data.value != gettext('默认')){
            appoint_token.disabled=false;
        }else{
            appoint_token.disabled=true;
        }

    });
    form.on('submit(cancel_service_con)',function(){   //取消
         layui_nav_each(page_list,page_list);
    });
    form.on('submit(sure_service_con)',function(){
        var appoint_token_value='';
        if(appoint_token.disabled != true){
            appoint_token_value=appoint_token.value;
        }
        console.log(username)
        $.ajax({
            type: "POST",
            url: '/base/ajax/admin_set_user_strategy_conf/',
            data: {
                username:username,
                value:appoint_token_value,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            error:function(){
                lay_tips(gettext('通讯异常'));
            },
            success: function(res){
                console.log(res);
                if(res.status){
                    layer.close(index_ado);
                    layui_nav_each(page_list,page_list);
                }else{
                    res_msg(res)

                }
            }
        })
    });
    form.render();
});