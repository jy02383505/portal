var parent_href=window.parent.location.href;  //浏览器url
var parent_url=parent_href.split('=');
var parent_split=parent_url[1].split('/');
var parent_page=parent_split[parent_split.length-3];

var domain_id='';
var all_rules_ajax=''//开启关闭规则接口
if(parent_url.length>3){
    parent_page=parent_split[parent_split.length-4];
    domain_id=parent_split[parent_split.length-2];
    // domain_id=parent_url[parent_url.length-2]
}else{
    parent_page=parent_split[parent_split.length-4];
}

var get_log_ajax='';// 拦截日志接口
var parent_get_waf_statistics='';//统计接口
var parent_get_log_detail='';//日志详情
var parent_download_time_cnt='';//攻击下载
var parent_download_ip_list='';//攻击来源
var parent_download_rule_list='';//攻击方式
var parent_download_log='';//日志下载
var limit=20;
if(parent_page=='admin_sec_overview' ){
    safe_url='/sec/admin_sec_domain_list/page/';
    get_log_ajax='admin_get_log_list';// 拦截日志接口
    parent_get_waf_statistics='admin_get_waf_statistics';//统计接口
    parent_get_log_detail='admin_get_log_detail';//日志详情
    parent_download_time_cnt='admin_download_time_cnt';//攻击下载
    parent_download_ip_list='admin_download_ip_list';//攻击来源
    parent_download_rule_list='admin_download_rule_list';//攻击方式
    parent_download_log='admin_download_log';//日志下载
}else if(parent_page=='parent_sec_overview'){  //用户
    get_log_ajax='parent_get_log_list';
    parent_get_waf_statistics='parent_get_waf_statistics';
    parent_get_log_detail='parent_get_log_detail';
    parent_download_time_cnt='parent_download_time_cnt';
    parent_download_ip_list='parent_download_ip_list';
    parent_download_rule_list='parent_download_rule_list';
    parent_download_log='parent_download_log';

}
var lang=parent.document.getElementById('lang').value; // 浏览器语言

var no_data_html='<div class="no_data"><div class="no_p"><img src="/static/image/no.png" />'+gettext('暂无数据') +'</div></div>';

var d=new Date();
var year=d.getFullYear();
var month=change(d.getMonth()+1);
var day=change(d.getDate());
var hour=change(d.getHours());
var minute=change(d.getMinutes());
var second=change(d.getSeconds());
function change(t){
    if(t<10){
     return "0"+t;
    }else{
     return t;
    }
}
var time=year+'-'+month+'-'+day+' '+hour+':'+minute+':'+second;

var time_flag='';
time_flag=time.split(' ')[0];
$('#log_data').val(time_flag+' 00:00:00 - '+time);

var format = "YYYY-MM-DD";
var startDate;
var endDate;
//今天
endDate = moment();
var startTime = endDate.format(format);
var endTime = endDate.format(format);
$('#code_data').val(startTime + ' - ' + endTime);
$(document).ready(function () {


});

