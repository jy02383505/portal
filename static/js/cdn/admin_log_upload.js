var page_list='';  //当前导航地址
var admin_cdn_domain_ajax=''; //日志列表
var cols=[
      {field:'time',title:gettext('日志时间')}
      ,{field:'download_url',title:gettext('日志文件名')}
      ,{field:'list_button', title: gettext('操作'),toolbar: '#list_button'}
    ]
if(layui_url=='/cdn/admin_log_upload/page/'){     //管理员端日志下载
    page_list='/cdn/admin_log_upload/page/';
    admin_cdn_domain_ajax='/cdn/ajax/admin_cdn_domain_log_list/';
}else if(layui_url=='/cdn/client_log_upload/page/'){
    page_list='/cdn/client_log_upload/page/';
    admin_cdn_domain_ajax='/cdn/ajax/client_cdn_domain_log_list/';
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
    timePicker12Hour:false,
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
    form.on('select(choice_user)',function(data){  //切换用户
        var domain_list='';
        for(var user_array in user_list){
            var user_array=user_list[user_array];
            if(data.value == user_array.id){
                var domain_array=user_array.domain_list;
                for(var domain in domain_array){
                    domain_list += '<option value="'+domain_array[domain]+'">'+domain_array[domain]+'</option>'
                }
            }

        }
        $('select[name="choice_domain"]').html('<option value="">'+gettext('请选择')+'</option>'+domain_list);
        form.render();
    });

    form.on('submit(lay_query)',function(){ //列表查询
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        window.data_search();
    });

    window.data_search = function(){
        if(layui_url=='/cdn/admin_log_upload/page/') {
            var user_id=$('select[name="choice_user"] option:selected').val();
        }else if(layui_url=='/cdn/client_log_upload/page/'){
            var user_id='';
        }
        // var user_id=$('select[name="choice_user"] option:selected').val();
        var choice_domain=$('select[name="choice_domain"] option:selected').val();
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

        var laypage= $('.layui-laypage-curr em:nth-child(2)').text();
        if(laypage == ''){
           curr=1;
        }else{
           curr=laypage;
        }
        var table_list=[];
        $.ajax({
            type: "POST",
            url: admin_cdn_domain_ajax,
            data: {
                user_id:user_id,
                domain:choice_domain,
                start_time:start_time,
                end_time:end_time,
                page:curr,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                if(res.status==true){
                    table_list=res.log_list;
                }else{
                    table_list=[];
                    // res_msg(res);
                }
                res_table(res,table_list,curr);
            }
        });
        table.render({
            elem: '#lay_table'
            ,data:table_list
            ,cols: [cols]
            ,limit:10
            ,even: true //开启隔行背景
            ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
            ,done:function(){
                $('[data-field="download_url"]').children().each(function(){  //文件名处理
                    var this_url=$(this).text().split('=');
                    $(this).text(this_url[1]);
                });
                /*$('[data-field="time"]').children().each(function(index){    //时间处理
                    if(index>0){
                        var this_time=$(this).text();
                        var year=this_time.substring(0,4),month=this_time.substring(4,6),data=this_time.substring(6,8),hour=data=this_time.substring(8,10);
                        $(this).text(year+'-'+month+'-'+data+' '+hour+':00:00');
                    }
                });*/
                $('.layui-none').text(gettext('暂无数据'));
            }
        });

        table.render();
    };
    data_search();

    table.on('tool(lay_table)', function(obj){   //下载
        var data = obj.data;
        if(obj.event === 'upload'){   //
            window.location.href=data.download_url;
        }
    });

});
