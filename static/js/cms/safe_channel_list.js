var parent_href=window.parent.location.href;  //浏览器url
var parent_url=parent_href.split('=');
var cms_user='';  //融合客户账号/cms客户账号
var add='';        //添加
var add_channel=''; //添加频道
var domain_page='';
var domain_data='';   //data数据
var ajax_list='';  //页面列表
var page_list='';
var cols_domain=[];   //导航数据
var parent_sec_domain_list=''; //页面地址

if(parent_url.length>3){
    $('#customer_account').val(parent_url[parent_url.length-2]);
    $('#cms_id').val(parent_url[parent_url.length-1]);
}

if(layui_url=='/sec/admin_sec_domain_list/page/'){
    cms_user=cms_user_list;
    add='admin_get_cms_channel_list';
    add_channel='admin_create_sec_domain';
    ajax_list='admin_get_sec_domain_list';
    page_list='admin_parent_list';
    parent_sec_domain_list='/sec/admin_sec_domain_list/page/';
    cols_domain=[
           {field:'username',width:'10%',title: gettext('融合客户账号')}
          ,{field:'cms_username', width:'20%',title: gettext('CMS客户ID')}
          ,{field:'channel_name', width:'40%',title: gettext('安全频道名')}
          ,{field:'WAF', title: 'WAF',width:'10%',sort: true}
          ,{field:'list_button', width:'20%',title:gettext('操作'),toolbar: '#list_button'}
        ]
}else if(layui_url=='/sec/parent_sec_domain_list/page/'){
    parent_sec_domain_list='/sec/parent_sec_domain_list/page/';
    ajax_list='parent_get_sec_domain_list';
    cols_domain=[
      {field:'channel_name', title: gettext('安全频道名')}
      ,{field:'WAF', title: 'WAF',sort: true}
      ,{field:'list_button', title: gettext('操作'),toolbar: '#list_button'}
    ]
}