layui.use(['table','laydate','form','element'], function(){
    var table = layui.table;
    var form = layui.form;
    var element=layui.element;
    var laydate = layui.laydate;

    element.on('tab(status_code)', function(){   //tab加载
        $('#code_data').val('');
        var this_lay_id=$(this).attr('lay-id');
        if(this_lay_id=='today'){
            time_flag=time.split(' ')[0];
            statistics_search(time_flag+' - '+time_flag);
        }else if(this_lay_id=='yesterday'){
            var yesterday_time=new Date(new Date()-1000*60*60*24);
            var year=yesterday_time.getFullYear();
            var month=change(yesterday_time.getMonth()+1);
            var day=change(yesterday_time.getDate());
            time_flag=year+'-'+month+'-'+day
            statistics_search(time_flag+' - '+time_flag);
        }

        $('#code_data').val(time_flag+' - '+time_flag);
    });
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
            locale:internation_trans.local,
        }).on('apply.daterangepicker', function(ev, picker) {
            statistics_search(picker.startDate.format('YYYY-MM-DD')+' - '+picker.endDate.format('YYYY-MM-DD'));
        });


    window.statistics_search=function(code_time){

        var start_time=code_time.split(' - ')[0];
        var end_time=code_time.split(' - ')[1];
        var echart_list='';

        $.ajax({      //统计接口
            type: "POST",
            url: '/sec/ajax/' + parent_get_waf_statistics + '/',
            data: {
                domain_id: mi_id,
                // time_flag:time_flag,
                start_time:start_time,
                end_time:end_time,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async: false,
            success: function (res) {
                if(res.status=true && res.statistics_data != undefined){
                    $('.no_data').remove();
                    echart_list=res.statistics_data;
                }
            }
        });

        var waf_times=[];
        var waf_value='';
        var waf_y=[];
        var waf_all=0;
        var waf_time_cnt=echart_list.time_cnt;
        $('#waf_times').hide();
        if(waf_time_cnt== '' || echart_list==''){
            $('.layui_first').append(no_data_html);
            $('#waf_echart').hide();
            $('#waf_attack_load').hide();
        }else{
            $('.no_data').remove();
            $('#waf_attack_load').show();
            $('#waf_echart').css('display','block');

            for(var i=0;i<waf_time_cnt.length;i++){
                waf_y.push(waf_time_cnt[i].cnt);
                waf_all += waf_time_cnt[i].cnt;
                waf_times.push(waf_time_cnt[i].name);
            }
            console.log(waf_all)
            $('#waf_times a').text(fmoney(waf_all).split('.')[0]);
            $('#waf_times').show();
            waf_value='{value}';
            // internation_trans.times
            //WAF拦截攻击数
            var waf_echart = echarts.init(document.getElementById('waf_echart'));
            var option = {
                tooltip: {
                    trigger: 'axis'
                },
                title: {
                    left: 'center',
                },
                grid: {
                    left:80,
                    right:50,
                    top:40
                },
                xAxis: {
                    type: 'category',//类目轴
                    boundaryGap: false,
                    data: waf_times,
                },

                yAxis: {
                    type: 'value',//数值轴    time时间轴
                    name: gettext('攻击数'),
                    axisLabel: {
                        formatter:waf_value
                    },
                },
                dataZoom: [
                    {
                        id: 'dataZoomX',
                        type: 'slider',
                        xAxisIndex: [0],
                        filterMode: 'filter'
                    },
                ],
                series: [{
                    name: '',
                    type: 'line',
                    smooth: true,//是否平滑显示
                    symbol: 'none',//标记的图形
                    sampling: 'average',//折线图在数据量远大于像素点时候的降采样策略，开启后可以有效的优化图表的绘制效率，默认关闭，也就是全部绘制不过滤数据点。

                    itemStyle: {
                        normal: {
                            color: '#438ECD',
                            width:1,
                        }
                    },
                    areaStyle: {
                        normal: {
                              color: '#F2F8FF'
                        }
                    },
                    data: waf_y
                }]
            };

            waf_echart.setOption(option);
        }


        //攻击来源
        var attack_x=[];
        var attack_city=[];
        var source_attack_list='';
        var ip_list=echart_list.ip_list;
        if(ip_list=='' || echart_list==''){
            $('.layui_second').append(no_data_html);
            $('.echart_second,#source_load,.top10_url_title').hide();
        }else{
            $('.no_data').remove();
            $('#source_load').show();
            $('#source_load,.top10_url_title').show();
            $('.echart_second').css('display','block');
            for(var attack in ip_list){
                if(attack<10){
                    attack_x.push(ip_list[attack].cnt);
                    attack_city.push(ip_list[attack].ip_address);
                    source_attack_list += '<li>' +
                    '                        <span style="width:110px;">'+ip_list[attack].ip+'</span>' +
                    // '                        <span>'+ip_list[attack].attack_country+'</span>' +
                    '                        <span><img class="flags_img" src="/static/image/flags/'+ip_list[attack].short_name.toLowerCase()+'_flag[1].gif" alt="">'+ip_list[attack].ip_address+'</span>' +
                    // '                        <span style="width:60px;">'+ip_list[attack].name+'</span>' +
                    '                    </li>'
                }

            }
            var attack_x_reverse=attack_x;
            var attack_one_id=document.getElementById('attack_one');
            $('#source_attack').html(source_attack_list);
            var attack_one = echarts.init(attack_one_id);
            var attack_one_option = {
                title: {
                    text: gettext('攻击次数（单位：次）'),
                    top:10,
                    left: 40,
                    textStyle: {
                        color:'#2B80E2',
                        fontSize:14,
                        fontWeight:'normal'
                    },
                },
                grid: {
                    // left: 50,
                    right: 50,
                    // bottom:0,
                    top:40,
                    containLabel: true
                },
                xAxis : [
                    {
                        show : false,
                        type : 'value'
                    },
                ],
                yAxis : [
                     {
                        type : 'category',

                        axisLabel: {
                            inside: true,
                            textStyle: {
                                color: '#fff'
                            }
                            /*textStyle: {
                                color: 'rgb(0,0,0,0)'
                            }*/
                        },
                        axisTick: {
                            show: false
                        },
                        axisLine: {
                            show:false,
                            color:'#D9D9D9'
                        },
                        //show : true,
                        // inverse: true,
                         inverse: true,
                        //data : attack_city
                         data: ['一', '二', '三', '四', '五','六','七','八','九','十']
                    }

                ],
                series : [
                    {
                        name: '',
                        type: 'bar',
                        barWidth:25,
                        barCategoryGap:25,
                        label: {
                            normal: {
                                show: true,
                                position: 'left',
                                color: '#4972C4',
                            },
                            formatter: '{c}'+gettext('次')
                        },
                        itemStyle: {
                            normal: {
                                color: '#4972C4',
                            }
                        },
                        data: attack_x_reverse
                    }
                ]
            };

            attack_one.setOption(attack_one_option);
            window.addEventListener("resize",function(){
                attack_one.resize();
            });

        }

        //攻击方式

        var rule_list=echart_list.rule_list;
        if(rule_list=='' || echart_list==''){
            $('.layui_third').append(no_data_html);
            $('.echart_three').hide();
            $('#attack_load').hide();
        }else {
            $('.no_data').remove();
            $('#attack_load').show();
            $('.echart_three').css('display','block');

            table.render({
                elem: '#attack_type'
                , data: rule_list
                , cols: [[      //默认规则
                    {field: 'name',width:'35%', title: gettext('攻击类型')}
                    , {field: 'cnt', width:'29%',title: gettext('攻击数')}
                    , {field: 'pro', width:'35%',title: gettext('攻击百分比')}
                ]]
                ,limit:5
                , even: true //开启隔行背景
                , done: function () {
                    $("[data-field = 'pro']").children().each(function (index) {
                        if(index>0){
                            $(this).text($(this).text() + '%')
                        }
                    });
                    // layer.close(index);
                }
            });
            table.render();
            var rule_data = {};
            for (var i = 0; i < rule_list.length; i++) {
                rule_data[i] = {
                    'value': '',
                    'name': '',
                };
                rule_data[i].value += rule_list[i].cnt;
                rule_data[i].name += rule_list[i].name;

            }
            var rule_arr = [];
            for (var i in rule_data) {
                rule_arr.push(rule_data[i]);
            }

            var attack_modes = echarts.init(document.getElementById('attack_modes'));
            var attack_modes_option = {

                title: {
                    text: gettext('攻击类型分布'),
                    top:0,
                    left: 'left',
                    textStyle: {
                        color:'#2B80E2',
                        fontSize:14,
                        fontWeight:'normal'
                    },
                },
                series: [

                    {
                        name: '',
                        type: 'pie',
                        minAngle: 30,           　　 //最小的扇区角度（0 ~ 360），用于防止某个值过小导致扇区太小影响交互
                        avoidLabelOverlap: true,   //是否启用防止标签重叠策略
                        hoverAnimation:false,　　  //是否开启 hover 在扇区上的放大动画效果。
                        silent: true,　
                        radius: ['50%', '65%'],
                        label: {
                            normal: {
                                //formatter: '{b|{b}：}{c};{d}% ',
                                formatter(v) {
                                    let text=v.name +':'+v.value+';'+v.percent + '%'
                                    if (text.length <= 16) {
                                        return text=v.name +':'+v.value+';'+v.percent + '%'
                                    } else if (text.length > 16 && text.length <= 24) {
                                        return text=v.name +':'+v.value+';\n'+v.percent + '%'
                                    } else if (text.length > 24) {
                                        return text=v.name +':\n'+v.value+';\n'+v.percent + '%'
                                    }
                                },
                                borderRadius: 4,
                                // shadowBlur:3,
                                // shadowOffsetX: 2,
                                // shadowOffsetY: 2,
                                // shadowColor: '#999',
                                // padding: [0, 7],
                                rich: {
                                    a: {
                                        color: '#999',
                                        lineHeight: 22,
                                        align: 'center'
                                    },
                                    hr: {
                                        borderColor: '#aaa',
                                        width: '100%',
                                        borderWidth: 0.5,
                                        height: 0
                                    },
                                    b: {
                                        fontSize: 14,
                                        lineHeight: 24
                                    },
                                    per: {
                                        color: '#eee',
                                        backgroundColor: '#334455',
                                        padding: [2, 4],
                                        borderRadius: 2
                                    }
                                }
                            }
                        },
                        data: rule_arr
                    }
                ]
            };
            attack_modes.setOption(attack_modes_option);
        }


        var url_list=echart_list.url_list;   //top5被攻击URL
        var attack_url_x=[];
        var attack_url_domain=[];
        var attack_url_list='';

        if(url_list=='' || echart_list==''){
            $('.layui_four').append(no_data_html);
            $('.echart_four,.top_url_title').hide();
        }else {
            $('.no_data').remove();
            $('.echart_four,.top_url_title').css('display','block');
            for (var attack in url_list) {
                if(attack<5){
                    attack_url_x.push(url_list[attack].cnt);
                    attack_url_domain.push(url_list[attack].name);
                    attack_url_list += '<li>' +
                        '                        <span id="copy'+attack+'" title="' + unescape(url_list[attack].site_url) + '">' + unescape(url_list[attack].site_url) +
                        '</span><a class="copy" id="copy_a'+attack+'">'+gettext('复制')+'</a><a type="javascript:;" class="copy"></a>' +
                        '                    </li>'
                }
            }
            $('#attack_url_ul').html(attack_url_list);

            //复制
            $(document).on('click','.copy',function(){
              var text = $(this).parent().find('span').text();
              var input = document.getElementById("textarea");
              input.value = text; // 修改文本框的内容
              input.select(); // 选中文本
              document.execCommand("copy"); // 执行浏览器复制命令
              top.layer.msg(gettext('复制成功'), {
                area: ['150px', '60px']
                ,offset: 'lt'
                ,time: 1000, //20s后自动关闭
              });
            })

            // var attack_url_id=document.getElementById('attack_url');

            var attack_url = echarts.init(document.getElementById('attack_url'));
            var attack_url_option = {
                title: {
                    text: gettext('攻击次数（单位：次）'),
                    top:0,
                    left: 80,
                    textStyle: {
                        color:'#2B80E2',
                        fontSize:14,
                        fontWeight:'normal'
                    },
                },
                grid: {

                    right: 50,
                    bottom: 0,
                    top: 35,
                    containLabel: true
                },
                xAxis: [
                    {
                        show: false,
                        type: 'value'
                    },
                ],
                yAxis: [
                    {
                        type: 'category',
                        show: false,
                        axisTick: {show: false},
                        axisLine: {
                            show:false,
                            color:'#fff'
                        },
                        inverse: true,
                        // data : attack_url_domain
                        data: ['周一', '周二', '周三', '周四', '周五']
                        // ['1','2','3','4','5']
                    }

                ],
                series: [
                    {
                        name: '',
                        type: 'bar',
                        barWidth:25,
                        barCategoryGap:25,
                        label: {
                            normal: {
                                show: true,
                                position: 'left'
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: '#4972C4',
                            }
                        },
                        data: attack_url_x
                    }
                ]
            }
            attack_url.setOption(attack_url_option);
        }

        parent.window.addEventListener("resize", function () {
            attack_url.resize();
            attack_modes.resize();
            waf_echart.resize();
            attack_one.resize();
        });
    }
    var code_time=$('#code_data').val();
    statistics_search(code_time);


    /*laydate.render({    //拦截日志时间
       max:0
      ,lang: lang
      ,format:'yyyy-MM-dd HH:mm:ss'
      ,type: 'datetime'
      ,range: true
      ,min:-30
      ,max:time
      ,trigger : 'click'
      ,elem: '#log_data'
      ,ready:function(){
          $('.laydate-btns-confirm').click(function(){
              // data_search();
          })
      }
    });*/

    $("#log_data").daterangepicker({
        format:'YYYY-MM-DD HH:mm:ss',
        todayBtn:true,
        //minDate:moment().subtract(90,'days'),
        maxDate : moment(),
        opens: 'left',
        timePicker: true,
        timePicker12Hour:false,
        timePickerIncrement : 1,
        dateLimit : {
           days : 180
        }, //起止时间的最大间隔
        locale:{
            applyLabel: gettext('确定'),
            cancelLabel: gettext('取消'),
            fromLabel: gettext('从'),
            toLabel: gettext('到'),
            customRangeLabel: gettext('手动选择'),
            daysOfWeek: [gettext('日'), gettext('一'), gettext('二'), gettext('三'), gettext('四'), gettext('五'), gettext('六')],
            monthNames: [gettext('一月'),gettext('二月'),gettext('三月') , gettext('四月'),gettext('五月') ,gettext('六月') ,
                gettext('七月'), gettext('八月'), gettext('九月'), gettext('十月'), gettext('十一月'),gettext('十二月')
            ],
            firstDay: 1

        },
    }).on('apply.daterangepicker', function(ev, picker) {

        // statistics_search(picker.startDate.format('YYYY-MM-DD HH:mm:ss')+' - '+picker.endDate.format('YYYY-MM-DD HH:mm:ss'));

    });



    if(parent_page=='parent_sec_overview') {

        window.data_search = function () {       //拦截日志
            var atk_ip = $('#atk_ip').val();//规则ID
            var log_data = $('#log_data').val();//拦截时间
            var start_time;
            var end_time;
            if (log_data != '') {
                var log_data_start = log_data.split(' - ');

                start_time = log_data_start[0];
                end_time = log_data_start[1];
            } else {
                start_time = '';
                end_time = '';
            }
            var laypage = $('.layui-laypage-curr em:nth-child(2)').text();
            if (laypage == '') {
                curr = 1;
            } else {
                curr = laypage;
            }
            $.ajax({
                type: "POST",
                url: '/sec/ajax/' + get_log_ajax + '/',
                data: {
                    domain_id: mi_id,
                    atk_ip: atk_ip,
                    start_time: start_time,
                    end_time: end_time,
                    page: curr,
                    csrfmiddlewaretoken: $.cookie('csrftoken')
                },
                async: false,
                success: function (res) {
                    console.log(res);
                    var startup_list;
                    if (res.status == true) {
                        if (parent_page == 'parent_sec_overview') {
                            startup_list = res.log_list;
                            var log_rows = res.log_rows;
                            $('#log_rows').text(log_rows);
                            if (log_rows == '0') {
                                document.getElementById('log_load').style.display = 'none';
                            } else {
                                document.getElementById('log_load').style.display = 'block';
                            }
                        }
                        if (startup_list != '' && startup_list != undefined) {
                            curr = curr;
                            count = res.page_info.total;
                            toPage(curr, count, limit);
                        }

                    } else {
                        if (res.msg != '' && res.msg != undefined) {
                            lay_tips(res.msg);
                        } else {
                            lay_tips(gettext('通讯异常'));
                        }
                    }

                    table.render({
                        elem: '#interception_log'
                        , data: startup_list
                        , cols: [[      //默认规则internation_trans.rule_id
                            {field: 'log_time', width: "20%", title: gettext('拦截时间')}
                            , {field: 'atk_ip', width: "20%", title: 'IP'}
                            , {field: 'target_url', width: "40%", event: 'url_event', title: 'URL'}

                            , {field: 'atk_type', width: "9%", title: gettext('攻击类型')}
                            , {field: 'ruleid', width: "9%", title: gettext('规则ID')}
                            // ,{field:'rule_info',width:"60%",title: internation_trans.inter_rule_info}
                            , {
                                field: 'rule_status',
                                width: "10%",
                                title: gettext('操作'),
                                toolbar: '#intercept_button'
                            }
                        ]]
                        , limit: 20
                        , lang: lang
                        , even: true //开启隔行背景
                        ,parseData: function(res){ //将原始数据解析成 table 组件所规定的数据
                          return {
                            "code": res.status, //解析接口状态
                            "msg": res.message, //解析提示文本
                            "count": res.total, //解析数据长度
                            "data": res.rows.item //解析数据列表
                          };
                        }
                        , done: function () {
                            $("[data-field = 'target_url']").children().each(function () {
                                var url_text = $(this).text();
                                $(this).text(unescape(url_text));
                            });
                            $('.layui-none').text(gettext('暂无数据'));

                            // layer.close(index);
                        }
                    });
                    table.render();
                }
            });
        };
        var domain_id = $('#domain').attr('domain_id');
        table.on('tool(interception_log)', function (obj) {
            var obj_log = obj.data;
            var data_detail = '';
            if (obj.event == 'details') {
                $.ajax({
                    type: "POST",
                    url: '/sec/ajax/' + parent_get_log_detail + '/',
                    data: {
                        domain_id: domain_id,
                        log_id: obj_log.log_id,
                        log_time: obj_log.log_time,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    },
                    async: false,
                    success: function (res) {
                        if (res.status) {
                            data_detail = JSON.stringify(res.detail_data, null, 2);
                        }

                    }
                });
                top.layer.open({
                    type: 1
                    , title: gettext('日志详情')
                    , area: ['400px', '550px']
                    , btnAlign: 'l'
                    , shade: 0
                    // ,offset: 'rb'
                    , fixed: true
                    , offset: ['0', '0', '0', '0']
                    , btnAlign: 'c'
                    , btn: [gettext('复制')]
                    , id: 'tips_layer'
                    , content: '<pre class="data_detail" style="padding:0 50px 20px;">' + data_detail + '</pre>'

                    , yes: function () {
                        var input = document.getElementById("textarea");
                        input.value = data_detail; // 修改文本框的内容
                        input.select(); // 选中文本
                        document.execCommand("copy"); // 执行浏览器复制命令
                        top.layer.msg(gettext('复制成功'), {
                            area: ['150px', '60px']
                            , offset: 'lt'
                            , time: 1000, //20s后自动关闭
                        });
                    }
                });

            }

        })

        data_search();
        form.render();
        table.render();

    }

    function data_times(){
        var data_time=$('#code_data').val();
        var time_flag = data_time.split(' - ');
        var time_flag_start=time_flag[0] +' 00:00:00';
        var time_flag_end=time_flag[1] +' 00:00:00';
        var start_time=Date.parse(new Date(time_flag_start))/1000;
        var end_time=Date.parse(new Date(time_flag_end))/1000;
        return {start_time:start_time,end_time:end_time};
    }
   $('#waf_attack_load').on('click',function(){

        window.location.href='/sec/ajax/'+parent_download_time_cnt+'/'+domain_id+"/"+ data_times().start_time+"/"+data_times().end_time;
    });
    $('#source_load').on('click',function(){
        window.location.href='/sec/ajax/'+parent_download_ip_list+'/'+domain_id+"/"+ data_times().start_time+"/"+data_times().end_time;
    });
    $('#attack_load').on('click',function(){    //攻击方式
        window.location.href='/sec/ajax/'+parent_download_rule_list+'/'+domain_id+"/"+ data_times().start_time+"/"+data_times().end_time;
    });
    $('#log_load').on('click',function(){
        var atk_ip='';//规则ID
        if(atk_ip==''){
            atk_ip='-';

        }else{
            atk_ip=$('#atk_ip').val();//规则IDstart_time
        }
        var log_data=$('#log_data').val();//拦截时间
        var log_rows=$('#log_rows').text();
        var start_time;
        var end_time;
        if(log_data != ''){
            var log_data_start=log_data.split(' - ');
            start_time=Date.parse(new Date(log_data_start[0]))/1000;
            end_time=Date.parse(new Date(log_data_start[1]))/1000;
        }else{
            start_time='-';
            end_time='-';
        }
        window.location.href='/sec/ajax/'+parent_download_log+'/'+domain_id+"/"+ atk_ip+"/"+start_time+'/'+end_time+'/'+log_rows+'/';

    });
});

