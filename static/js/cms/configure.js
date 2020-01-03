var domain_key=parent_split[parent_split.length-1];     //域名
var domain_id=parent_oblique[parent_oblique.length-2];  //域名id
var all_rules_ajax='';    //开启关闭规则接口
var default_ajax_list='';// 默认规则
var custom_ajax_list='';//自定义规则
var enable_default_ajax='';//单规则状态修改
var enable_self_ajax='';//单规则状态修改
var waf_default_mod='';
var waf_self_mode='';
if(is_staff == 'True'){
    default_ajax_list='admin_get_waf_default_rule';//默认规则
    custom_ajax_list='admin_get_waf_self_rule';//自定义规则
    all_rules_ajax='admin_reset_default_rule';   //   开启关闭规则接口
    enable_default_ajax='admin_enable_default_rule';//单规则状态修改
    enable_self_ajax='admin_enable_self_rule';//单规则状态修改
}else if(is_staff == 'False'){
    default_ajax_list='parent_get_waf_default_rule';//默认规则
    custom_ajax_list='parent_get_waf_self_rule';//自定义规则
    all_rules_ajax='parent_reset_default_rule';   //   开启关闭规则接口
    enable_default_ajax='parent_enable_default_rule';//单规则状态修改
    enable_self_ajax='parent_enable_self_rule';//单规则状态修改
    set_ajax_list='/sec/ajax/parent_set_defense_mode/';//客户端修改基础配置
    waf_default_mod=waf_default_mode_conf;   //默认规则列表
    waf_self_mode=waf_self_mode_conf;        //自定义规则列表
}
layui.use(['table','form','laypage','element'], function() {
    var form = layui.form;
    var table = layui.table;
    var layer = layui.layer;
    var element=layui.element;
    var index;
    var lan=parent.document.getElementById('lang').value;
    var default_rules='';
    $(".layui-laypage-btn").click(function(){
        var curr_page=$(".layui-laypage-skip").find("input").val();
    });
    window.search_rule=function(index){       //默认规则
        var rule_id=$('#rule_id').val();//规则ID
        var rule_name=$('#rule_name').val();//规则名
        var rule_status=$('#rule_status option:selected').val();//规则状态

        $.ajax({
            type: "POST",
            url: '/sec/ajax/'+default_ajax_list+'/',
            data: {
                domain_id:domain_id,
                domain:domain_key,
                rule_id:rule_id,
                rule_info:rule_name,
                rule_status:rule_status,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                console.log(res)
                var startup_list;
                layer.close(index);
                if(res.status==true){
                    startup_list=res.rule_list;
                    default_rules=res.rule_list;
                }else{
                    startup_list=[];
                    res_msg(res);
                }

                if(startup_list != '' && startup_list !=undefined){
                    var rule_info_list=[];
                    for(var i=0;i<startup_list.length;i++){
                        if(startup_list[i].rule_id=='171'){
                            startup_list[i].rule_info=gettext('防止利用多个“script”重叠标签进行xss跨站攻击的规则')
                        }
                        rule_info_list.push(startup_list[i].rule_info);
                    }
                }

                var laypage_txt='<input type="text" min="1" value="1" class="layui-input">' +
                                '<button type="button" class="layui-laypage-btn">Go</button>';
                 $('.layui-laypage-skip').html(laypage_txt);

                table.render({
                    elem: '#default_waf'
                    ,data:startup_list
                    ,page: {
                      layout: ['count', 'prev', 'page', 'next',  'skip']
                      ,prev: '<'
                      ,next: '>'
                      ,curr:''
                      ,groups: 5 //只显示 1 个连续页码
                    }
                    ,cols: [[      //默认规则
                      {field:'rule_id',width:'10%',title:gettext('规则ID')}
                      ,{field:'rule_info',width:"70%",title: gettext('规则名')}
                      ,{field:'enable',title:gettext('规则开关'),templet: function(d){  //自定义显示内容
                        return '<div class="layui-unselect layui-form-switch switch_default" mid="'+d.rule_status+'" lay-skin="_switch"><em>OFF</em><i></i></div>'
                      }}

                    ]]
                    ,even: true //开启隔行背景
                    // ,width:'100%'
                    ,time: 10*1000
                    // ,cellMinWidth: 100
                    ,done:function(obj){
                        $("[data-field = 'enable']").find('.switch_default').each(function(obj){
                            if($(this).attr('mid') == '1'){
                              $(this).addClass('layui-form-onswitch');
                              $(this).find('em').text('ON');
                            }else if($(this).text() == '0'){
                              $(this).removeClass('layui-form-onswitch');
                              $(this).find('em').text('OFF');
                            }
                        });
                        $(".layui-laypage-skip").find("input").val();
                        $('.layui-none').text(gettext('暂无数据'));
                        if(lan == 'zh'){
                            $('.layui-laypage-count').text('共'+obj.count+'条');
                        }else{
                            $('.layui-laypage-count').text('Total '+obj.count);
                        }
                        $('.layui-laypage-btn').text('Go');
                    }
              });
            }
        });
    };


    window.custom_search=function(index){   //自定义状态
        var limit=10;
        var custom_id=$('#custom_id').val();//规则ID
        var custom_status=$('#custom_status option:selected').val();//规则状态
        layer.close(index);
        var laypage= $('#page .layui-laypage-curr em:nth-child(2)').text();
        if(laypage == ''){
           curr=1;
        }else{
           curr=laypage;
        }
        $.ajax({
            type: "POST",
            url: '/sec/ajax/'+custom_ajax_list+'/',
            data: {
                domain_id:domain_id,
                rule_name:custom_id,
                rule_status:custom_status,
                page:curr,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                var custom_data;
                if(res.status==true){
                    custom_data=res.rule_list;
                    if(custom_data != '' && custom_data !=undefined){
                        curr=curr;
                        count=res.page_info.total;
                        toPage(curr,count,limit);
                    }
                }else{
                    custom_data=[];
                }
                table.render({
                    elem: '#custom_list'
                    ,data:custom_data
                    // ,width:1000
                    ,cols: [[      //默认规则
                      {field:'id',title:gettext('规则ID')}
                      ,{field:'name',title: gettext('规则名')}
                      ,{field:'rule_details',title: gettext('匹配内容'),toolbar:'#custom_bar'}
                      ,{field:'action',title: gettext('后续动作')}
                      ,{field:'enable',title:gettext('规则开关'),templet: function(d){  //自定义显示内容
                        return '<div class="layui-unselect layui-form-switch switch_custom" mid="'+d.enable+'" lay-skin="_switch"><em>OFF</em><i></i></div>'
                      }}
                    ]]
                    ,even: true //开启隔行背景
                    ,done:function(obj){
                        $("[data-field = 'action']").children().each(function(){
                            if($(this).text() == '2'){
                              $(this).html(gettext('直接阻断'));
                            }else if($(this).text() == '3'){
                              $(this).html(gettext('直接放行'));
                            }
                        });
                        $("[data-field = 'enable']").find('.switch_custom').each(function(obj){
                            if($(this).attr('mid') == '1'){
                              $(this).addClass('layui-form-onswitch');
                              $(this).find('em').text('ON');
                            }else if($(this).text() == '0'){
                              $(this).removeClass('layui-form-onswitch');
                              $(this).find('em').text('OFF');
                            }
                        });
                        $('.layui-none').text(gettext('暂无数据'));

                    }
                });
                table.render();

            }
        });
    };

    element.on('tab(waf_con)', function(){   //tab加载
        var index = layer.load(1);
        var this_lay_id=$(this).attr('lay-id');
        if(this_lay_id=='22'){
            search_rule(index);

        }else if(this_lay_id=='33'){
            custom_search(index);
        }else if(this_lay_id=='11'){
            layer.close(index);
        }
        $('.search_in input[type="text"],.search_in select').val('');
        form.render();
    });

    var default_rules_id=[];     //默认规则全部id
    for(var i=0;default_rules.length<i;i++){
        default_rules_id.push(default_rules[i].rule_id);
    }
    form.on('submit(open_all_rules)', function() {   //开启全部规则
        var custom_status=1;
        var delete_content=gettext('确定开启全部默认规则？');
        all_rules(default_rules_id,custom_status,delete_content);

    });
    form.on('submit(close_all_rules)', function() {   //关闭全部规则
        var custom_status=0;
        var delete_content=gettext('确定关闭全部默认规则？');
        all_rules(default_rules_id,custom_status,delete_content);

    });

    function all_rules(default_rules_id,custom_status,delete_content){
        layer.open({
            type: 1
            ,title: gettext('提示')
            ,area: ['400px', '200px']
            ,btnAlign: 'l'
            ,shade:0
            ,btnAlign: 'c'
            ,id: 'tips_layer'
            ,content: delete_content
            ,btn: [gettext('确定'),gettext('取消')]
            ,yes: function(index_ado){
                $.ajax({
                    type: "POST",
                    url: '/sec/ajax/'+all_rules_ajax+'/',
                    data: {
                        domain_id:domain_id,
                        enable:custom_status,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    },
                    async:false,
                    success: function(res){
                        if(res.status == true){
                            layer.close(index_ado);
                            search_rule();
                        }
                    }
                });
            }
        });
    }
    $(document).on('click','.switch_default',function(){
        var obj=$(this);
        var this_text=$(this).text();
        var id = $(this).parents('tr').find('td:first-child').text();
        var delete_content='';
        var status;
        var x;
        if(this_text=='OFF'){
            status=1;
            x=true;
            delete_content=gettext('确定开启默认规则？');
        }else{
            status=0;
            x=false;
            delete_content=gettext('确定关闭默认规则？');
        }
        var enable_ajax=enable_default_ajax;
        rules(obj,id,x,delete_content,status,enable_ajax);
    });

    $(document).on('click','.switch_custom',function(){
        var obj=$(this);
        var this_text=$(this).text();
        var id = $(this).parents('tr').find('td:first-child').text();
        var delete_content='';
        var status;
        var x;
        if(this_text=='OFF'){
            status=1;
            x=true;
            delete_content=gettext('确定开启自定义规则？');
        }else{
            status=0;
            x=false;
            delete_content=gettext('确定关闭自定义规则？');
        }
        var enable_ajax=enable_self_ajax;
        rules(obj,id,x,delete_content,status,enable_ajax);
    });


    function rules(obj,id,x,delete_content,status,enable_ajax){
        layer.open({
            type: 1
            ,title: gettext('提示')
            ,area: ['400px', '200px']
            ,btnAlign: 'l'
            ,shade:0
            ,btnAlign: 'c'
            ,id: 'tips_layer'
            ,content: delete_content
            ,btn: [gettext('确定'),gettext('取消')]
            ,yes: function(index_ado){
                // form.render();
                $.ajax({
                    type: "POST",
                    url: '/sec/ajax/'+enable_ajax+'/',
                    data: {
                        domain_id:domain_id,
                        rule_id:id,
                        enable:status,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    },
                    async:false,
                    success: function(res){

                        if(res.status == true){
                            layer.close(index_ado);
                            if(status==1){
                                obj.addClass('layui-form-onswitch');
                                obj.find('em').text('ON');
                            }else{
                                obj.removeClass('layui-form-onswitch');
                                obj.find('em').text('OFF');
                            }

                        }
                    }
                });
            }
        });

    };


    table.on('tool(custom_list)', function(obj) {   //自定义规则详情
        var data = obj.data;
        var data_detail = JSON.stringify(data.detail,null,2);
        if (obj.event === 'details') {
            layer.open({
                type: 1
                , title: gettext('匹配内容')
                , area: ['350px', '550px']
                , btnAlign: 'l'
                , shade: 0
                , btnAlign: 'c'
                , id: 'tips_layer'
                , content: '<pre class="data_detail" style="padding:0 50px;">' + data_detail + '</pre>'
                , yes: function (index_ado) {
                }
            });
        }
    });
    form.render();
});
