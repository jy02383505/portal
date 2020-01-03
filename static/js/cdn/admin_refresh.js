var page_list='';  //当前导航地址
var admin_cdn_domain_ajax='';  //提交刷新/预加载
var admin_cdn_domain_list_ajax=''; //刷新列表
if(layui_url=='/cdn/admin_refresh/page/'){     //管理员端刷新
    page_list='/cdn/admin_refresh/page/';
    admin_cdn_domain_ajax='/cdn/ajax/admin_cdn_domain_refresh/';
    admin_cdn_domain_list_ajax='/cdn/ajax/admin_cdn_domain_refresh_status/';
}else if(layui_url=='/cdn/admin_preload/page/'){    //管理员端预加载
    page_list='/cdn/admin_preload/page/';
    admin_cdn_domain_ajax='/cdn/ajax/admin_cdn_domain_preload/';
    admin_cdn_domain_list_ajax='/cdn/ajax/admin_cdn_domain_preload_status/';
}else if(layui_url=='/cdn/client_refresh/page/'){   //客户端刷新
    page_list='/cdn/client_refresh/page/';
    admin_cdn_domain_ajax='/cdn/ajax/client_cdn_domain_refresh/';
    admin_cdn_domain_list_ajax='/cdn/ajax/client_cdn_domain_refresh_status/';
}else if(layui_url=='/cdn/client_preload/page/'){    //客户端刷新
    page_list='/cdn/client_preload/page/';
    admin_cdn_domain_ajax='/cdn/ajax/client_cdn_domain_preload/';
    admin_cdn_domain_list_ajax='/cdn/ajax/client_cdn_domain_preload_status/';
}

if(layui_url=='/cdn/admin_preload/page/'){
    $('.search .layui-form-label').width(28)
    $('.search .layui-input-block').css('margin-left','38px');
}else if(layui_url=='/cdn/admin_refresh/page/' || layui_url=='/cdn/client_refresh/page/'){
    if(lan == 'en'){
        $('.search .layui-form-label').width(84)
        $('.search .layui-input-block').css('margin-left','94px');
    }else{
        $('.search .layui-form-label').width(56)
        $('.search .layui-input-block').css('margin-left','66px');
    }
}


if(layui_url=='/cdn/admin_refresh/page/' || layui_url=='/cdn/client_refresh/page/'){     //刷新
    var cols=[
          {type: 'checkbox',field: 'checkbox'}
          ,{field:'url',title:gettext('刷新记录')}
          ,{field:'start_time',width:150,title:gettext('刷新时间')}
          ,{field:'status',width:150,title:gettext('状态')}
        ]
}else if(layui_url=='/cdn/admin_preload/page/' || layui_url=='/cdn/client_preload/page/'){    //预加载
    var cols=[
          {type: 'checkbox',field: 'checkbox'}
          ,{field:'url',title:gettext('预加载记录')}
          ,{field:'start_time',width:150,title:gettext('预加载时间')}
          ,{field:'status',width:150,title:gettext('状态')}
        ]
}
var format = "YYYY-MM-DD";    //日历
var startDate;
var endDate;
endDate = moment();  //今天
var startTime = endDate.format(format);
var endTime = endDate.format(format);
$('#code_data').val(startTime + ' - ' + endTime);
$("#code_data").daterangepicker({
    format:'YYYY-MM-DD',
    todayBtn:true,
    //minDate:moment().subtract(90,'days'),
    maxDate : moment(),
    opens: 'left',
    timePicker: true,
    timePicker24Hour:true,
    timePickerIncrement : 5,
    dateLimit : {
       days : 7
    }, //起止时间的最大间隔
    locale:internation_trans.local ,
}).on('apply.daterangepicker', function(ev, picker) {

});