layui.use(['table','form','laypage'], function(){
    var form = layui.form;
    var table = layui.table;
    var layer = layui.layer;
    var count='';
    var curr="";

    window.data_search = function () {
        var customer_account=$('#customer_account').val();
        var cms_id=$('#cms_id').val();
        var channel_name=$('#channel_name').val();
        var laypage= $('.layui-laypage-curr em:nth-child(2)').text();
        if(laypage == ''){
           curr=1;
        }else{
           curr=laypage;
        }
        if(layui_url=='/sec/admin_sec_domain_list/page/'){     //用户
            domain_data={
                    id_or_username:customer_account,
                    cms_username:cms_id,
                    domain:channel_name,
                    page:curr,
                    csrfmiddlewaretoken: $.cookie('csrftoken')
            }
        }else if(layui_url=='/sec/parent_sec_domain_list/page/'){
            domain_data={
                    domain:channel_name,
                    page:curr,
                    csrfmiddlewaretoken: $.cookie('csrftoken')
            }

        }
        var table_list=[];
        $.ajax({
            type: "POST",
            url: '/sec/ajax/'+ajax_list+'/',
            data: domain_data,
            async:false,
            error: function () {
                lay_tips(gettext('通讯异常'));
            },
            success: function(res){
                // console.log(res)
                if(res.status==true){
                    table_list=res.domain_list;
                }else{
                    table_list=[];
                    res_msg(res);
                }
                res_table(res,table_list,curr);
                table.render({
                    elem: '#accounts_list'
                    ,data:table_list
                    ,cols: [cols_domain]
                    ,limit:10
                    , even: true //开启隔行背景
                    ,cellMinWidth: 80
                    ,done:function(){
                        data_waf();
                        $('.layui-none').text(gettext('通讯异常'));
                    }
                });
            }
        });
    };
    data_search();
    form.on('submit(search_channel)',function(){
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        data_search();
    })
    function data_waf(){ //表格排序
        var create_waf='<a class="layui-btn layui-btn-xs" lay-event="create_waf">'+gettext("开通WAF")+'</a>';
        var create_ing='<a class="layui-btn layui-btn-xs" lay-event="create_ing">'+gettext("创建中")+'</a>';
        if(is_staff ==  'True'){
            var create_fail='<a class="layui-btn layui-btn-xs" lay-event="create_fail">'+gettext("创建失败")+'</a>';
        }else{
            var create_fail='<a class="layui-btn layui-btn-xs" lay-event="create_fail">'+gettext("创建中")+'</a>';
        }
        var create_suc='<a class="layui-btn layui-btn-xs" lay-event="statistics">'+gettext("统计")+'</a><a class="layui-btn layui-btn-xs" lay-event="configure">'+gettext("配置")+'</a>';
        var alarm_mark='<div class="alarm_mark" style="padding-left: 5px;"><img src="/static/image/alarm_mark.png" /></div>';
        $("[data-field = 'WAF']").children().each(function(index){
            var this_find=$(this).parents('tr').find("[data-field = 'list_button'] div");
            if($(this).text() == '0'){
                $(this).html('');
                if(is_staff ==  'True'){
                    this_find.html(create_waf)
                }
            }else{
                if($(this).text() == '1' && is_staff ==  'True'){
                    this_find.html(create_ing)
                }else if($(this).text() == '2' && is_staff ==  'True'){
                    this_find.html(create_fail)
                }else if($(this).text() == '3'){
                    this_find.html(create_suc)
                }
                if(index>0){
                    $(this).html(alarm_mark);
                }
            }
        });
    }
    table.on('sort(parse-table-demo)', function(){  //表格排序
        data_waf();
    });

    table.on('tool(parse-table-demo)', function(obj){   //删除
        var data = obj.data;
        if(is_staff ==  'True'){
            if(obj.event === 'create_waf'){
                domain_page='admin_domain_waf_register';
            }else if(obj.event === 'statistics'){   //统计
                domain_page='admin_sec_overview';
            }else if(obj.event === 'configure'){   //配置
                if(data.WAF== 0){
                    domain_page='admin_domain_waf_register';
                }else{
                    domain_page='admin_sec_domain_conf';

                }
            }else if(obj.event === 'create_fail' || obj.event === 'create_ing'){
                domain_page='admin_domain_waf_conf_fail';

            }
        }else{
            if(obj.event === 'statistics'){       //用户统计
                domain_page='parent_sec_overview';
            }else if(obj.event === 'configure' ){    //用户配置
                domain_page='parent_sec_domain_conf';

            }else if(obj.event === 'create_fail' || obj.event === 'create_ing'){
                domain_page='parent_domain_waf_conf_fail';
            }
        }
        var this_data=data.channel_name;
        if(obj.event === 'create_fail' || obj.event === 'create_ing'){
            if(obj.event === 'create_ing'){
                var num='loading';
            }else{
                var num=404;
            }
            var url_upload='/sec/'+domain_page+'/page/';
            layui_nav_each(url_upload,parent_sec_domain_list,num,this_data);

        }else{
            var url_upload='/sec/'+domain_page+'/page/'+data.domain_id+'/';
            layui_nav_each(url_upload,parent_sec_domain_list,this_data);
        }


    });

    form.on('submit(lay_add)',function(){    //添加安全频道
        var cms_user_list='';
        for(var user in cms_user){
            var user=cms_user[user];
            if(user.has_create==true){
                cms_user_list+='<option value="'+user.user_id+'/'+user.cms_username+'">'+user.username+'/'+user.cms_username+'</option>';
            }else{
                cms_user_list+='<option value="'+user.user_id+'/'+user.cms_username+'">'+user.username+'/'+user.cms_username+'</option>';
            }

        }
        var cms_user_list='<option value=""></option>'+cms_user_list;
        var content='<div class="layui-form" style="padding:0 40px;">' +
            '     <div class="layui-form-item" style="text-align: left;">' +
            '           <select name="" id="cms_user_name" lay-filter="cms_user_name" lay-search>' +
            '               <option value="">'+gettext("融合客户账号/CMS客户ID")+'</option>' +cms_user_list+' </select>'+
            '     </div>' +
            '<div class="layui-form-item" id="channel_list" style="text-align: left;display: none;">' +
            '      <div class="layui-form-item" style="text-align: left;">' +
            '           <input type="text" value="" name="layui_cms_name" lay-filter="layui_cms_name" placeholder="'+gettext('频道名')+'">'+
            '           <button class="layui-btn layui-btn-blue " lay-filter="lay_search" style="margin-left:80px;" lay-submit >'+gettext('查询')+'</button>'+
            '      </div>' +
            '      <div class="check_box" id="lay_user_id" style="height:345px;">' +
            '      </div>'+
            '        <div class="layui-input-block" style="display: none;">' +
            '         <button class="checkBtn fl" lay-filter="button_layero" id="button_sub" ></button>' +
            '        </div>'+
            '     </div>'+
            '</div>';
        layer.open({
            type: 1
            ,title: gettext('添加安全频道')
            ,area: ['700px', '600px']
            ,btnAlign: 'l'
            ,shade:0
            ,btnAlign: 'c'
            ,id: 'tips_layer'
            ,content: content
            ,btn: [gettext('确定添加'),gettext('取消')]
            ,yes: function(index_ado){
                var channel_list={};
                var channel = document.getElementsByName('channel');
                for(var i=0;i<channel.length;i++){
                    if(channel[i].checked && channel[i].disabled != true){
                        channel_list[i]= {
                            'channel_id': '',
                            'channel_name': ''
                        };
                        channel_list[i].channel_id += channel[i].id;
                        channel_list[i].channel_name += channel[i].title;

                    }
                }
                var channel_arr=[];
                for (var i in channel_list) {
                    channel_arr.push(channel_list[i]);
                }
                var cms_user_name=$('#cms_user_name option:selected').val();
                var obj_value=cms_user_name.split('/');
                var channel_info_list = JSON.stringify(channel_arr);
                $.ajax({                                      //添加频道
                    type: "POST",
                    url: '/sec/ajax/'+add_channel+'/',
                    data: {
                        channel_info_list:channel_info_list,
                        user_id:obj_value[0],
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    },
                    dataType : 'json',
                    error:function(){
                        lay_tips(gettext('通讯异常'));
                    },
                    async:false,
                    success: function(res){
                        if(res.status){
                            parent.layer.close(index_ado);
                            window.location.reload();
                        }else{
                            if(res.msg !='' && res.msg != undefined){
                                lay_tips(res.msg);
                            }else{
                                lay_tips(gettext('通讯异常'));
                            }

                        }
                    }
                })
            }
        });

        form.on('select(cms_user_name)', function(obj){   //选择服务
            var obj_value=obj.value.split('/');
            $.ajax({
                type: "POST",
                url: '/sec/ajax/'+add+'/',
                data: {
                    cms_username:obj_value[1],
                    user_id:obj_value[0],
                    csrfmiddlewaretoken: $.cookie('csrftoken')
                },
                async:false,
                success: function(res){
                    $('#lay_user_id').html('');
                    $('#channel_list').hide();
                    if(res.status){
                        if(res.cms_channel_list !=''){
                            var cms_channel_list='';
                            var cms_channel=res.cms_channel_list;
                            var channel_name=[];
                            for(var channel in cms_channel){
                                    var channel=cms_channel[channel];
                                    if(channel.has_create==true){
                                        cms_channel_list+='<input id="'+channel.channel_id+'" checked disabled name="channel" type="checkbox" name="" title="'+channel.channel_name+'" lay-skin="primary" >';
                                    }else{
                                        cms_channel_list+='<input id="'+channel.channel_id+'" name="channel" type="checkbox" name="" title="'+channel.channel_name+'" lay-skin="primary" >';
                                    }
                                    channel_name.push(channel.channel_name);
                            }
                            $('#lay_user_id').html(cms_channel_list);
                            $('#channel_list').show();

                        }
                    }else{

                    }
                    form.render();

                }
            })
        });
        form.on('submit(lay_search)',function(){    //模糊查询客户
            var layui_cms_name=$('input[name="layui_cms_name"]').val();
            var storeId = document.getElementById('lay_user_id');
            fuzzy_search(layui_cms_name,storeId);
        });

        form.render();

    });

});