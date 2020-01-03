var add='';        //添加
var details='';   //详情
var o_List='';  //操作页面
var ajax_list='';  //页面列表
var log_list='';  //操作列表
var page_list=''; //页面
if(layui_url=='/base/admin_parent_list/page/'){     //用户
    add='create_parent_user';
    details='admin_parent_details';
    o_List='admin_parent_opt_log';
    ajax_list='admin_get_parent_list';
    log_list='admin_parent_opt_log';
    page_list='admin_parent_list';
    var cols=[
          {field:'username',title:gettext('用户名'),event: 'username',style:'cursor: pointer;color:#2c80e3;'}
          ,{field:'is_active',title:gettext('用户状态')}
          ,{field:'user_type', title: gettext('用户类型')}
          ,{field:'list_button', title: gettext('操作'),toolbar: '#list_button'}
        ]

}else if(layui_url=='/base/admin_admin_list/page/'){   //管理员
    add='create_admin_user';
    details='admin_admin_details';
    o_List='admin_admin_opt_log';
    ajax_list='admin_get_admin_list';
    log_list='admin_admin_opt_log';
    page_list='admin_admin_list';
    var cols=[
          {field:'username',title:gettext('用户名') ,event: 'username',style:'cursor: pointer;color:#2c80e3;'}
          ,{field:'is_active',title:gettext('用户状态')}
          ,{field:'group_name', title: gettext('用户类型')}
          ,{field:'list_button', title: gettext('操作'),toolbar: '#list_button'}
        ]
}else if(layui_url=='/base/admin_group_manage/page/'){  //角色
    add='admin_group_create';
    details='admin_group_details_views';
    ajax_list='admin_get_group_list';
    page_list='admin_group_manage';
    delete_list='admin_group_delete';
    delete_content=gettext('角色的所有信息都将被删除')+',<br>'+gettext('确定删除该角色？');
    var cols=[
      {field:'name',title:gettext('角色') ,event: 'username',style:'cursor: pointer;color:#2c80e3;'}
      ,{field:'desc',title:gettext('描述')}
      ,{field:'remark', title: gettext('备注')}
      ,{field:'list_button', title: gettext('操作'),toolbar: '#list_button'}
    ]
}
$(document).on('click','#add_user',function(){       //新建用户
    var url_upload='/base/'+add+'/page/';
    layui_nav_each(url_upload,'/base/'+page_list+'/page/');
});
layui.use(['table','form','laypage'], function(){
   var form = layui.form;
   var table = layui.table;
   var curr="";
    window.data_search = function () {
        var username=$('#username').val();
        var is_active=$('#select_status option:selected').val();
        var user_type=$('#select_type option:selected').val();
        if(is_active=='-1'){
           is_active='';
        }
        if(user_type=='-1'){
           user_type='';
        }

        var laypage= $('.layui-laypage-curr em:nth-child(2)').text();
        if(laypage == ''){
           curr=1;
        }else{
           curr=laypage;
        }
        $.ajax({
            type: "POST",
            url: '/base/ajax/'+ajax_list+'/',
            data: {
                id:'',
                username:username,
                is_active:is_active,
                user_type:user_type,
                groups__id:user_type,
                info:username,
                page:curr,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                var table_list;
                if(res.status==true){
                    if(layui_url =='/base/admin_group_manage/page/'){
                        table_list=res.groups;
                    }else{
                        table_list=res.user_list;
                    }
                }else{
                    res_msg(res);
                }

                if(layui_url !='/base/admin_group_manage/page/'){
                   res_table(res,table_list,curr);
                }

                table.render({
                    elem: '#accounts_list'
                    ,data:table_list
                    ,cols: [cols]
                    ,limit:10
                    , even: true //开启隔行背景
                    ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
                    ,done:function(res){
                        $('.layui-none').text(gettext('暂无数据'));
                        $("[data-field = 'is_active']").children().each(function(){
                            if($(this).text() == 'true'){
                              $(this).text(gettext('启用'));
                            }else if($(this).text() == 'false'){
                               $(this).text(gettext('禁用'));
                            }
                        });
                        $("[data-field = 'user_type'],[data-field = 'group_name'],[data-field = 'name']").children().each(function(){
                            $(this).text(gettext($(this).text()))
                        });
                    }
              });


            }
        });
    };

    data_search();
    form.on('select(username)', function(){
       $('.layui-laypage-curr em:nth-child(2)').text('1');
       data_search();
    });
    form.on('select(select_status)', function(){
       $('.layui-laypage-curr em:nth-child(2)').text('1');
       data_search();
    });
    $('.search_user').click(function(){
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        data_search();
    });

    form.on('select(select_type)', function(){
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        data_search();
    });

    table.on('tool(parse-table-demo)', function(obj){   //用户详情
        var data = obj.data;
        if(obj.event === 'username'){   //用户详情
            var url_upload='/base/'+details+'/page/'+data.id+'/';
            layui_nav_each(url_upload,'/base/'+page_list+'/page/');

        }else if(obj.event === 'edit'){   //操作日志
            var url_upload='/base/'+o_List+'/page/';
            layui_nav_each(url_upload,url_upload,data.username);
        }else if(obj.event === 'del'){   //操作日志
            layer.open({
                type: 1
                ,title: gettext('删除')
                ,area: ['400px', '200px']
                ,btnAlign: 'l'
                ,shade:0
                ,btnAlign: 'c'
                ,id: 'tips_layer'
                ,content: gettext('确认删除该角色？')
                ,btn: [gettext('是，确认删除'),gettext('否，取消删除')]
                ,yes: function(index_ado){
                    $.ajax({
                        type: "POST",
                        url: '/base/ajax/'+delete_list+'/',
                        data: {
                            obj_id: data.id,
                            csrfmiddlewaretoken: $.cookie('csrftoken')
                        },
                        async:false,
                        success: function(res){

                            if(res.status){
                                window.location.reload();
                            }else{
                                lay_tips(res.msg);

                            }
                        }
                    });
                }
            });
        }
    });

});