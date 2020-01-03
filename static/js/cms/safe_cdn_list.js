var parent_href=window.parent.location.href;  //浏览器url
var parent_url=parent_href.split('=');

var ajax_list='';  //页面列表
var channel_list=''; //跳转到频道列
var configure_list='';//安全服务配置页面
var cms_user='';  //融合客户账号/cms客户账号
var add_accounts_ajax='';//添加安全客户接口
if(parent_oblique[2]=='admin_sec_user_list' || parent_split.length==1){
    ajax_list='admin_sec_user_list';
    channel_list='admin_sec_domain_list';
    configure_list='admin_set_user_strategy';
    add_accounts_ajax='/sec/ajax/admin_create_sec_user/';
    cms_user=cms_user_list;
    var cols=[
          {field:'username',width:'15%', title:'安全客户账号'}
          ,{field:'cms_username', width:'15%', title: 'CMS客户ID'}
          ,{field:'cms_status',width:'15%', title:'CMS客户状态',sort: true}
          ,{field:'domain_num', width:'15%',event:'domain_num', title: '安全频道',style:'cursor: pointer;color:#2c80e3;'}
          ,{field:'list_button', width:'40%', title: '操作',toolbar: '#list_button'}
        ]
}

layui.use(['table','form','laypage'], function(){
   var form = layui.form;
   var table = layui.table;
   var layer = layui.layer;
   var curr="";
   window.data_search = function () {
        var id_or_username=$('#id_or_username').val();
        var cms_username=$('#cms_username').val();
        var laypage= $('.layui-laypage-curr em:nth-child(2)').text();
        if(laypage == ''){
           curr=1;
        }else{
           curr=laypage;
        }
        var table_list=[]
        $.ajax({
            type: "POST",
            url: '/sec/ajax/'+ajax_list+'/',
            data: {
                id_or_username:id_or_username,
                cms_username:cms_username,
                page:curr,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                if(res.status==true){
                    table_list=res.sec_user_list;
                }else{
                    table_list=[];
                    res_msg(res);
                }
                res_table(res,table_list,curr);

                table.render({
                    elem: '#admin_sec_user_list'
                    ,data:table_list
                    ,cols: [cols]
                    ,limit:10
                    , even: true //开启隔行背景
                    ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
                    ,done:function(res){
                        $("[data-field = 'is_active']").children().each(function(){
                            if($(this).text() == 'true'){
                              $(this).text("启用");
                            }else if($(this).text() == 'false'){
                               $(this).text("禁用");
                            }
                        });
                    }
              });
              table.render();
            }
        });
    };
    data_search();
    form.on('submit(search_pro)',function(){
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        data_search();
    })
    form.on('submit(lay_add)',function(){    //添加安全客户
        var content='<div class="layui-form" id="add_jurisdiction" style="padding:0 40px;">' +
            '     <div class="layui-form-item">' +
            '      <p class="title_p">'+gettext('选择客户')+'</p>' +
            '      <p class="title_p blue">'+gettext('显示方式：融合客户账号 / CMS客户ID')+'</p>' +
            '     </div>' +
            '     <div class="layui-form-item" style="text-align: left;">' +
            '           <input type="text" value="" name="layui_cms_name" lay-filter="layui_cms_name" placeholder="'+gettext('客户账号 /  CMS客户ID')+'">'+
            '           <button class="layui-btn layui-btn-blue " lay-filter="lay_search" style="margin-left:80px;" lay-submit >'+gettext('查询')+'</button>'+
            '     </div>' +
            '     <div class="layui-form-item" style="text-align: left;">' +
            '      <div class="check_box" id="lay_user_id">' +
            '      </div>'+
            '        <div class="layui-input-block" style="display: none;">' +
            '         <button class="checkBtn fl" lay-filter="button_layero" id="button_sub" ></button>' +
            '        </div>'+
            '     </div>'+
            '</div>';
        layer.open({
            type: 1
            ,title: gettext('添加安全客户')
            ,area: ['600px', '600px']
            ,btnAlign: 'l'
            ,shade:0
            ,btnAlign: 'c'
            ,id: 'tips_layer'
            ,content: content
            ,btn: [gettext('确定添加'),gettext('取消')]
            ,yes: function(index_ado){
                var user_id=[];
                var cms_user = document.getElementsByName('cms_user');
                for(var i=0;i<cms_user.length;i++){
                    if(cms_user[i].checked && cms_user[i].value=='0'){
                        console.log(cms_user[i].id);
                        user_id.push(cms_user[i].id);
                    }
                }
                $.ajax({
                    type: "POST",
                    url: add_accounts_ajax,
                    data: {
                        user_ids:user_id,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    },
                    async:false,
                    success: function(res){
                        console.log(res);
                        if(res.status){
                            layer.close(index_ado);
                            window.location.reload();
                        }else{
                            lay_tips(res.msg);
                        }

                    }
                })

            }
        });
        var cms_user_list='';   //客户数据
        var channel_name=[];
        for(var cms in cms_user){
                var cms=cms_user[cms];
                if(cms.is_sec==1){
                    cms_user_list+='<input id="'+cms.user_id+'" value="'+cms.is_sec+'" checked disabled name="cms_user" type="checkbox" name="" title="'+cms.username+'/'+cms.cms_username+'" lay-skin="primary" >';
                }else{
                    cms_user_list+='<input id="'+cms.user_id+'" value="'+cms.is_sec+'" name="cms_user" type="checkbox" name="" title="'+cms.username+'/'+cms.cms_username+'" lay-skin="primary" >';
                }
                channel_name.push(cms_user.username);
        }
        $('#lay_user_id').html(cms_user_list);

        form.on('submit(lay_search)',function(){    //模糊查询客户
            var layui_cms_name=$('input[name="layui_cms_name"]').val();
            var storeId = document.getElementById('lay_user_id');
            fuzzy_search(layui_cms_name,storeId);
        });

        form.render();
    });

    table.on('tool(admin_sec_user_list)', function(obj){   //安全列表交互
        var data = obj.data;
        if(obj.event === 'domain_num'){   //安全频道
            var this_data=data.username+'='+data.cms_username;
            var url_upload='/sec/'+channel_list+'/page/';
            layui_nav_each(url_upload,url_upload,this_data);

        }else if(obj.event === 'configure'){
            var this_data=data.username;
            var url_upload='/base/'+configure_list+'/page/'+data.user_id+'/';
            layui_nav_each(url_upload,'/sec/'+ajax_list+'/page/',this_data);
        }
        form.render();
    });

    form.render();
});


