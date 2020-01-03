// var page_list='';  //当前导航地址
var admin_statistics_ajax='';  //流量数据查询
var admin_cdn_request_ajax='';  //请求量
var admin_status_code_ajax='';  //状态码数据查询
var bandwidth_data_upload_ajax='';   //详细带宽数据   下载
var state_data_upload_ajax='';    //状态码数据   下载
var code_data_upload_ajax='';   //状态码趋势数据   下载

if(layui_url == '/cdn/client_cdn_overview/page/'){
/*    admin_statistics_ajax='/cdn/ajax/client_cdn_overview/';*/
    admin_statistics_ajax='/cdn/ajax/client_cdn_flux_data/';      //流量数据
    admin_cdn_request_ajax='/cdn/ajax/client_cdn_request_data/';   //请求量
    bandwidth_data_upload_ajax='/cdn/ajax/client_download_cdn_flux/';   //详细带宽数据   下载
    $('#overview_time').show();
}else if(layui_url == '/cdn/client_statistics/page/'){
    admin_statistics_ajax='/cdn/ajax/client_cdn_flux_data/';      //流量数据
    admin_cdn_request_ajax='/cdn/ajax/client_cdn_request_data/';   //请求量
    admin_status_code_ajax='/cdn/ajax/client_cdn_status_code_data/';   //状态码
    bandwidth_data_upload_ajax='/cdn/ajax/client_download_cdn_flux/';   //详细带宽数据   下载
    state_data_upload_ajax='/cdn/ajax/client_download_status_code/';    //状态码数据   下载
    code_data_upload_ajax='/cdn/ajax/client_download_status_code_trend/';   //状态码趋势数据   下载
    var cols_trend=[
      {field:'code',title:gettext('状态码')}
      ,{field:'num',title:gettext('总数')}
      ,{field:'ratio',title:gettext('百分比')}
    ];

var cols_all_trend=[
      {field:'code',title:gettext('状态码')}
      ,{field:'count',title:gettext('总数')}
      ,{field:'ratio',title:gettext('百分比')}
    ];
}else if(layui_url == '/cdn/admin_statistics/page/'){

    admin_statistics_ajax='/cdn/ajax/admin_cdn_flux_data/';
    admin_cdn_request_ajax='/cdn/ajax/admin_cdn_request_data/';
    admin_status_code_ajax='/cdn/ajax/admin_cdn_status_code_data/';
    bandwidth_data_upload_ajax='/cdn/ajax/admin_download_cdn_flux/';   //详细带宽数据   下载
    state_data_upload_ajax='/cdn/ajax/admin_download_status_code/';    //状态码数据   下载
    code_data_upload_ajax='/cdn/ajax/admin_download_status_code_trend/';   //状态码趋势数据   下载
    var cols_trend=[
      {field:'opt',title:gettext('服务商')}
      ,{field:'200',title:'200'}
      ,{field:'206',title:'206'}
      ,{field:'302',title:'302'}
      ,{field:'304',title:'304'}
      ,{field:'403',title:'403'}
      ,{field:'404',title:'404'}
      ,{field:'5xx',title:'5xx'}
      ,{field:'other',title:gettext('其他')}
    ];

var cols_all_trend=[
      {field:'opt',title:gettext('服务商')}
      ,{field:'2xx',title:'2xx'}
      ,{field:'3xx',title:'3xx'}
      ,{field:'4xx',title:'4xx'}
      ,{field:'5xx',title:'5xx'}
    ];
    var user_list = user_list;
}

var domain_url='';
if(parent_split.length>3){
    if(layui_url == '/cdn/admin_statistics/page/'){
        var user_name=parent_split[parent_split.length-2];   //用户
        $('select[name="choice_user"] option').each(function(){
            if($(this).val()==user_name){
                $(this).attr('selected','selected');
            }
        })
    }
    domain_url=parent_split[parent_split.length-1];   //域名


}


var no_data_html='<div class="no_data"><div class="no_p"><img src="/static/image/no.png" />'+gettext('暂无数据')+'</div></div>';  //图表无数据




//日历
var format = "YYYY-MM-DD HH:mm:ss";
var endDate = moment();  //今天
var endTime = endDate.format(format);   //当前时间
var startTime = endDate.subtract('hours', 24).format(format);   //24小时之前
$('#code_data').val(startTime + ' - ' + endTime);
var formSelects = layui.formSelects;

