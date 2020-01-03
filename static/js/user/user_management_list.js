var parent_href=window.parent.location.href;  //浏览器url
var parent_url=parent_href.split('=');

var add='';        //添加
var details='';   //详情
var del='';      //删除
var ajax_list='';  //页面列表
var ajax_user='';  //编辑列表
var page_list=''; //yemian
var delete_list='';
var delete_content=''; //删除文案
var url='';
var cols=[];
console.log(parent_url[1]);
if(parent_url[1]=='/base/parent_child_list/page/' || parent_url.length==1){     //用户管理

    add='create_child_user';
    details='parent_child_details_views';
    edit_List='edit_child_user';
    ajax_list='parent_get_child_list';
    url='/base/parent_child_list/page/';
    page_list='parent_child_list';
    ajax_user='edit_child_user';  //页面列表
    /*log_list='admin_parent_opt_log';
    */
    $('#strategy').hide();
    cols=[
          {field:'username',title:internation_trans.user_name ,event: 'username',style:'cursor: pointer;color:#2c80e3;'}
          ,{field:'is_active',title:internation_trans.remarks}
          ,{field:'user_type', title: internation_trans.creation_time}
          ,{field:'list_button', title: internation_trans.operation,toolbar: '#list_button'}
        ]

}else if(parent_url[1]=='/base/parent_get_perm_strategy/page/'){   //策略管理
    add='parent_create_perm_strategy';
    details='parent_perm_strategy_details';
    ajax_list='parent_get_perm_strategy_list';
    url='/base/parent_get_perm_strategy/page/';
    page_list='parent_get_perm_strategy';
    delete_content='确定删除该条策略？';
    delete_list='delete_perm_strategy';
    cols=[
          {field:'name',title:'策略名' ,event: 'username',style:'cursor: pointer;color:#2c80e3;'}
          ,{field:'strategy_type_name',title:'类型'}
          ,{field:'remark', title: '描述'}
          ,{field:'list_button', title: '操作',toolbar: '#list_button'}
        ]
}

