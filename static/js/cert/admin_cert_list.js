var page_list='';    //导航
var add_cert='';        //添加证书
var admin_cert_list_ajax='';  //列表
var details='';   //详情
var update='';   //更新
var del_ajax='';  //删除
var cert_status_array=cert_status;

if(layui_url=='/cert/admin_cert_ssl_manage/page/'){     //用户
    page_list='/cert/admin_cert_ssl_manage/page/';
    add_cert='/cert/admin_cert_create/page/';
    admin_cert_list_ajax='/cert/ajax/admin_cert_list/';
    details='/cert/admin_cert_detail/page/';
    update='/cert/admin_cert_edit/page/';
    del_ajax='/cert/ajax/admin_cert_delete/';
    var cols=[        //证书表头
          {field:'cert_name',title:gettext('证书名称'),event: 'username'}
          ,{field:'username',title:gettext('用户')}
          ,{field:'cert_from',title:gettext('证书来源')}
          ,{field:'start_time',title:gettext('颁发时间')}
          ,{field:'end_time',title:gettext('到期时间')}
          ,{field:'status', title: gettext('证书状态')}
          ,{field:'list_button', title: gettext('操作'),toolbar: '#list_button'}
        ]

}else if(layui_url=='/cert/client_cert_ssl_manage/page/'){
    page_list='/cert/client_cert_ssl_manage/page/';
    add_cert='/cert/client_cert_create/page/';
    admin_cert_list_ajax='/cert/ajax/client_cert_list/';
    details='/cert/client_cert_detail/page/';
    update='/cert/client_cert_edit/page/';
    del_ajax='/cert/ajax/client_cert_delete/';
    var cols=[        //证书表头
          {field:'cert_name',title:gettext('证书名称'),event: 'username'}
          ,{field:'cert_from',title:gettext('证书来源')}
          ,{field:'start_time',width:140,title:gettext('颁发时间')}
          ,{field:'end_time',width:140,title:gettext('到期时间')}
          ,{field:'status', title: gettext('证书状态')}
          ,{field:'list_button', title: gettext('操作'),toolbar: '#list_button'}
        ]

}
var domain_status_list='';    //状态
for(var status_name in cert_status){
    var status_name=cert_status[status_name];
    var status_id=status_name.id;
    var status_data=[];
    for(var status_in in status_id){
        status_data.push(status_id[status_in]);
    }

    domain_status_list += '<option value="'+status_data+'">'+gettext(status_name.name)+'</option>';
}
$('select[name="cert_status"] option:nth-child(2)').after(domain_status_list);
layui.use(['table','form','laypage'], function(){
   var form = layui.form;
   var table = layui.table;
   var curr="";
   form.on('submit(add_cert)',function(){
        layui_nav_each(add_cert,page_list);
   });
    window.data_search = function () {
        var table_list=[];
        var cert=$('#cert').val();
        var username=$('select[name="username"] option:selected').val();
        var cert_status=$('select[name="cert_status"] option:selected').val();
        var laypage= $('.layui-laypage-curr em:nth-child(2)').text();
        if(laypage == ''){
           curr=1;
        }else{
           curr=laypage;
        }
        var status=cert_status.split(',');
        console.log(admin_cert_list_ajax)
        $.ajax({
            type: "POST",
            url: admin_cert_list_ajax,
            data: {
                cert_name:cert,
                user_id:username,
                status:JSON.stringify(status),
                page:curr,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                if(res.status==true){
                    table_list=res.cert_list;
                }else{
                    table_list=[];
                    res_msg(res);
                }
                res_table(res,table_list,curr);
            }
        });
        table.render({
            elem: '#accounts_list'
            ,data:table_list
            ,cols: [cols]
            ,limit:10
            , even: true
            ,cellMinWidth: 80
            ,done:function(){
                $('.layui-none').text(gettext('暂无数据'));
                $("[data-field = 'status']").children().each(function(){   //状态转换
                    for(var cert_status in cert_status_array){
                        var cert_status=cert_status_array[cert_status]
                        var cert_id=cert_status.id;
                        for(var i=0;i<cert_id.length;i++){
                            if(cert_id[i]==$(this).text()){
                                $(this).text(gettext(cert_status.name));
                            }
                        }

                    }
                });
                $("[data-field = 'cert_from']").children().each(function(){   //状态转换
                    for(var cert in cert_from){
                        var cert=cert_from[cert];
                        if(cert.id==$(this).text()){
                            $(this).text(gettext(cert.name));
                        }

                    }

                });

            }
        });
        table.render();
    };

    data_search();
    $('.search_user').click(function(){
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        data_search();
    });
    form.on('select(username)', function(){
       $('.layui-laypage-curr em:nth-child(2)').text('1');
       data_search();
    });
    form.on('select(cert_status)', function(){
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        data_search();
    });

    table.on('tool(lay_table)', function(obj){   //用户详情
        var data = obj.data;
        console.log(data);
        if(obj.event === 'details'){   //
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