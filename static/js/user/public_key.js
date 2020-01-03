var page_list='/base/parent_secret_info/page/';    //导航
var admin_key_list_ajax='';  //列表
var update_status_ajax='';   //状态
var del_ajax='';  //删除
var user_id='';
var table_list;
if(is_staff == 'True'){
    admin_key_list_ajax='/base/ajax/admin_open_parent_api/';  //列表
    update_status_ajax='/base/ajax/admin_set_parent_api_status/';   //状态
    del_ajax='/base/ajax/admin_set_parent_api_remove/';  //删除
    user_id=parent_oblique[parent_oblique.length-2]

}else{
    admin_key_list_ajax='/base/ajax/client_open_parent_api/';  //列表
    update_status_ajax='/base/ajax/client_set_parent_api_status/';   //状态
    del_ajax='/base/ajax/client_set_parent_api_remove/';  //删除
    username=''
}
var cols=[        //证书表头
          {field:'secret_id',title:'Access Key'}
          ,{field:'secret_key',title:'Secret Key',event: 'secret_key',style:'cursor: pointer;color:#2c80e3;'}
          ,{field:'create_time',title:gettext('创建时间')}
          ,{field:'status',title:gettext('状态')}
          ,{field:'type',title:gettext('类型')}
          ,{field:'list_button', title: gettext('操作'),toolbar: '#list_button'}
        ]


layui.use(['table','form','laypage'], function(){
   var form = layui.form;
   var table = layui.table;
   var curr="";
   form.on('submit(add_new_key)',function(){
        window.data_search()
   });

   var table_list=[];
   if(api_info == undefined ){
       table_list=[]
   }else{
       table_list=api_info;
   }

   window.data_search = function () {
        table_list=[]
        $.ajax({
            type: "POST",
            url: admin_key_list_ajax,
            data: {
                username:username,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                if(res.status==true){
                    table_list=res.api_info;
                }else{
                    table_list=[];
                    res_msg(res);
                }
                table_render(table_list)

            }
        });

    };
    function table_render(table_list){
        table.render({
            elem: '#api_key'
            ,data:table_list
            ,cols: [cols]
            ,limit:10
            , even: true
            ,cellMinWidth: 80
            ,done:function(){
                $("[data-field = 'status']").children().each(function(){   //状态转换
                    if($(this).text() == 1){
                        $(this).text(gettext('启用'))
                        $(this).parents('tr').find('.layui_status').text(gettext('禁用'));
                    }else{
                        $(this).text(gettext('禁用'))
                        $(this).parents('tr').find('.layui_status').text(gettext('启用'));
                    }
                });
                $("[data-field = 'secret_key']").children().each(function(index){   //状态转换
                    if(index>0){
                        $(this).text(gettext('显示'))
                    }

                });

            }
        });
        table.render();
    }
    table_render(table_list)

    // window.data_search()


    table.on('tool(api_key)', function(obj){   //操作列
        var obj_this=$(this);
        var obj_this_text=obj_this.parents('tr').find("[data-field = 'status']").children().text();

        var data=obj.data;
        if(obj.event === 'secret_key'){
            obj_this.parents('tr').find("[data-field = 'secret_key']").children().text(data.secret_key)
        }else if(obj.event === 'status'){
            if(gettext(obj_this_text) == '禁用'){
                var status=1;
            }else{
                var status=0;
            }
            $.ajax({
                type: "POST",
                url: update_status_ajax,
                data: {
                    user_id:user_id,
                    api_status:status,
                    csrfmiddlewaretoken: $.cookie('csrftoken')
                },
                async:false,
                success: function(res){
                    if(res.status){
                        if(status==0){
                            obj_this.parents('tr').find("[data-field = 'status']").children().text(gettext('禁用'))
                            obj_this.parents('tr').find(".layui_status").text(gettext('启用'))
                        }else{
                            obj_this.parents('tr').find("[data-field = 'status']").children().text(gettext('启用'))
                            obj_this.parents('tr').find(".layui_status").text(gettext('禁用'))
                        }
                    }else{
                        res_msg(res);
                    }
                }
            });

        }else if(obj.event === 'del'){
            $.ajax({
                type: "POST",
                url: del_ajax,
                data: {
                    user_id:user_id,
                    csrfmiddlewaretoken: $.cookie('csrftoken')
                },
                async:false,
                success: function(res){
                    if(res.status){
                        obj_this.parents('tr').remove();
                        if($('.layui-table tbody tr').length == 0){
                            $('.layui-table tbody').html('<tr><td style="text-align: center">'+gettext('暂无数据')+'</td></tr>')
                        }

                    }else{
                        res_msg(res);
                    }
                }
            });
        }

    });

});