layui.use(['jquery','table','form','layer','element'], function() {
    var form = layui.form;
    var table = layui.table;
    var element = layui.element;

    // var formSelects = layui.formSelects;

    $("#code_data").daterangepicker({
        format:'YYYY-MM-DD HH:mm:ss',
        todayBtn:true,
        //minDate:moment().subtract(90,'days'),
        maxDate : moment(),
        opens: 'left',
        timePicker: true,
        timePicker12Hour:false,
        timePickerIncrement : 5,
        dateLimit : {
           days : 30
        }, //起止时间的最大间隔
        locale:internation_trans.local ,
    }).on('apply.daterangepicker', function(ev, picker) {

    });

    var time_range=function(time){

        $('.daterangepicker').attr('id','daterangepicker')
        var format = "YYYY-MM-DD HH:mm:ss";
        var startDate;
        var endDate;

        if(time == "24"){
            //最近24小时
            startDate = moment().subtract('hours', 24);
            endDate = moment();
        }else if(time == "seven"){
            // 最近7天
            startDate = moment().startOf('day').subtract('days', 7);
            endDate = moment();
        }else if(time == "today"){
            // 今天
            endDate = moment();
            startDate = moment(moment().format('YYYY-MM-DD') + ' 00:00:00', 'YYYY-MM-DD HH:mm:ss');
        }else if(time == "yesterday"){
             // 昨天
            startDate = moment().subtract('hours', 24);
            startDate = moment(startDate.format('YYYY-MM-DD') + ' 00:00:00', 'YYYY-MM-DD HH:mm:ss');
            endDate = moment(startDate.format('YYYY-MM-DD') + ' 23:59:59', 'YYYY-MM-DD HH:mm:ss');
        }else if(time == "thirty"){
             // 三十天
            startDate = moment().startOf('day').subtract('days', 30);
            endDate = moment();
        }else if(time == "last_month"){
             // 上个月
            startDate = moment().startOf('month').subtract('months', 1);
            endDate = moment().startOf('month').subtract('months', 0);
            // endDate=moment().startOf('month').subtract('months', 0).format('YYYY-MM-DD') + ' 23:59:59', 'YYYY-MM-DD HH:mm:ss'
        }else if(time == "this_month"){
             // 本月
            startDate = moment().startOf('month');
            endDate = moment();
        }else{
            return;
        }
        var startTime = startDate.format(format);
        var endTime = endDate.format(format);

        /*if(is_staff == 'False'){
            time_range('last_month');
        }*/

        $('#code_data').val(startTime + ' - ' + endTime);
    };
    form.on('select(choice_time)',function(data){
        time_range(data.value);
        form.render();
        data_search();
    });
    element.on('tab(time_tab)', function(){    //时间tab切换
        var lay_id=$(this).attr('lay-id');
        time_range(lay_id);
    });
    /*if(is_staff == 'False'){
        time_range('this_month');
    }
*/

    //默认选中用户，域名，服务商
    var user_array=function(value){
        var choice_domain_list='';   //域名
        var choice_opts_list='';   //服务商
        for(var user in user_list){
            var user=user_list[user];
            if(user.id == value || layui_url == '/cdn/client_statistics/page/'){
                var domain_list=user.domain_list;
                for(var domain in domain_list){
                    var domain_in=domain_list[domain];
                    if(domain_url == ''){
                        choice_domain_list += '<option selected value="'+domain_in.id+'">'+domain_in.domain+'</option>'
                    }else{
                        if(domain_in.domain == domain_url){
                            choice_domain_list += '<option selected value="'+domain_in.id+'">'+domain_in.domain+'</option>'
                        }else{
                            choice_domain_list += '<option value="'+domain_in.id+'">'+domain_in.domain+'</option>'
                        }

                    }
                }
                var opts_list=user.cdn_opt;
                for(var opts in opts_list){
                    var opts_in=opts_list[opts];
                    for(var provider in provider_info){
                        var provider=provider_info[provider];
                        if(opts == 0 && opts_in == provider.id){
                            choice_opts_list += '<input checked type="checkbox" lay-filter="service_provider" value="'+gettext(opts_in)+'" name="service_provider" lay-skin="primary" title="'+gettext(provider.name)+'">'
                        }else{
                            if(opts_in == provider.id){
                                choice_opts_list += '<input type="checkbox" lay-filter="service_provider" value="'+gettext(opts_in)+'" name="service_provider" lay-skin="primary" title="'+gettext(provider.name)+'">'
                            }
                        }
                    }
                }
            }
        }
        $("#choice_domain").html('<option value="">'+gettext("全部")+'</option>'+choice_domain_list);
        formSelects.render();
        $("#opts").html('<input type="checkbox" name="all_opts" lay-filter="all_opts" lay-skin="primary" title="'+gettext("所有")+'">'+choice_opts_list);
        form.render();
    };
    user_array($('select[name="choice_user"] option:selected').val());

    //判断服务商个数//是否选中全选按钮
    var service_array=function(){
        var service_provider_list=document.getElementsByName('service_provider').length;
        var service_provider_checked=$('input[name="service_provider"]:checked').length;
        if(service_provider_list == service_provider_checked){
            $('input[name="all_opts"]').prop('checked',true);
        }else{
            $('input[name="all_opts"]').removeAttr('checked');
        }
        form.render();
    };
    service_array();

    form.on('select(choice_user)',function(data){   //选择用户
        user_array(data.value);
        service_array()
        $('.xm-select-label').hide();
        $('.xm-hide-input,.xm-input').val(gettext('全部'))

    });

    form.on('checkbox(service_provider)',function(){    //服务商选择
        service_array();
    });
    form.on('checkbox(all_opts)',function(data){   //服务商全选
        if(data.elem.checked == true){
            $('input[name="service_provider"]').prop('checked',true);
        }else{
            $('input[name="service_provider"]').removeAttr('checked');
        }
        form.render();
    });

    element.on('tab(statistical_data)', function(){   //tab加载
        var this_lay_id=$(this).attr('lay-id');
        if(this_lay_id==1){
            data_search(this_lay_id);
        }else if(this_lay_id==2){
            data_search(this_lay_id);
        }
        form.render();
    });

    form.on('submit(lay_query)',function(){ //查询
        var lay_id=$('#comprehensive .layui-this').attr('lay-id');
        data_search(lay_id);
    });

    function data_array() {     //获取所有查询条件

        var user_id = '';   //用户id
        var domain_id=[];   //域名id
        var opts_array=[];  //服务商
        var opts_array_upload;
        if(is_staff == 'False' && layui_url == '/cdn/client_cdn_overview/page/'){
            time_range($('#client_time option:selected').val());
            user_id='';
            for(var domain in domain_list){
                domain_id.push(domain_list[domain].id)
            }

        }else{
            var choice_domain_list = formSelects.value('choice_domain', 'valStr');
            domain_id = choice_domain_list.split(',');
            if(layui_url == '/cdn/client_statistics/page/'){
                for(var user in user_list){
                    user_id=user_list[user].id;
                }

            }else{
                user_id = $('select[name="choice_user"] option:selected').val();
                var service_provider = document.getElementsByName('service_provider');
                var service_provider_array = [];
                for (var i = 0; i < service_provider.length; i++) {
                    if (service_provider[i].checked) {
                        service_provider_array.push(service_provider[i].value);
                    }
                }
                opts_array = JSON.stringify(service_provider_array);
                opts_array_upload = service_provider_array.join();
            }
        }

        var code_time = $('#code_data').val();
        var start_time = code_time.split(' - ')[0];
        var end_time = code_time.split(' - ')[1];
        var startTime = new Date(Date.parse(start_time.replace(/-/g, "/"))).getTime() / 1000;
        var endTime = new Date(Date.parse(end_time.replace(/-/g, "/"))).getTime() / 1000;
        var domain_array_upload=domain_id.join();
        var domain_array=JSON.stringify(domain_id);
        if(is_staff == 'True'){
            var upload_url=startTime+"/"+endTime+'/'+user_id+'/'+domain_array_upload+'/'+opts_array_upload+'/';
        }else{
            var upload_url=startTime+"/"+endTime+'/'+domain_array_upload+'/';
        }
        return {user_id:user_id,domain_array:domain_array,start_time:startTime,end_time:endTime,opts:opts_array,upload_url:upload_url};
    }

    window.data_search = function(search_id){
        var loading = top.layer.load(1, {
            shade: [0.4,'#fff']
        });

        for(var user in user_list){
            if(is_staff == 'True'){
                var user=user_list[user];
                if(data_array().user_id ==user.id){
                    var domain_list_length=user.domain_list.length;
                }
            }else if(is_staff == 'False'){
                var domain_list_length=user_list[user].domain_list.length;
            }

        }
        var choice_domain_dd=$('.xm-select-label span').length;

        if(domain_list_length == choice_domain_dd){
            $('.xm-select-label').hide();
            $('.xm-hide-input,.xm-input').val(gettext('全部'))
        }

        var table_list=[];
        var json_data={     //json数据
                user_id:data_array().user_id,
                domain_list:data_array().domain_array,
                start_time:data_array().start_time,
                end_time:data_array().end_time,
                opts: data_array().opts,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            };

        if(search_id == 1 || layui_url == '/cdn/client_cdn_overview/page/'){
            //流量带宽数据查询
            var domain_flux=[];
            var echarts_time=[];
            var echarts_sum_cdn=[];
            var echarts_sum_src=[];
            $.ajax({
                type: "POST",
                url: admin_statistics_ajax,
                data: json_data,
                // async:false,
                async:true,
                success: function(res){
                    top.layer.close(loading)
                    if(res.status){
                        var max_cdn_progress=0;
                        var res_max_cdn=0;//峰值带宽
                        var day_max_company='(Mbps)';
                        if(res.max_cdn != undefined  || res.max_cdn !=''){
                            // max_cdn_progress=new Number(res.max_cdn);
                            res_max_cdn=res.max_cdn;
                            var max_zero = parseInt(res_max_cdn);
                            var max_val_length = max_zero.toString().length;

                            if(max_val_length>6){
                                res_max_cdn=res_max_cdn/1000;
                                $('#max_cdn_company').text('Gbps')
                                day_max_company='(Gbps)'
                            }else if(res_max_cdn<1){
                                res_max_cdn=res_max_cdn*1000;
                                $('#max_cdn_company').text('Kbps')
                                day_max_company='(Kbps)'
                            }else{
                                $('#max_cdn_company').text('Mbps')
                                day_max_company='(Mbps)'
                            }
                            // $('#max_cdn').text(fmoney(Math.floor(max_cdn_progress * 100) / 100));
                            $('#max_cdn').text(fmoney(res_max_cdn))
                        }

                        var sum_cdn_progress=0;                                 //总流量
                        var cdn_flux_company='';
                        var day_cdn_company='';
                        if(res.sum_cdn_flux != undefined  || res.sum_cdn_flux !=''){
                            sum_cdn_progress=res.sum_cdn_flux;
                            var max_zero=parseInt(sum_cdn_progress);

                            var sum_cdn_length=max_zero.toString().length;

                            if(sum_cdn_length>9){
                                sum_cdn_progress=sum_cdn_progress/1000000;
                                cdn_flux_company='TB';
                                day_cdn_company='(TB)';

                            }else if(sum_cdn_length>6){
                                sum_cdn_progress=sum_cdn_progress/1000;
                                cdn_flux_company='GB';
                                day_cdn_company='(GB)';
                            }else if(sum_cdn_progress<1){
                                sum_cdn_progress=sum_cdn_progress*1000;
                                cdn_flux_company='KB';
                                day_cdn_company='(KB)';
                            }else{
                                cdn_flux_company='MB';
                                day_cdn_company='(MB)';
                            }

                            $('#cdn_flux_company').text(cdn_flux_company);
                            $('#sum_cdn_flux').text(fmoney(sum_cdn_progress));
                        }



                        var sum_src_company='';                        //回源流量
                        var sum_src_progress=0;
                        var day_src_company='';
                        if(res.sum_src_flux != undefined  || res.sum_src_flux !=''){
                            // sum_src_progress=new Number(res.sum_src_flux);
                            sum_src_progress=res.sum_src_flux;

                            var max_zero=parseInt(sum_src_progress);

                            var sum_cdn_length=max_zero.toString().length;
                            if(sum_cdn_length>9){

                                sum_src_progress=sum_src_progress/1000000;
                                sum_src_company='TB';
                                day_src_company='(TB)';
                            }else if(sum_cdn_length>6){

                                sum_src_progress=sum_src_progress/1000;
                                sum_src_company='GB';
                                day_src_company='(GB)';
                            }else if(sum_src_progress<1){
                                sum_src_progress=sum_src_progress*1000;
                                sum_src_company='KB';
                                day_src_company='(KB)';
                            }else{
                                sum_src_company='MB';
                                day_src_company='(MB)';
                            }

                            $('#sum_src_company').text(sum_src_company);

                            $('#sum_src_flux').text(fmoney(sum_src_progress));

                        }
                        // $('#sum_src_flux').text(fmoney(Math.floor(sum_src_progress * 100) / 100));
                        table_list=res.table_data;

                    }else{
                        res_msg(res);
                    }
                    domain_flux=res.domain_flux;
                    table.render({
                        elem: '#lay_table'
                        ,data:table_list
                        ,cols:[[
                              {field:'day',title:gettext('时间')}
                              ,{field:'day_max_cdn',title:gettext('峰值带宽')+day_max_company}
                              ,{field:'day_max_cdn_time',title:gettext('发生时间')}
                              ,{field:'day_cdn_flux',title:gettext('流量')+day_cdn_company}
                              ,{field:'day_max_src',title:gettext('回源峰值带宽')+day_max_company}
                              ,{field:'day_max_src_time',title:gettext('发生时间')}
                              ,{field:'day_src_flux',title:gettext('回源流量')+day_src_company}
                            ]]
                        ,page: {
                          layout: ['count', 'prev', 'page', 'next',  'skip']
                          ,prev: '<'
                          ,next: '>'
                          ,curr:''
                          ,groups: 5 //只显示 1 个连续页码
                        }
                        ,even: true //开启隔行背景
                        ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
                        ,done:function(obj){
                            $('.layui-none').text(gettext('暂无数据'));
                            $(".layui-table td").each(function(index) {   //状态转换
                                // console.log($(this).attr('data-field'))
                                var this_field=$(this).attr('data-field');
                                var this_children=$(this).children().text();
                                if(index>0){
                                    if(this_field=='day_max_cdn' || this_field=='day_max_src'){
                                        if(day_max_company=='(Kbps)' ){
                                            $(this).children().text(fmoney(this_children*1000))
                                        }else if(day_max_company=='(Gbps)'){
                                            $(this).children().text(fmoney(this_children/1000))
                                        }else if(day_max_company=='(Tbps)'){
                                            $(this).children().text(fmoney(this_children/1000000))
                                        }else{
                                            $(this).children().text(fmoney(this_children))
                                        }
                                    }else if(this_field =='day_cdn_flux'){
                                        if(day_cdn_company=='(KB)' ){
                                            $(this).children().text(fmoney(this_children*1000))
                                        }else if(day_cdn_company=='(GB)'){
                                            $(this).children().text(fmoney(this_children/1000))
                                        }else if(day_cdn_company=='(TB)'){
                                            $(this).children().text(fmoney(this_children/1000000))
                                        }else{
                                            $(this).children().text(fmoney(this_children))
                                        }
                                    }else if(this_field =='day_src_flux'){
                                        if(day_src_company=='(KB)' ){
                                            $(this).children().text(fmoney(this_children*1000))
                                        }else if(day_src_company=='(GB)'){
                                            $(this).children().text(fmoney(this_children/1000))
                                        }else if(day_src_company=='(TB)'){
                                            $(this).children().text(fmoney(this_children/1000000))
                                        }else{
                                            $(this).children().text(fmoney(this_children))
                                        }
                                    }
                                }


                            })
                            if(lan == 'zh'){
                                $('.layui-laypage-count').text('共'+table_list.length+'条');
                            }else{
                                $('.layui-laypage-count').text('Total '+table_list.length);
                            }
                            var laypage_txt='<input type="text" min="1" value="1" class="layui-input">' +
                                    '<button type="button" class="layui-laypage-btn">Go</button>';

                            $('.layui-laypage-skip').html(laypage_txt);
                            $(".layui-laypage-skip").find("input").val($('.layui-laypage-curr em:nth-child(2)').text());
                        }
                    });
                    table.render();
                    // res_table(res,table_list);
                    if(domain_flux !='' && domain_flux !=undefined){
                        res_max=res.max_cdn;

                        $('.no_data').remove();
                        var y_name=gettext('峰值带宽')+'Mbps';
                        var value_num='{value} Mbps';
                        for(var flux_list in domain_flux ){
                            var flux_list=domain_flux[flux_list];
                            echarts_time.push(flux_list.time_key);
                            var cdn_data=flux_list.cdn_data;
                            var src_data=flux_list.src_data;
                            var src_data_split=String(src_data).split('.');

                            if(max_val_length>6 && src_data_split[0]=='0' && src_data_split[1] != undefined && src_data_split[1].substring(0,3)=='000'){
                                src_data=0;
                            }
                            if(max_val_length>9){
                                cdn_data=cdn_data/1000000;
                                src_data=src_data/1000000;
                                y_name=gettext('峰值带宽')+'Tbps';
                                value_num='{value} Tbps';
                            }else if(max_val_length>6){
                                cdn_data=cdn_data/1000;
                                src_data=src_data/1000;
                                y_name=gettext('峰值带宽')+'Gbps';
                                value_num='{value} Gbps';
                            }else if(res_max<1){
                                cdn_data=cdn_data*1000;
                                src_data=src_data*1000;
                                y_name=gettext('峰值带宽')+'Kbps';
                                value_num='{value} Kbps';
                            }
                            // console.log(cdn_data,src_data)
                            // console.log(value_num)
                            echarts_sum_cdn.push(cdn_data);
                            echarts_sum_src.push(src_data);
                        }
                        var band_echart = echarts.init(document.getElementById('band_echart'));
                        var option = {
                            tooltip: {
                                trigger: 'axis'
                            },
                            title: {
                                left: 'center',
                            },
                            legend: {
                                type: 'scroll',
                                bottom: 10,
                                icon: "rect",
                                padding: [5, 20],
                                data:[gettext('CDN带宽'), gettext('回源带宽')]
                            },
                            grid: {
                                left:80,
                                right:50,
                                top:40,
                                bottom:80
                            },
                            xAxis: {
                                type: 'category',//类目轴
                                boundaryGap: false,
                                axisLabel:{
                                    color:'#4f4745'
                                },   // x轴字体颜色
                                axisLine:{
                                    lineStyle:{
                                        color:'#c6c6c6'
                                    }    // x轴坐标轴颜色
                                },
                                axisTick:{
                                    lineStyle:{
                                        color:'#9e9e9e'
                                    }    // x轴刻度的颜色
                                },
                                data: echarts_time
                            },

                            yAxis: {
                                type: 'value',//数值轴    time时间轴
                                name :y_name ,
                                // max: fmoney(res_max_cdn),
                                axisLabel: {
                                    formatter:value_num,
                                    color:'#4f4745'
                                },
                                axisLine:{       //y轴
                                  "show":false

                                },
                                axisTick:{       //y轴刻度线
                                  "show":false
                                },
                                splitLine: {     //网格线
                                    lineStyle:{
                                        color:'#ebebeb'
                                    }
                                }
                            },
                            /*series: [{
                                name: '',
                                type: 'line',
                                symbol: "none",
                                itemStyle: {
                                   normal: {
                                       color: '#2b80e2',
                                       lineStyle: {
                                           color: '#2b80e2'
                                       }
                                   }
                                },
                                data:echarts_value
                            }],*/
                            series: [{
                                name: gettext('CDN带宽'),
                                type: 'line',
                                // step: 'start',
                                // smooth: true,//是否平滑显示
                                symbol: 'none',//标记的图形
                                /*sampling: 'average',//折线图在数据量远大于像素点时候的降采样策略，开启后可以有效的优化图表的绘制效率，默认关闭，也就是全部绘制不过滤数据点。*/
                                itemStyle: {
                                    color: '#2b80e2',
                                    normal: {
                                        color: '#2b80e2',
                                        width:1,
                                    }
                                },
                                data:echarts_sum_cdn
                            },
                            {
                                name:gettext('回源带宽'),
                                type:'line',
                                // step: 'end',
                                // smooth: true,//是否平滑显示
                                symbol: "none",
                                /*sampling: 'average',*/
                                itemStyle: {
                                   normal: {
                                       color: '#e60518',
                                       lineStyle: {
                                           color: '#e60518'
                                       }
                                   }
                                },
                                data:echarts_sum_src
                            }
                            ]
                        };

                        band_echart.setOption(option);
                    }else{

                        $('#band_echart').html(no_data_html);


                    }
                }
            });

            $.ajax({
                type: "POST",
                url: admin_cdn_request_ajax,
                data: json_data,
                // async:false,
                success: function(res){

                    var request_ratio_progress=0;
                    if(res.request_ratio != undefined  || res.request_ratio !=''){
                        request_ratio_progress=new Number(res.request_ratio);
                    }
                    $('#request_ratio').text(Math.floor(request_ratio_progress * 100) / 100);
                }
            })
        }else if(search_id == 2){      //状态码数据查询
            var all_status_code_list='';   //状态码饼图
            var opt_trend_data_list=[];    //趋势数据
            var all_trend_data_list=[];    //趋势数据
            var all_trend_result_list='';

            $.ajax({
                type: "POST",
                url: admin_status_code_ajax,
                data: json_data,
                // async:false,
                success: function(res){
                    top.layer.close(loading)
                    table_list=res.table_data;
                    if(res.status==true){
                        all_status_code_list=res.all_status_code;
                        opt_trend_data_list=res.status_code_table;
                        all_trend_data_list=res.trend_table ;
                        all_trend_result_list=res.all_trend_result;
                        all_status_code_list=res.all_status_code;
                        if(layui_url == '/cdn/client_statistics/page/') {
                            all_trend_data_list = res.all_trend_data;
                        }else{
                            all_trend_data_list = res.trend_table;
                        }
                    }else{
                        res_msg(res);
                    }

                    table.render({
                        elem: '#state_code_table'
                        ,data:opt_trend_data_list
                        ,cols: [cols_trend]
                        ,limit:10
                        ,even: true //开启隔行背景
                        ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
                    });
                    table.render({
                        elem: '#lay_table_xx'
                        ,data:all_trend_data_list
                        ,cols: [cols_all_trend]
                        ,limit:10
                        ,even: true //开启隔行背景
                        ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
                        ,done:function(){
                            $('.layui-none').text(gettext('暂无数据'));
                            $("[data-field = 'opt']").children().each(function(index){   //状态转换
                                if($(this).text()== 'all'){
                                    $(this).text(gettext('所有'));
                                }else if(index>1){
                                    for(var provider in  provider_info){
                                        var provider=provider_info[provider];
                                        if($(this).text() == provider.id){
                                            if(index % 2 == 1){
                                                if(lan == 'en'){
                                                    $(this).text('Percentage of '+gettext(provider.name));
                                                }else{
                                                    $(this).text(gettext(provider.name)+gettext('占比'));
                                                }
                                            }else{
                                                $(this).text(gettext(provider.name));
                                            }
                                        }
                                    }
                                }
                            });

                            $("[data-field = 'ratio']").children().each(function(index){   //状态转换
                                if(index>1 && $(this).text() != gettext('百分比')){
                             /*       var task_progress=new Number($(this).text());
                                    var progress=Math.floor(task_progress * 100) / 100;*/
                                    $(this).text(fmoney($(this).text())+'%');
                                }
                            });
                        }
                    });
                    table.render();


                    if(all_status_code_list != undefined && all_status_code_list != ''){
                        var all_status_code_data=[];
                        var all_status_code_name=[];
                        var code_array=[];
                        for(var all_status_code in all_status_code_list ){
                            all_status_code_name.push(all_status_code);
                            all_status_code_data.push(all_status_code_list[all_status_code])
                        }
                        for(var i in all_status_code_name){
                            code_array[i]={
                                'name': '',
                                'value': ''
                            }
                            code_array[i].name += all_status_code_name[i];
                            code_array[i].value += all_status_code_data[i];

                        }
                        var code_echart = echarts.init(document.getElementById("code_echart"));
                        status_code_option = {
                            tooltip: {
                                trigger: 'item', //触发类型
                                formatter: "{a} <br/>{b}: {c} ({d}%)" //字符串模板
                            },
                            color:['#52b8fa','#fd1b1b','#fdb71b','#ecee25','#84ce7f','#ff6dac','#ab80dc'],
                            legend: { //图例组件
                                top: 'center',
                                orient: 'vertical', //图例列表的布局朝向
                                x: '80%',
                                data: all_status_code_name
                            },
                            series: [{
                                name:gettext('状态码'),
                                type:'pie',
                               /* radius: ['35%', '55%'],
                                center: ['36%', '60%'],*/
                                radius: ['50%', '70%'],
                                    // avoidLabelOverlap: false,
                                label: {
                                    normal: {
                                        formatter: '{abg|}\n{hr|}\n  {b|{b} {d}%}',
                                        borderWidth: 1,
                                        borderRadius: 40,
                                        rich: {
                                            hr: {
                                                width: '100%',
                                                height: 0
                                            },
                                            b: {
                                                fontSize: 14,
                                                lineHeight: 33
                                            },
                                            per: {
                                                color: '#000',
                                                padding: [2, 4],
                                                borderRadius: 2
                                            }
                                        }
                                    }
                                },
                                data:code_array
                            }]
                        };
                        code_echart.setOption(status_code_option);
                    }else{
                        console.log(no_data_html)
                        $('#code_echart').html(no_data_html);
                    }
                }
            });


        };
        element.on('tab(code_tab)', function(){  //状态码趋势图 //tab加载
            $('#code_echart_xx').width($('.code_width').width());

            if(all_trend_result_list != undefined && all_trend_result_list != ''){

                element.on('tab(code_xx)', function() {   //状态码加载
                    var this_lay_id=$(this).attr('lay-id');
                    echarts_code_xx(this_lay_id)
                });
                echarts_code_xx('2xx');
                function echarts_code_xx(this_lay_id){
                    var echarts_time=[];
                    var echarts_value=[];
                    for(var all_trend_result in all_trend_result_list ){
                        var all_trend_result=all_trend_result_list[all_trend_result];
                        echarts_time.push(all_trend_result.time_key);
                        for(var all_trend in all_trend_result){

                            if(all_trend == this_lay_id){
                                echarts_value.push(all_trend_result[all_trend]);
                            }
                        }
                    }
                    var code_echart_xx = echarts.init(document.getElementById('code_echart_xx'));
                    var code_xx_option = {
                        tooltip: {
                            trigger: 'axis'
                        },
                        title: {
                            left: 'center',
                        },
                        /*legend: {
                            type: 'scroll',
                            bottom: 10,
                            icon: "rect",
                            padding: [5, 20],
                            data:
                        },*/
                        grid: {
                            left:80,
                            right:50,
                            top:40,
                            bottom:80
                        },
                        xAxis: {
                            type: 'category',//类目轴
                            boundaryGap: false,
                            axisLabel:{
                                color:'#4f4745'
                            },   // x轴字体颜色
                            axisLine:{
                                lineStyle:{
                                    color:'#c6c6c6'
                                }    // x轴坐标轴颜色
                            },
                            axisTick:{
                                lineStyle:{
                                    color:'#9e9e9e'
                                }    // x轴刻度的颜色
                            },
                            data: echarts_time
                        },

                        yAxis: {
                            type: 'value',//数值轴    time时间轴
                            name : '',
                            axisLabel: {
                                formatter:'{value}',
                                color:'#4f4745'
                            },
                            axisLine:{       //y轴
                              "show":false

                            },
                            axisTick:{       //y轴刻度线
                              "show":false
                            },
                            splitLine: {     //网格线
                                lineStyle:{
                                    color:'#ebebeb'
                                }
                            }
                        },

                        series: [{
                            name: '',
                            type: 'line',
                            symbol: "none",
                            itemStyle: {
                               normal: {
                                   color: '#2b80e2',
                                   lineStyle: {
                                       color: '#2b80e2'
                                   }
                               }
                            },
                            data:echarts_value
                        }]
                    };
                    code_echart_xx.setOption(code_xx_option);
                }
            }else{
                $('#code_echart_xx').html(no_data_html);
            }
            form.render();
        });



    };
    data_search($('#comprehensive .layui-this').attr('lay-id'));

    //详细带宽数据 下载
    $('#bandwidth_data_upload').on('click',function(){
        window.location.href=bandwidth_data_upload_ajax+data_array().upload_url;
    });
    //状态码饼图数据 下载
    $('#state_data_upload').on('click',function(){
        window.location.href=state_data_upload_ajax+data_array().upload_url;
    });
    //状态码趋势图 下载
    $('#code_data_upload').on('click',function(){
        window.location.href=code_data_upload_ajax+data_array().upload_url;
    });
    form.render();
    $(".layui-icon-help").hover(function() {
        $(this).parent().find('.remarks_span').show();
    }, function() {
        $(this).parent().find('.remarks_span').hide();
    });
});