layui.use(['table','form','laypage'], function(){
   var form = layui.form;
   var table = layui.table;
   var layer = layui.layer;
    var count='';
    var curr="";
    var lay_tips =function(lay_cont){    //报错信息
        layer.open({
              title:internation_trans.tips,
              type: 1,
              shade:0,
              btn:internation_trans.sure,
              btnAlign: 'c', //按钮居中
              content:'<div class="lay_content" style="padding: 20px 100px;">'+lay_cont+'</div>'  //这里content是一个普通的String
        });
    };
    window.data_search = function () {
        var username=$('#username').val();
        var strategy_type=$('#management option:selected').val();
        var laypage= $('.layui-laypage-curr em:nth-child(2)').text();
        if(laypage == ''){
           curr=1;
        }else{
           curr=laypage;
        }
        console.log(ajax_list);
        $.ajax({
            type: "POST",
            url: '/base/ajax/'+ajax_list+'/',
            data: {
                id:'',
                name:username,
                username:username,
                strategy_type:strategy_type,
                page:curr,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                console.log(res);
                var table_list;
                // var table_page;
                if(res.status==true){
                    if(parent_url[1] =='/base/parent_get_perm_strategy/page/'){
                        table_list=res.perm_strategy_list;
                    }else{
                        table_list=res.user_list;
                    }
                    if(table_list != '' && table_list !=undefined && parent_url[1] !='/base/parent_get_perm_strategy/page/'){
                        curr=curr;
                        count=res.page_info.total;
                        toPage(curr,count);
                    }
                }
                console.log(cols);
                table.render({
                    elem: '#accounts_list'
                    ,data:table_list
                    ,cols: [cols]
                    ,limit:10
                    , even: true //开启隔行背景
                    ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
                    ,done:function(res){
                        $('.layui-none').text(gettext('暂无数据'));
                        $("[data-field = 'strategy_type_name']").children().each(function(){
                            if($(this).text() == internation_trans.system_strategy){
                              $(this).parents('tr').find("[data-field = 'list_button']").children().hide();
                            }
                        });
                    }
              });


            }
        });
    };

    data_search();

    form.on('select(management)', function(){
       data_search();
    });
    $('.search_user').click(function(){
        data_search();
    });

    table.on('tool(parse-table-demo)', function(obj){   //用户详情
        var data = obj.data;
        var id=data.id;
        if(obj.event === 'username'){   //用户详情
            $('.layui-nav a',parent.document).each(function(){

                    var url_a=$(this).attr('href');
                    var url_split=url_a.split('=');
                    if(url_split[1]=='/base/'+page_list+'/page/'){
                        $("#container",parent.document).attr('src','/base/'+details+'/page/');
                        $("#container",parent.document).attr('url',url_split[2]);
                        if(parent_split.length==1){
                            window.parent.location.href=parent_split[0]+'?=/base/'+details+'/page/'+data.id+'/='+url_split[2];
                        }else{
                            window.parent.location.href=parent_split[0]+'=/base/'+details+'/page/'+data.id+'/='+url_split[2];
                        }

                    }
            })

        }else if(obj.event === 'edit'){
            var user_perm_strategy=data.user_perm_strategy;

            var lay_second = $('#strategy').html();

            var content='<div class="layui-form" id="add_jurisdiction">'+ lay_second + '</div>';
            layer.open({
                type: 1
                ,title: internation_trans.add_strategy
                ,area: ['600px', '560px']
                ,btnAlign: 'l'
                ,shade:0
                ,id: 'add_operational'
                ,content:content
                ,btn: [internation_trans.creation]
                ,yes: function(index_ado){
                    var strategy_list=[];
                    console.log($('#add_operational .added li').length);
                    $('#add_operational .added li').each(function(){
                        strategy_list.push($(this).attr('id'));
                    });
                    var data={
                        perm_strategy:strategy_list,
                        obj_id:id,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    };
                    $.ajax({
                        type: "POST",
                        url: '/base/ajax/'+ajax_user+'/',
                        data: data,
                        async:false,
                        success: function(res){
                            console.log(res);
                            if(res.status){
                                $('.user_add').hide();
                                $('.user_details').show();

                                window.location.reload();
                            }else{
                                lay_tips(res.msg);

                            }
                        }
                    });
                    layer.close(index_ado);
                }

            });
            $('.policy li').removeClass('gray');
            $('.added').html('');

            $('.policy li').each(function(){       //选择策略
                for(var perm_type_in in user_perm_strategy){
                    var perm_type_in=user_perm_strategy[perm_type_in];
                    if(perm_type_in.id==$(this).attr('id')){
                        console.log($(this).attr('id'));
                        $(this).addClass('gray');
                    }
                }

            });
            var user_perm__list='';
            for(var perm_strategy in user_perm_strategy){
                var perm_strategy=user_perm_strategy[perm_strategy];
                user_perm__list +='<li id="'+perm_strategy.id+'" value="'+perm_strategy.strategy_type_name+'"><p>'+perm_strategy.name+'</p>' +
                    '<span>'+perm_strategy.remark+'</span><img src="/static/image/bin.png" /></li>'
            }
            $('.added').html(user_perm__list);

        }else if(obj.event === 'delete'){    //删除用户列表
            console.log(id);
            layer.open({
                type: 1
                ,title: internation_trans.del
                ,area: ['400px', '200px']
                ,btnAlign: 'l'
                ,shade:0
                ,btnAlign: 'c'
                ,id: 'tips_layer'
                ,content: delete_content
                ,btn: [internation_trans.yes_del,internation_trans.no_del]
                ,yes: function(index_ado){
                    $.ajax({
                        type: "POST",
                        url: '/base/ajax/'+delete_list+'/',
                        data: {
                            obj_id:id,
                            csrfmiddlewaretoken: $.cookie('csrftoken')
                        },
                        async:false,
                        success: function(res){
                            if(res.status){
                                layer.close(index_ado);
                                window.location.reload();

                            }

                        }
                    })

                }
            });
        }
        form.render();

    });

    //    新建用户
    var parent_href=window.parent.location.href;  //浏览器url
    var parent_split=parent_href.split('=');
    $(document).on('click','#add_user',function(){       //新建用户

        $('.layui-nav a',parent.document).each(function(){
            var url_a=$(this).attr('href');
            var url_split=url_a.split('=');
            console.log(url_split[1]);
            console.log(url);
            if(url_split[1]==url || parent_url.length==1){
                $("#container",parent.document).attr('src','/user/'+add+'/page/');
                $("#container",parent.document).attr('url',url_split[2]);
                if(parent_split.length==1){
                    window.parent.location.href=parent_split[0]+'?=/base/'+add+'/page/='+url_split[2];
                }else{
                    window.parent.location.href=parent_split[0]+'=/base/'+add+'/page/='+url_split[2];
                }

            }
        })
    });

});


