var parent_href=window.parent.location.href;  //浏览器url
var parent_url=parent_href.split('=');
console.log(parent_url);
var parent_split=parent_url[1].split('/');
var parent_page=parent_split[parent_split.length-3];
console.log(parent_page);
var  url='/security/admin_safe_channel_list/page/';
var ajax_list='';
layui.use(['table','form','laypage','element','laydate'], function() {
    var form = layui.form;
    var element = layui.element;
    var table = layui.table;
    var layer = layui.layer;
    var laydate = layui.laydate;
    var startup_cols=[      //启动阙值
          {field:'customer_account',title:'安全客户账号'}
          ,{field:'cms_id', title: 'CMS客户ID'}
          ,{field:'cms_status',title:'CMS客户状态',sort: true}
          ,{field:'safe_channel', title: '安全频道',style:'cursor: pointer;color:#2c80e3;'}
          ,{field:'startup_button', title: '操作',toolbar: '#startup_button'}
        ];
    $.ajax({
        type: "POST",
        url: '/base/ajax/'+ajax_list+'/',
        data: {
            id:'',
            /*customer_account:customer_account,
            company:company,
            salesforce:salesforce,*/
            csrfmiddlewaretoken: $.cookie('csrftoken')
        },
        async:false,
        success: function(res){
            console.log(res);
            var startup_list;
            // var table_page;
            if(res.status==true){
                if(parent_url[1] =='/base/admin_group_manage/page/'){
                    startup_list=res.groups;
                }else{
                    startup_list=res.user_list;
                }

                for(var table_id in startup_list){
                    table_id=startup_list[table_id];
                }

            }

            table.render({
                elem: '#startup_threshold'
                ,data:startup_list
                ,cols: [startup_cols]
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

        }
    });

    var recognition_cols=[    //ip识别规则
          {field:'customer_account',title:'场景'}
          ,{field:'cms_id', title: '场景'}
          ,{field:'cms_status',title:'开关'}
          ,{field:'safe_channel', title: '请求频率（请求/分钟）',style:'cursor: pointer;color:#2c80e3;'}
          ,{field:'cms_status',title:'请求占比'}
          ,{field:'cms_status',title:'miss率'}
          ,{field:'cms_status',title:'空referer率'}
          ,{field:'cms_status',title:'空range率'}
          ,{field:'cms_status',title:'触发动作'}
          ,{field:'cms_status',title:'生效时长'}
          ,{field:'recognition_button', title: '操作',toolbar: '#recognition_button'}
        ];
    $.ajax({
        type: "POST",
        url: '/base/ajax/'+ajax_list+'/',
        data: {
            id:'',
            /*customer_account:customer_account,
            company:company,
            salesforce:salesforce,*/
            csrfmiddlewaretoken: $.cookie('csrftoken')
        },
        async:false,
        success: function(res){
            console.log(res);
            var recognition_list;
            // var table_page;
            if(res.status==true){
                if(parent_url[1] =='/base/admin_group_manage/page/'){
                    recognition_list=res.groups;
                }else{
                    recognition_list=res.user_list;
                }

                for(var table_id in recognition_list){
                    table_id=recognition_list[table_id];
                }

            }

            table.render({
                elem: '#recognition_ip'
                ,data:recognition_list
                ,cols: [recognition_cols]
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

        }
    });

    var alarm_cols=[    //ip识别规则
          {field:'customer_account',title:'监控项'}
          ,{field:'cms_status',title:'开关'}
          ,{field:'cms_status',title:'阙值'}
          ,{field:'alarm_button', title: '操作',toolbar: '#alarm_button'}
        ];
    $.ajax({
        type: "POST",
        url: '/base/ajax/'+ajax_list+'/',
        data: {
            id:'',
        /*    customer_account:customer_account,
            company:company,
            salesforce:salesforce,*/
            csrfmiddlewaretoken: $.cookie('csrftoken')
        },
        async:false,
        success: function(res){
            console.log(res);
            var alarm_list;
            // var table_page;
            if(res.status==true){
                if(parent_url[1] =='/base/admin_group_manage/page/'){
                    alarm_list=res.groups;
                }else{
                    alarm_list=res.user_list;
                }

                for(var table_id in alarm_list){
                    table_id=alarm_list[table_id];
                }

            }

            table.render({
                elem: '#alarm_configuration'
                ,data:alarm_list
                ,cols: [alarm_cols]
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

        }
    });


    var alarm_cols=[      //启动阙值
          {field:'customer_account',title:''}
          ,{field:'cms_id', title: gettext('CMS客户ID')}
          ,{field:'cms_status',title: gettext('CMS客户状态'),sort: true}
          ,{field:'safe_channel', title: gettext('安全频道'),style:'cursor: pointer;color:#2c80e3;'}
          ,{field:'startup_button', title: gettext('操作'),toolbar: '#startup_button'}
        ];
    $.ajax({
        type: "POST",
        url: '/base/ajax/'+ajax_list+'/',
        data: {
            id:'',
            /*customer_account:customer_account,
            company:company,
            salesforce:salesforce,*/
            csrfmiddlewaretoken: $.cookie('csrftoken')
        },
        async:false,
        success: function(res){
            console.log(res);
            var alarm_list;
            // var table_page;
            if(res.status==true){
                if(parent_url[1] =='/base/admin_group_manage/page/'){
                    alarm_list=res.groups;
                }else{
                    alarm_list=res.user_list;
                }

                for(var table_id in alarm_list){
                    table_id=alarm_list[table_id];
                }

            }

            table.render({
                elem: '#startup_threshold'
                ,data:alarm_list
                ,cols: [alarm_cols]
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

        }
    });



    // var comprehensive_li=document.getElementById('comprehensive').getElementsByTagName('li');

    console.log(parent_url[2]);
    var channel_select=document.getElementById('channel_select');
    channel_select.onclick=function(){
        console.log(this.value);
        var this_value=this.value;
        $('.layui-nav a',parent.document).each(function(){
            var url_a=$(this).attr('href');
            var url_split=url_a.split('=');
            if(url_split[1]==url){
                window.parent.location.href=parent_url[0]+'=/security/'+this_value+'/page/='+url_split[2];
            }
        })

    }
/*    form.on('select(channel_select)', function(obj){
        console.log(obj);
       $(document).on('click','#add_user',function(){       //新建用户
            $('.layui-nav a',parent.document).each(function(){
                var url_a=$(this).attr('href');
                var url_split=url_a.split('=');
                if(url_split[1]=='/base/admin_parent_list/page/'){
                    $("#container",parent.document).attr('src','/base/'+add+'/page/');
                    $("#container",parent.document).attr('url',url_split[2]);
                    if(parent_split.length==1){
                        window.parent.location.href=parent_split[0]+'?=/base/'+add+'/page/='+url_split[2];
                    }else{
                        window.parent.location.href=parent_split[0]+'=/base/'+add+'/page/='+url_split[2];
                    }

                }
            })
        });
    });*/
    form.render();
    laydate.render({
       max:0
      ,type: 'date'
      ,range: true
      ,elem: '#alarm_data'
      ,ready:function(){
          $('.laydate-btns-confirm').click(function(){
              // data_search();
          })

      }
    });

})
