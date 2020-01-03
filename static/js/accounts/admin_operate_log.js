if(layui_url=='/base/admin_parent_opt_log/page/'){   //用户操作日志
    var admin_log_list='/base/ajax/admin_get_parent_opt_log_list/';
}else if(layui_url=='/base/admin_admin_opt_log/page/'){   //管理员操作日志
    var admin_log_list='/base/ajax/admin_get_admin_opt_log_list/';
}

if(parent_split.length>3){
    $('#username').val(parent_split[parent_split.length-1])
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
    window.data_search()
});

layui.use(['table','laydate','form'], function(){
    var table = layui.table;
    var form = layui.form;
    var laydate = layui.laydate;
    //日期范围
    var curr=0;

    window.data_search = function () {
       var username=$('#username').val();
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
      $.ajax({
        type: "POST",
        url: admin_log_list,
        data: {
            username:username,
            start_time:start_time,
            end_time:end_time,
            page:curr,
            csrfmiddlewaretoken: $.cookie('csrftoken')
        },
        async:false,
        success: function(res){
            var table_list=[];
            if(res.status==true){
                table_list=res.log_list;
            }else{
                table_list=[];
                res_msg(res);
            }
            res_table(res,table_list,curr);

            table.render({
                elem: '#accounts_list'
                ,data:table_list
                ,cols: [[
                  {field:'add_time',title:gettext('操作时间')}
                  ,{field:'user',title:gettext('用户名')}
                  ,{field:'info', title: gettext('操作记录')}
                ]]
                ,limit:10
                , even: true //开启隔行背景
                ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
                ,done:function(){
                    $("[data-field = 'is_active']").children().each(function(){
                        if($(this).text() == 'true'){
                          $(this).text(gettext('启用'));
                        }else if($(this).text() == 'false'){
                           $(this).text(gettext('禁用'));
                        }
                    });
                    $("[data-field = 'info']").children().each(function(){
                         $(this).text(gettext($(this).text()));
                    });
                     $('.layui-none').text(gettext('暂无数据'));
                }
            });
            table.render();
        }
      });
    }

    data_search();
    form.on('select(username)', function(){
       $('.layui-laypage-curr em:nth-child(2)').text('1');
       data_search();
    });
    $('.search_user').click(function(){
        $('.layui-laypage-curr em:nth-child(2)').text('1');
        data_search();
    });

    laydate.render({
       max:0
      ,type: 'date'
      ,range: true
      ,elem: '#time'
      ,ready:function(){
          $('.laydate-btns-confirm').click(function(){
              data_search();
          })

      }
    });
});


