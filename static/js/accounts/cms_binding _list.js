var page_list='/base/admin_bind_cms_parent/page/';   //导航页
var ajax_list='admin_get_parent_cms_list';
var add='';        //添加
var details='';   //详情
var untying_list_ajax='';   //解绑
if(layui_url==page_list){     //用户
    add='/base/admin_create_binding/page/';
    details='/base/admin_cms_details/page/';
    ajax_list='/base/ajax/admin_get_parent_cms_list/';
    untying_ajax_list='/base/ajax/admin_user_relieve_binding/';
    var cols=[
          {field:'username',title:gettext('客户账号')}
          ,{field:'company',title:gettext('公司名')}
          ,{field:'cms_username', title: gettext('CMS客户ID')}
          ,{field:'list_button', title: gettext('操作'),toolbar: '#list_button'}
        ]
}


layui.use(['table','form','laypage'], function(){
   var form = layui.form;
   var table = layui.table;
   var layer = layui.layer;
    var curr="";
    window.data_search = function () {
        var customer_account=$('#customer_account').val();
        var cms_username=$('#cms_username').val();
        var laypage= $('.layui-laypage-curr em:nth-child(2)').text();
        if(laypage == ''){
           curr=1;
        }else{
           curr=laypage;
        }
        $.ajax({
            type: "POST",
            url: ajax_list,
            data: {
                username:customer_account,
                cms_username:cms_username,
                page:curr,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                var table_list;
                if(res.status==true){
                    table_list=res.user_list;
                }else{
                    res_msg(res);
                }
                res_table(res,table_list,curr);
                table.render({
                    elem: '#accounts_list'
                    ,data:table_list
                    ,cols: [cols]
                    ,limit:10
                    , even: true //开启隔行背景
                    ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
                    ,done:function(){
                        $('.layui-none').text(gettext('暂无数据'));
                        $("[data-field = 'is_active']").children().each(function(){
                            if($(this).text() == 'true'){
                              $(this).text("启用");
                            }else if($(this).text() == 'false'){
                               $(this).text("禁用");
                            }
                        });
                        $("[data-field = 'company']").children().each(function(){
                            $(this).text(gettext($(this).text()))
                        });
                    }
                });
            }
        });
    };
    data_search();

    $('.search_user').click(function(){
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        data_search();
    });

    table.on('tool(parse-table-demo)', function(obj){   //用户详情
        var data = obj.data;
        var id=data.id;
        var username=data.username;
        if(obj.event === 'details'){   //用户详情
            var url_upload=details+id+'/';
            layui_nav_each(url_upload,page_list);

        }else if(obj.event === 'untying'){    //解绑
            layer.alert(gettext('确定解除当前选中账号的绑定关系？'), {
                title:gettext('解绑'),
                icon: 0,
                area:['400px','190px'],
                shade:0,
                btn:[gettext('确定'),gettext('取消')],
                btnAlign:'c',
                yes:function(index) {
                    $.ajax({
                        type: "POST",
                        url: untying_ajax_list,
                        data: {
                            username:username,
                            csrfmiddlewaretoken: $.cookie('csrftoken')
                        },
                        dataType : 'json',
                        error:function(){
                            lay_tips(gettext('通讯异常'));
                        },
                        async:false,
                        success: function(res){
                            if(res.status){
                                layer.close(index);
                                data_search();
                            }else{
                                res_msg(res);
                            }
                        }
                    })
                }
            });
            form.render();
        }
    });

    form.on('submit(create_binding_cms)',function(){  //创建绑定关系
        layui_nav_each(add,page_list);
    });

});