layui.use(['table','form','layer'], function() {
    var form = layui.form;
    var table = layui.table;
    var layer = layui.layer;
    var curr='';
    form.on('radio(opt_type)',function(data){   //
        if(data.value=='url'){
            $('#url_text_first').show();$('#url_text_last').hide();$('#url_text_last').val('');
        }else{
            $('#url_text_first').hide();$('#url_text_last').show();$('#url_text_first').val('');
        }
    });
    form.on('submit(lay_submit)',function(){
        console.log(user_id)
        var user_id=$('select[name="username"] option:selected').val();
        var opt_type=$('input[name="opt_type"]:checked').val();

        var file_url=$('#url_text_first').val();
        var catalog_url=$('#url_text_last').val();

        if(opt_type == 'url'){
            catalog_url='';
        }else if(opt_type == 'dir'){
            file_url=[];
        }
        if(user_id == ''){
            lay_tips(gettext('用户不能为空'));
            return;
        }else if(opt_type== ''){
            lay_tips(gettext('操作类型不能为空'));
            return;
        }else if(file_url=='' && catalog_url==''){
            lay_tips(gettext('域名不能为空'));
            return;
        }
        if(file_url != ''){
            file_url=file_url.split("\n");
        }
        if(catalog_url !=''){
            catalog_url=catalog_url.split("\n");
        }

        lower_hair(user_id,file_url,catalog_url);

    });
    function lower_hair(user_id,file_url,catalog_url){
        $.ajax({
            type: "POST",
            url: admin_cdn_domain_ajax,
            data: {
                user_id:user_id,
                urls:JSON.stringify(file_url),
                dirs:JSON.stringify(catalog_url),
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                console.log(res)
                if(res.status==true){
                    if(layui_url=='/cdn/admin_refresh/page/' || layui_url=='/cdn/client_refresh/page/'){     //刷新
                        lay_time(gettext('您的刷新请求已提交，预计将在10分钟内生效'))
                    }else if(layui_url=='/cdn/admin_preload/page/' || layui_url=='/cdn/client_preload/page/'){    //预加载
                        lay_time(gettext('您的预加载请求已提交，预计将在10分钟内生效'))
                    }
                    $('.layui-textarea').val('');
                    var laypage= $('.layui-laypage-curr em:nth-child(2)').text('1');
                    window.data_search();
                }else{
                    res_msg(res)
                }
            }
        });

    }

    form.on('submit(lay_query)',function(){
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        window.data_search();
    });

    window.data_search = function(){
        if(layui_url=='/cdn/admin_refresh/page/' || layui_url=='/cdn/admin_preload/page/') {
            var username=$('select[name="choice_user"] option:selected').text();
            if(username == gettext('请选择')){
                username='';
             }
        }else if(layui_url=='/cdn/client_refresh/page/' || layui_url=='/cdn/client_preload/page/'){
            var username='';
        }

        var opt_type=$('input[name="opt_type"]:checked').val();
        var refresh_url=$('input[name="refresh_url"]').val();

        var code_time=$('#code_data').val();
        if(code_time != ''){
            var start_sub=code_time.substring(0,10);
            var end_sub=code_time.substring(13,23);                            //结束时间

            var startTime=start_sub + ' 00:00:00';
            var endTime=end_sub + ' 23:59:59';
            var start_stamp = startTime.replace(/-/g,'/');
            var end_stamp = endTime.replace(/-/g,'/');

            var startTime = Date.parse(new Date(start_stamp));
            var endTime = Date.parse(new Date(end_stamp));
            var start_time = startTime / 1000;
            var end_time = endTime / 1000;
        }else{
            var start_time = '';
            var end_time = '';
        }

        var lay_status=$('select[name="lay_status"] option:selected').val();
        var laypage= $('.layui-laypage-curr em:nth-child(2)').text();
        if(laypage == ''){
           curr=1;
        }else{
           curr=laypage;
        }
        if(layui_url=='/cdn/admin_refresh/page/' || layui_url=='/cdn/client_refresh/page/'){     //管理员端域名列表
            var data={
                username:username,
                refresh_type:opt_type,
                url:refresh_url,
                start_time:start_time,
                end_time:end_time,
                type:lay_status,
                page:curr,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            }
        }else if(layui_url=='/cdn/admin_preload/page/' || layui_url=='/cdn/client_preload/page/'){
            var data={
                username:username,
                preload_status:opt_type,
                url:refresh_url,
                start_time:start_time,
                end_time:end_time,
                page:curr,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            }

        }
        var table_list=[];
        $.ajax({
            type: "POST",
            url: admin_cdn_domain_list_ajax,
            data: data,
            // async:false,
            success: function(res){
                console.log(res)
                if(res.status==true){
                    if(layui_url=='/cdn/admin_refresh/page/' || layui_url=='/cdn/client_refresh/page/'){
                        table_list=res.refresh_log_list;
                    }else if(layui_url=='/cdn/admin_preload/page/' || layui_url=='/cdn/client_preload/page/'){
                        table_list=res.preload_log_list;
                    }

                }else{
                    table_list=[];
                    // res_msg(res);
                }
                res_table(res,table_list,curr);
                table.render({
                    elem: '#lay_table'
                    ,toolbar: '#toolbar_table'
                    ,defaultToolbar: []
                    ,data:table_list
                    ,cols: [cols]
                    ,limit:10
                    ,even: true //开启隔行背景
                    ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
                    ,done:function(){
                        $('.layui-none').text(gettext('暂无数据'));
                        if(layui_url=='/cdn/admin_refresh/page/' || layui_url=='/cdn/client_refresh/page/'){
                            var status_array=refresh_status;
                        }else if(layui_url=='/cdn/admin_preload/page/' || layui_url=='/cdn/client_preload/page/'){
                            var status_array=preload_status;
                        }
                        $("[data-field = 'status']").children().each(function(){
                            var status_text=$(this).text();
                            for(var status in status_array){
                                var status=status_array[status];
                                if(status.id == status_text){
                                    $(this).text(gettext(status.name))
                                }
                            }
                        });
                    }
                });
                table.render();
            }
        });
    };
    data_search();

    table.on('toolbar(lay_table)', function(obj){
        var checkStatus = table.checkStatus(obj.config.id);
        var data = checkStatus.data;
        if(data == ''){
            return;
        }
        var data_status_array=0;
        switch(obj.event){
            case 'lay_reset':                      //重置
            var data_url=[];
            var data_dir=[];
            for(var data_status in data){
                var data_status=data[data_status];
                console.log(data_status)
                if(data_status.status == 2){
                    if(data_status.type=='url'){
                        data_url.push(data_status.url);

                    }else if(data_status.type=='dir'){
                        data_dir.push(data_status.url);
                    }else if(layui_url=='/cdn/admin_preload/page/' || layui_url=='/cdn/client_preload/page/'){
                        data_url.push(data_status.url);
                    }
                }else if(data_status.status != 2){
                    data_status_array ++;
                }
            }
            console.log(data_status_array)
            if(data_status_array != 0){
                var lay_tips_text=gettext('重置任务操作只能作用于“失败”状态的域名，请重新选择。');
                lay_tips(lay_tips_text);
                return;
            }

            var username=$('select[name="choice_user"] option:selected').val();
            layer.alert(gettext('确定重新下发当前选中域名？'), {
              title:gettext('重置任务'),
              icon: 0,
              shade:0,
              skin:'skin_icon',
              area:['500px','200px'],
              btn:[gettext('确定'),gettext('取消')],
              btnAlign:'l',
              // skin: 'layer-ext-moon', //该皮肤由layer.seaning.com友情扩展。关于皮肤的扩展规则，去这里查阅
              yes:function() {
                  lower_hair(username,data_url,data_dir); // 重新下发
              }
            });
          break;
        }
    });

    form.render();
});


