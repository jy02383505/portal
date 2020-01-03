var page_list='';  //当前导航地址
var domain_list_ajax='';  //域名列表
var add_domain_list='';  //添加域名
var domain_configure_list=''; // 配置
var admin_statistics_list=''; // 统计
var domain_name_status_ajax='';  //域名状态
if(layui_url == '/cdn/admin_get_domain_list/page/') {     //管理员端域名列表
    page_list = '/cdn/admin_get_domain_list/page/';
    domain_list_ajax = '/cdn/ajax/admin_get_domain_list/';
    add_domain_list = '/cdn/admin_cdn_create_domain_views/page/';
    domain_configure_list = '/cdn/modify_admin_domain_configure/page/';   //配置
    admin_statistics_list = '/cdn/admin_statistics/page/'; // 统计
    domain_name_status_ajax = '/cdn/ajax/admin_cdn_domain_active/';
    var cols = [
        {type: 'checkbox',event: 'checkbox' ,width: 40,field: 'checkbox'}
        , {field: 'domain', title: gettext('域名')}
        , {field: 'username', width: 120,title: gettext('用户')}
        , {field: 'cdn_type', title: gettext('加速类型')}
        // ,{field:'cdn_type',width:100,title:gettext('协议类型')}
        , {field: 'cname', title: 'CNAME'}
        , {field: 'status',  width: 134,title: gettext('状态')}
        , {field: 'task_progress', width: 140,title: gettext('任务进度')}
        , {field: 'list_button',  title: gettext('操作'), toolbar: '#list_button'}
    ]

}else if(layui_url == '/cdn/client_get_domain_list/page/'){
    page_list = '/cdn/client_get_domain_list/page/';
    domain_list_ajax = '/cdn/ajax/client_get_domain_list/';
    add_domain_list = '/cdn/client_cdn_create_domain/page/';
    domain_name_status_ajax = '/cdn/ajax/client_cdn_domain_active/';
    domain_configure_list = '/cdn/modify_client_domain_configure/page/';   //配置
    admin_statistics_list = '/cdn/client_statistics/page/'; // 统计
    var cols = [
        {field: 'domain',width: 260, title: gettext('域名')}
        , {field: 'cdn_type', width: 180, title: gettext('加速类型')}
        , {field: 'cname', title: 'CNAME'}
        , {field: 'status', width: 160, title: gettext('状态')}
        , {field: 'list_button', width: 260, title: gettext('操作'), toolbar: '#list_button'}
    ]
}
if(parent_split.length>3){
    var user_name=parent_split[parent_split.length-1];   //用户
    $('select[name="username"] option').each(function(){
        if($(this).text()==user_name){
            $(this).attr('selected','selected');
        }
    })

}
var domain_status_list='';    //状态

for(var status_name in domain_status){
    var status_name=domain_status[status_name];
    var status_id=status_name.id;
    var status_data=[];
    for(var status_in in status_id){
        status_data.push(status_id[status_in]);
    }

    domain_status_list += '<option value="'+status_data+'">'+gettext(status_name.name)+'</option>';
}

$('select[name="domain_status"] option:nth-child(2)').after(domain_status_list);

