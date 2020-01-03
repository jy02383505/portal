var  ajax_list='edit_admin_user';       //接口
var  page_list='/base/admin_admin_list/page/';//导航地址
layui.use(['form','table','element','layer'], function(){
    var form = layui.form;
    form.on('submit(user_sure)',function(){   //确定
        data_aggregation();
    });
    //页面数据
    function data_aggregation(){
        var username=$('#username').text();   //用户
        var is_active=$('#select_status option:selected').val();  //状态
        var group_id=$('#role option:selected').val();    //角色id
        $.ajax({
            type: "POST",
            url: '/base/ajax/'+ajax_list+'/',
            data: {
                username:username,
                is_active:is_active,
                group_id:group_id,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                if(res.status){
                    layui_nav_each(page_list,page_list);
                }else{
                    res_msg(res);
                }
            }
        });

    }

    form.on('submit(user_cancel)',function(){   //取消
        layui_nav_each(page_list,page_list);
    });
});
