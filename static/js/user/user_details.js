var parent_href=window.parent.location.href;  //浏览器url
var parent_url=parent_href.split('=');
var parent_id=parent_url[1].split('/');

var ajax_list='edit_child_user';  //页面列表
var navigation_url='parent_child_list';  //操作列表
var password_reg = /([a-zA-Z0-9!@#$%^&*()_?<>{}]){6,12}/;
var role_group_id=parent_id[parent_id.length-2];
var username=$('#username').text();
$('#strategy').hide();
if(parent_id[2]=='admin_parent_details'){     //用户详情

    var user_type_json = localStorage.getItem("user_type_json");  //管理员页面
    user_type_json = JSON.parse(user_type_json); //转为JSON

    var products_list ='';      //用户类型
    var user_type_name=$('#user_type_name').text();

    for(var perm_type_in in user_type_json){
        var perm_data=user_type_json[perm_type_in];
        console.log(user_type_name);
        console.log(perm_data.name);
        if(user_type_name==perm_data.name){
            // products_list+='<option value="'+perm_data.id+'" selected>'+perm_data.name+'</option>'
            products_list+='<input type="radio" name="user_type" id="'+perm_data.id+'" ' +
                'value="'+perm_data.name+'" title="'+perm_data.name+'" checked="">'
        }else{
            // products_list+='<option value="'+perm_data.id+'">'+perm_data.name+'</option>'
            products_list+='<input type="radio" name="user_type" id="'+perm_data.id+'" ' +
                'value="'+perm_data.name+'" title="'+perm_data.name+'">'
        }
    }
    $('#select_type').html(products_list);

}else if(parent_id[2]=='admin_group_details_views'){    //角色详情
    ajax_list='admin_group_edit';
    navigation_url='admin_group_details_views';

}

layui.use(['form','table','element','layer'], function(){
    var form = layui.form;
    var table = layui.table;
    var layer=layui.layer;
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

   var lay_second = $('#strategy').html();
   document.getElementById("add_operation").onclick = add_operation;   //详情页添加权限策略
   function add_operation(){
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
                var added_length=$('#add_jurisdiction .added li').length;
                var strategy_id=[],
                strategy_type=[],
                strategy_name=[]
                $('#add_jurisdiction .added li').each(function(e){
                    strategy_id.push($(this).attr('id'));
                    strategy_type.push($(this).attr('value'));
                    strategy_name.push($(this).find('p').text());

                });
                /*var server_list='';
                for(var i=0;i<strategy_id.length;i++){
                    server_list +='<tr id="'+strategy_id[i]+'">'+
                        '<td class="server_td">'+strategy_name[i]+'</td>' +
                        '<td class="server_td" >'+strategy_type[i]+'</td>' +
                        '<td><a class="layui-btn layui-btn-danger layui-btn-xs del" lay-event="del">删除</a></td>'
                        // '<td class="server_td">'+add_input[i]+'</td>' +
                    '</tr>';
                }
                console.log(server_list);
                if($('#server_tbody').html() !=''){
                    $('#server_tbody').append(server_list);
                }else{
                    $('#server_tbody').html(server_list);
                }*/

                // reset_password();

                var perm_list={
                    perm_strategy:strategy_id,
                    obj_id:role_group_id,
                    csrfmiddlewaretoken: $.cookie('csrftoken')
                };

                data_aggregation(perm_list,index_ado);
                form.render();
                return;
            }

        });
        $('.button_all').hide();

        $('.policy li').removeClass('gray');
        $('.added').html('');

        $('.policy li').each(function(){       //选择策略
            for(var perm_type_in in user_perm){
                var perm_type_in=user_perm[perm_type_in];
                if(perm_type_in.id==$(this).attr('id')){
                    console.log($(this).attr('id'));
                    $(this).addClass('gray');
                }
            }

        });
        var user_perm__list='';
        for(var perm_strategy in user_perm){
            var perm_strategy=user_perm[perm_strategy];
            user_perm__list +='<li id="'+perm_strategy.id+'" value="'+perm_strategy.strategy_type_name+'"><p>'+perm_strategy.name+'</p>' +
                '<span>'+perm_strategy.remark+'</span><img src="/static/image/bin.png" /></li>'
        }
        $('.added').html(user_perm__list);
        form.render();
    }

   $(document).on('click','.del',function(){    //删除操作权限
        var obj = $(this);
        layer.open({
            type: 1
            ,title: internation_trans.del
            ,area: ['400px', '200px']
            ,btnAlign: 'l'
            ,shade:0
            ,btnAlign: 'c'
            ,id: 'tips_layer'
            ,content:internation_trans.delete_service
            ,btn: [internation_trans.yes_del,internation_trans.no_del]
            ,yes: function(index_ado){
                obj.parents('tr').remove();
                var strategy_id=[];
                $('#server_tbody tr').each(function(){
                    strategy_id.push($(this).attr('id'));
                });
                var data={
                    obj_id: role_group_id,
                    perm:strategy_id,
                    csrfmiddlewaretoken: $.cookie('csrftoken')
                }
                data_aggregation(data,index_ado);


            }
        });
        form.render();
   });

    //页面数据
    function data_aggregation(data,value){
       console.log(data);
       console.log(ajax_list);
       // return;
       $.ajax({
            type: "POST",
            url: '/base/ajax/'+ajax_list+'/',
            data: data,
            async:false,
            success: function(res){
                console.log(res);
                if(res.status){
                    layer.close(value);
                    window.location.reload();
                }else{
                    lay_tips(res.msg);

                }
            }
        });
    }

  /*  var server_list='';
    var sums_all=[];
    for(var i=0;i<user_perm_type.length;i++){
        var user_perm_id=user_perm_type[i].id;
        var user_perm_value=user_perm_type[i].name;
        if (!sums_all[i]) {
            sums_all[i] = {
                user_perm_id: '',
                user_perm_value: '',
                perm_id:[],
                perm_value:[]
            };
        }
        sums_all[i].user_perm_id += user_perm_id;                                   //流量和
        sums_all[i].user_perm_value += user_perm_value;
        for(var perm_all  in user_perm){
            if(perm_all==user_perm_type[i].id){
                console.log(perm_all);
                var perm_all=user_perm[perm_all];
                for(var operation in perm_all){
                    var operation=perm_all[operation];
                    sums_all[i].perm_id += operation.id+',';                                   //流量和
                    sums_all[i].perm_value += operation.name+',';
                }
            }
        }

    }
    console.log(sums_all);
    for(var i=0;i<sums_all.length;i++){
        server_list +='<tr><td class="server_td" id="'+sums_all[i].user_perm_id+'">'+sums_all[i].user_perm_value+'</td>'+
        '<td class="server_td" id="'+sums_all[i].perm_id+'">'+sums_all[i].perm_value+'</td>' +
        '<td><a class="layui-btn layui-btn-danger layui-btn-xs del" lay-event="del">删除</a></td></tr>'
    }

    $('#server_tbody').html(server_list);*/



    document.getElementById("user_sure").onclick = user_sure; //确定
    function user_sure(){
        var mobile=$('#mobile').val();
        var email=$('#email').val();
        var remark=$('#remark').val();
        var data={
            username: username,
            mobile: mobile,
            email: email,
            remark: remark,
            obj_id:role_group_id,
            csrfmiddlewaretoken: $.cookie('csrftoken')
        }
        data_aggregation(data);
    }

    document.getElementById("reset_password").onclick = reset_password; //重置密码
    // var perm_type_in=perm_type;
    function reset_password(){
        var content='<div class="layui-form" id="add_jurisdiction">' +
            '     <div class="layui-form-item">' +
            '      <label class="layui-form-label" style="width:110px;">'+internation_trans.log_password+'</label>' +
            '      <div class="layui-input-block">' +
            '<input id="password" type="text" name="password"  lay-verify="password" placeholder="" autocomplete="off" class="layui-input">' +
            '<p class="mistake"></p>'+
            '      </div>'+
            '     </div>' +
 // /*           '     <div class="layui-form-item">' +
 //            '       <label class="layui-form-label" style="width:110px;">需要重置密码</label>' +
 //            '       <div class="layui-input-block">' +
 //            '           <input id="reset_password" title="用户必须在下次登录时重置密码" type="checkbox" name="perm_type" value="用户必须在下次登录时重置密码" lay-skin="primary">' +
 //            '       </div>' +
 //            '     </div>'+*/
            '</div>';
        layer.open({
            type: 1
            ,title: '重置密码'
            ,area: ['500px', '220px']
            ,btnAlign: 'l'
            ,shade:0
            ,id: 'permissions'
            ,content:content
            ,btn: ['确定']
            ,yes: function(index_ado){
                var password=$('#password').val();

                if(password==''){
                    var lay_cont='密码不能为空';
                    $('.mistake').text(lay_cont);
                    return;
                }
                if(!password_reg.test(password)){
                    var lay_cont='密码必须6到12位';
                    lay_tips(lay_cont);
                    return;
                }

                var data={
                    username: username,
                    password: password,
                    csrfmiddlewaretoken: $.cookie('csrftoken')
                }

                data_aggregation(data);

                form.render();
                layer.close(index_ado);

            }

        });

        form.render();
    }


    form.on('switch(switch_login)', function(data){    //控制台登录
        var x=data.elem.checked;
        layer.open({
            title:'控制台登录'
            ,content: '确定开启/关闭控制台访问权限'
            ,btnAlign: 'c'
            ,shade:0
            ,btn: ['确定', '取消']
            ,yes: function(index, layero){
                data.elem.checked=x;
                if(data.elem.checked==true){
                    var is_active=1;
                }else{
                    var is_active=0;
                }
                var data_url={
                    username: username,
                    is_active:is_active,
                    csrfmiddlewaretoken: $.cookie('csrftoken')
                }
                data_aggregation(data_url);
                form.render();
                layer.close(index);
                //按钮【按钮一】的回调
            }
            ,btn2: function(index, layero){
                //按钮【按钮二】的回调
                data.elem.checked=!x;
                form.render();
                layer.close(index);
            }
            ,cancel: function(){
                //右上角关闭回调
                data.elem.checked=!x;
                form.render();

            }
        });
        // return false;
        form.render();
    });

});