layui.use(['table','form','layer','laypage'], function(){
    var form = layui.form;
    var table = layui.table;
    var layer = layui.layer;
    var laypage = layui.laypage;
    var count='';
    var curr="";

    $('.search_user').click(function(){   //输入域名查询
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        data_search();
    });
    form.on('select(username)',function(){   //选择用户
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        data_search();
    });
    form.on('select(acceleration_type)',function(){   //选择加速类型
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        data_search();
    });
    form.on('select(domain_status)',function(){    //选择状态
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        data_search();
    });
    form.on('submit(add_domain)',function(){   //添加域名
        if(is_staff == 'True'){
            layui_nav_each(add_domain_list,page_list);
        }else{
            if(contract == '' || contract == undefined){
                lay_tips(gettext('您账号下的CDN合同已到期，暂时无法创建新的域名'))
            }else{
                layui_nav_each(add_domain_list,page_list);
            }
        }

    });
    window.data_search = function(){
        var domain=$('input[name="domain_input"]').val();
        var user_id=$('select[name="username"] option:selected').val();
        var cdn_type=$('select[name="acceleration_type"] option:selected').val();
        var protocol=$('select[name="protocol_type"] option:selected').val();
        var domain_status=$('select[name="domain_status"] option:selected').val();
        var laypage= $('.layui-laypage-curr em:nth-child(2)').text();
        if(laypage == ''){
           curr=1;
        }else{
           curr=laypage;
        }
        var status=domain_status.split(',');
        var table_list=[];
        $.ajax({
            type: "POST",
            url: domain_list_ajax,
            data: {
                domain:domain,
                user_id:user_id,
                protocol:protocol,
                cdn_type:cdn_type,
                domain_status:JSON.stringify(status),
                page:curr,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            // async:false,
            success: function(res){
                if(res.status==true){
                    table_list=res.domain_list;
                }else{
                    table_list=[];
                    res_msg(res);
                }
                res_table(res,table_list,curr);
                table.render({
                    elem: '#domain_list'
                    ,toolbar: '#toolbar_table'
                    ,defaultToolbar: []
                    ,data:table_list
                    ,cols: [cols]
                    ,limit:10
                    ,even: true //开启隔行背景
                    ,cellMinWidth: 80
                    ,done:function() {

                        var tips_span = '<span class="hover_span" style="padding-left: 3px;"><i class="layui-icon layui-icon-help" style=""></i>' +
                            '<span class="remarks_span">' + gettext('设备任务下发进度，如任务进度长时间停滞，或域名仍于配置中状态，请联系平台运维处理') + '</span></span>';
                        $("[data-field = 'task_progress']").children().each(function (index) {   //状态转换
                            if (index > 0) {
                                var task_progress = new Number($(this).text());
                                var progress = Math.floor(task_progress * 100) / 100;
                                $(this).text(progress + '%');
                            } else {
                                $(this).append(tips_span);
                            }
                        });
                        $(".layui-icon-help").hover(function () {
                            $(this).parent().find('.remarks_span').show();
                        }, function () {
                            $(this).parent().find('.remarks_span').hide();
                        });
                        $("[data-field = 'cdn_type']").children().each(function () {   //状态转换
                            $(this).text(gettext($(this).text()))
                        })

                        if (user_perm != '') {
                            for (var user in user_perm) {
                                $("[data-field = 'status']").children().each(function () {   //状态转换
                                    $(this).text(gettext($(this).text()))
                                    if ('client_cdn_create_domain' == user_perm[user]) {
                                        if (layui_url == '/cdn/client_get_domain_list/page/') {

                                            if ($(this).text() == gettext('已启动')) {
                                                $(this).parents('tr').find("[data-field = 'list_button']").children().append('<a class="layui-btn layui-btn-xs layui_status" lay-event="close_status">' + gettext('关闭') + '</a>');
                                            } else if ($(this).text() == gettext('已关闭')) {
                                                $(this).parents('tr').find("[data-field = 'list_button']").children().append('<a class="layui-btn layui-btn-xs layui_status" lay-event="open_status">' + gettext('启动') + '</a>');
                                            }
                                        }
                                    }
                                });



                            }
                        }
                        $('.layui-none').text(gettext('暂无数据'));
                    }
                });
                table.render();
            }
        });

    };

    data_search();

    table.on('tool(lay_domain)', function(obj){   //操作列
        var data=obj.data;
        var domain=[data.domain]
        if(obj.event=='cdn_configure'){
            var url_upload=domain_configure_list+data.id+'/';
            layui_nav_each(url_upload,page_list);
        }else if(obj.event=='statistics'){
            // var url_upload=admin_statistics_list+data.id+'/';
            layui_nav_each(admin_statistics_list,admin_statistics_list,data.user_id,data.domain);
        }else if(obj.event=='close_status'){
            domain_name_status_ajax='/cdn/ajax/client_cdn_domain_disable/';

            var lay_cont=gettext('确定关闭当前选中域名正在使用的CDN服务？')+'<p style="font-size: 12px;">'+gettext('关闭后的域名配置会保留（下次开启时无需再次配置），但不会继续提供加速服务。')+'</p>';
            var lay_title=gettext('关闭CDN');
            lay_domain_ope(lay_title,lay_cont,domain_name_status_ajax,data.user_id,domain);

        }else if(obj.event=='open_status'){
            var lay_cont=gettext('确定启动当前选中域名正在使用的CDN服务？');
            var lay_title=gettext('启动CDN');
            lay_domain_ope(lay_title,lay_cont,domain_name_status_ajax,data.user_id,domain);

        }else if(obj.event=='checkbox'){

            var table_checked=document.getElementsByName('layTableCheckbox');

            var checked_length=0
            for(var i=0;i<table_checked.length;i++){
                if(table_checked[i].checked){
                    checked_length++;
                }
            }

            if(checked_length != 0){
                $('.layui_status').removeClass('layui-btn-gray');
                $('.layui_status').prop('disabled',false);
            }else{
                $('.layui_status').addClass('layui-btn-gray');
                $('.layui_status').attr('disabled',true);
            }


        }
    });

    table.on('toolbar(lay_domain)', function(obj){   //列表工具栏

        var checkStatus = table.checkStatus(obj.config.id);
        var data = checkStatus.data;
        if(data == ''){
            return;
        }
        var data_status_array=0;
        var data_user_array=[];   //用户id
        var domain=[];

        //域名不属于同一用户
        var lay_cont=gettext('请选择从属于同一用户下的域名')+'<p style="font-size: 12px;">'+gettext('目前不支持同时删除多个用户账号下的域名，请重新选择')+'</p>';
        var lay_title=gettext('启动/关闭CDN');
        switch(obj.event){
            case 'open_domain':                      //启动
            for(var data_status in data){
                var data_status=data[data_status];
                if(data_status.status != '已关闭'){
                    data_status_array ++;
                }else{
                    domain.push(data_status.domain);
                }
                if (data_user_array.indexOf(data_status.user_id) ===-1){
                    data_user_array.push(data_status.user_id)
                }
            }

            if(data_user_array.length != 1){   //域名不属于同一用户
                lay_tips_second(lay_cont,lay_title);
                return;
            }
            if(data_status_array != 0){
                var lay_tips_text=gettext('启动操作只能作用于“已关闭”状态的域名，请重新选择。');
                lay_tips(lay_tips_text);
                return;
            }

            // layer.alert(JSON.stringify(data));
            var lay_cont=gettext('确定启动当前选中域名正在使用的CDN服务？');
            var lay_title=gettext('启动CDN');
            lay_domain_ope(lay_title,lay_cont,domain_name_status_ajax,data_user_array[0],domain);
          break;

          case 'close_domain':                //关闭
            domain_name_status_ajax='/cdn/ajax/admin_cdn_domain_disable/';
            for(var data_status in data){
                var data_status=data[data_status];
                if(data_status.status != '已启动'){
                    data_status_array ++;
                }else{
                    domain.push(data_status.domain);
                }
                if (data_user_array.indexOf(data_status.user_id) ===-1){
                    data_user_array.push(data_status.user_id)
                }
            }
            if(data_user_array.length != 1){  //域名不属于同一用户
                lay_tips_second(lay_cont,lay_title);
                return;
            }
            if(data_status_array != 0){
                var lay_tips_text=gettext('关闭操作只能作用于“已启动”状态的域名，请重新选择。');
                lay_tips(lay_tips_text);
                return;
            }
            var lay_cont=gettext('确定关闭当前选中域名正在使用的CDN服务？')+'<p style="font-size: 12px;">'+gettext('关闭后的域名配置会保留（下次开启时无需再次配置），但不会继续提供加速服务。')+'</p>';
            var lay_title=gettext('关闭CDN');
            lay_domain_ope(lay_title,lay_cont,domain_name_status_ajax,data_user_array[0],domain);
          break;
        }
    });

    var lay_domain_ope =function(lay_title,lay_cont,domain_name_status_ajax,user_id,domain){    //域名开启关闭操作
        top.layer.alert(lay_cont, {
          title:lay_title,
          icon: 0,
          shade:0,
          offset:'auto',
          area:['500px','230px'],
          btn:[gettext('确定'),gettext('取消')],
          btnAlign:'c',
          yes:function(index) {
              lay_load(); // 加载
              $.ajax({
                  type: "POST",
                  url: domain_name_status_ajax,
                  data: {
                      user_id: user_id,
                      domain: JSON.stringify(domain),
                      csrfmiddlewaretoken: $.cookie('csrftoken')
                  },
                  error: function () {
                      lay_tips(gettext('通讯异常'));
                  },
                  success: function (res) {
                      parent.layer.closeAll();
                      if (res.status) {
                          top.layer.close(index);
                          window.data_search();
                      } else {
                          res_msg(res);
                      }

                  }
              })
          }
        });
    };
});

