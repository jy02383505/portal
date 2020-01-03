var page_list='/base/parent_secret_info/page/';    //导航
var add_key='/base/ajax/client_open_parent_api/';        //添加证书
var admin_key_list_ajax='/base/ajax/client_open_parent_api/';  //列表
var update='/base/ajax/client_set_parent_api_status/';   //状态
var del_ajax='/base/ajax/client_set_parent_api_remove/';  //删除
// var cert_status_array=cert_status;
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
   form.on('submit(add_key)',function(){
        window.data_search()
   });
    window.data_search = function () {
        var table_list=[];
        $.ajax({
            type: "POST",
            url: admin_key_list_ajax,
            data: {
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                console.log(res);
                if(res.status==true){
                    table_list=res.api_info;
                }else{
                    table_list=[];
                    res_msg(res);
                }
                table.render({
                    elem: '#lay_table'
                    ,data:table_list
                    ,cols: [cols]
                    ,limit:10
                    , even: true
                    ,cellMinWidth: 80
                    ,done:function(){
                        $('.layui-none').text(gettext('暂无数据'));
                        $("[data-field = 'status']").children().each(function(){   //状态转换
                            if($(this).text() == 1){
                                $(this).text(gettext('启用'))
                                $(this).parents('tr').find('.layui_status').text(gettext('禁用'));
                            }else{
                                $(this).text(gettext('禁用'))
                                $(this).parents('tr').find('.layui_status').text(gettext('启用'));
                            }
                        });
                        $("[data-field = 'secret_key']").children().each(function(){   //状态转换
                            $(this).text(gettext('显示'))
                        });

                    }
                });
                table.render();

            }
        });

    };


    table.on('tool(lay_table)', function(obj){   //用户详情
        var data = obj.data;
        console.log(data);
        if(obj.event === 'secret_key'){

        }else if(obj.event === 'details'){   //
            var url_upload=details+data.cert_name+'/'+data.user_id+'/';
            layui_nav_each(url_upload,page_list);
        }else if(obj.event === 'up_data'){   //详情
            var url_upload=update+data.cert_name+'/'+data.user_id+'/';
            layui_nav_each(url_upload,page_list);
        }else if(obj.event === 'del'){   //更新
            layer.open({
              title:gettext('删除'),
              skin:'skin_class',
              type: 1,
              shade:0,
              area:['400px','220px'],
              btn: [gettext('确定'),gettext('取消')],
              content:'<div class="lay_content">'+gettext('确定删除该证书？')+'</div>',  //这里content是一个普通的String
              yes:function(){
                console.log(data.cert_name);
                $.ajax({
                    type: "POST",
                    url: del_ajax,
                    data: {
                        cert_name:data.cert_name,
                        user_id:data.user_id,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    },
                    async:false,
                    success: function(res){
                        if(res.status==true){
                            data_search();
                            layer.close(index);
                        }else{
                            res_msg(res);
                        }

                    }
                });

              }
        });

        }
    });

});