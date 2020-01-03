
var page_list='';  //当前导航地址
var admin_cdn_user_ajax='';   //查询借口
var cdn_base_conf=''; //融合cdn配置
var get_domain_list='';  //域名列表页面
var admin_statistics_list='';  //统计

if(layui_url=='/cdn/admin_cdn_user_list/page/'){     //管理员端用户
    admin_cdn_user_ajax='/cdn/ajax/admin_cdn_user_list/';
    cdn_base_conf='/cdn/admin_cdn_base_conf/page/';
    page_list='/cdn/admin_cdn_user_list/page/';
    get_domain_list='/cdn/admin_get_domain_list/page/';
    admin_statistics_list='/cdn/admin_statistics/page/';
    var cols=[
          {field:'username',title:gettext('用户')}
          ,{field:'cdn_opt',title:gettext('服务商')}
          ,{field:'list_button', title: gettext('操作'),toolbar: '#list_button'}
        ]
}
layui.use(['table','form','layer','laypage'], function(){
   var layer = layui.layer;
   var form = layui.form;
   var table = layui.table;
   var curr="";
   window.data_search = function () {
        var username=$('#username').val();
        var laypage= $('.layui-laypage-curr em:nth-child(2)').text();
        if(laypage == ''){
           curr=1;
        }else{
           curr=laypage;
        }

        $.ajax({
            type: "POST",
            url: admin_cdn_user_ajax,
            data: {
                id_or_username:username,
                page:curr,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                var table_list;
                if(res.status==true){
                    table_list=res.cdn_user_list;
                }else{
                    res_msg(res);
                }
                console.log(res)
                res_table(res,table_list,curr);
                table.render({
                    elem: '#user_list'
                    ,data:table_list
                    ,cols: [cols]
                    ,limit:10
                    , even: true //开启隔行背景
                    ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
                    ,done:function(){
                        $('.layui-none').text(gettext('暂无数据'));
                        $("[data-field = 'cdn_opt']").children().each(function() {   //状态转换
                            for(var opt in opt_type){
                                var opt=opt_type[opt];
                                if(opt.id == $(this).text()){

                                }
                            }

                        })
                    }
                });

                table.render();
            }
        });
    };

    data_search();
    $('.search_user').click(function(){
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        data_search();
    });

    table.on('tool(parse-table-demo)', function(obj){   //操作
        var data = obj.data;
        if(obj.event === 'cdn_configure'){   //融合CDN配置
            var url_upload=cdn_base_conf+data.user_id+'/';
            layui_nav_each(url_upload,page_list);

        }else if(obj.event === 'domain_list'){   //域名列表
            layui_nav_each(get_domain_list,get_domain_list,data.username);

        }else if(obj.event === 'statistics'){    //统计
            layui_nav_each(admin_statistics_list,admin_statistics_list,data.username);

        }
        form.render();
    });

});


