var parent_href=window.parent.location.href;  //浏览器url
var parent_url=parent_href.split('=');
var parent_id=parent_url[1].split('/');
var ajax_list='';  //页面列表
var navigation_url='';  //操作列表
var ajax_group_delete=''; //删除

var role_group_id=parent_id[parent_id.length-2];
var password_reg = /([a-zA-Z0-9!@#$%^&*()_?<>{}]){6,12}/;
if(parent_id[2]=='admin_parent_details'){     //用户详情
    ajax_list='edit_parent_user';
    navigation_url='admin_parent_list';
    var user_type_json = localStorage.getItem("user_type_json");  //管理员页面
    user_type_json = JSON.parse(user_type_json); //转为JSON
    var products_list ='';      //用户类型
    var user_type_name=$('#user_type_name').text();
    for(var perm_type_in in user_type_json){
        var perm_data=user_type_json[perm_type_in];
        if(user_type_name==perm_data.name){
            // products_list+='<option value="'+perm_data.id+'" selected>'+perm_data.name+'</option>'
            products_list+='<input type="radio" name="user_type" id="'+perm_data.id+'" ' +
                'value="'+perm_data.name+'" title="'+gettext(perm_data.name)+'" checked="">'
        }else{
            // products_list+='<option value="'+perm_data.id+'">'+perm_data.name+'</option>'
            products_list+='<input type="radio" name="user_type" id="'+perm_data.id+'" ' +
                'value="'+perm_data.name+'" title="'+gettext(perm_data.name)+'">'
        }
    }
    $('#select_type').html(products_list);

}else if(parent_id[2]=='admin_group_details_views'){    //角色详情
    ajax_list='admin_group_edit';
    ajax_group_delete='admin_group_delete';
    navigation_url='admin_group_details_views';

}

layui.use(['form','table','element','layer'], function(){
    var form = layui.form;
    var table = layui.table;
    var layer=layui.layer;
    var element=layui.element;
    form.render();
    form.render('checkbox');

    element.on('tab(login_management)', function(){   //tab加载
        form.render();
    });

    $(document).on('click','.del',function(){    //删除操作权限
        var obj = $(this);
        layer.open({
            type: 1
            ,title: gettext('删除')
            ,area: ['400px', '200px']
            ,btnAlign: 'l'
            ,shade:0
            ,btnAlign: 'c'
            ,id: 'tips_layer'
            ,content: gettext('确认删除该服务？')
            ,btn: [gettext('是，确认删除'),gettext('否，取消删除')]
            ,yes: function(index_ado){
                obj.parents('tr').remove();
                var username=$('#username').val();   //新建用户
                var authority_arr=[];   //操作权限
                var td_List = $("#server_tbody tr .server_td");
                var td_length = $('#server_tbody .server_td').length;
                if(td_length == 0){
                    authority_split=[]
                }else{
                    for(var j=0;j<td_length;j++){
                        var td_Arr = td_List.eq(j).attr('id');
                        if(td_Arr !=''){
                           authority_arr+=td_Arr+',';
                        }
                    }
                    var authority_split=authority_arr.split(',');
                }

                authority_split.pop();

                if(parent_id[2]=='admin_group_details_views'){
                    var data={
                        group_id: role_group_id,
                        perm_list:authority_split,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    }
                }else if(parent_id[2]=='admin_parent_details'){
                    var data={
                        username: username,
                        perm:authority_split,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    }
                }

                data_aggregation(data,index_ado);


            }
        });
        form.render();
    });


    //页面数据
    function data_aggregation(data,value){
       $.ajax({
            type: "POST",
            url: '/base/ajax/'+ajax_list+'/',
            data: data,
            async:false,
            success: function(res){
                if(res.status){
                    layer.close(value);
                    // window.location.reload();
                }else{
                    lay_tips(res.msg);

                }
            }
        });
    }

    var server_list='';
    var sums_all=[];
    for(var i=0;i<user_perm_type.length;i++){
        var user_perm_id=user_perm_type[i].id;
        var user_perm_value=gettext(user_perm_type[i].name);
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
                var perm_all=user_perm[perm_all];
                for(var operation in perm_all){
                    var operation=perm_all[operation];
                    sums_all[i].perm_id.push(operation.id);                                   //流量和
                    sums_all[i].perm_value.push(gettext(operation.name));
                }
            }
        }

    }

    for(var i=0;i<sums_all.length;i++){
        server_list +='<tr><td class="server_td" id="'+sums_all[i].user_perm_id+'">'+sums_all[i].user_perm_value+'</td>'+
        '<td class="server_td" id="'+sums_all[i].perm_id+'">'+sums_all[i].perm_value+'</td>' +
        '<td><a class="layui-btn layui-btn-xs edit_xs" lay-event="edit">'+gettext('编辑')+'</a><a class="layui-btn layui-btn-xs del" lay-event="del">'+gettext('删除')+'</a></td></tr>'
    }
    $('#server_tbody').html(server_list);



    var products_list ='';      //选择服务列表

    for(var perm_type_in in perm_type){
        var perm_data=perm_type[perm_type_in];
        if(perm_data.id != 'access_manage_menu'){
            products_list+='<option value="'+perm_data.id+'">'+gettext(perm_data.name)+'</option>'
        }

    }
    form.on('submit(add_operation)',function(){  //添加操作权限
        var get_txt=gettext('添加操作权限');
        add_operation(get_txt);
    });

    $(document).on('click','.edit_xs',function(){    //编辑操作权限
        var edit_xs_this=$(this).parents('tr');
        var server_td_first=edit_xs_this.find('.server_td').eq(0).attr('id');
        var server_td_second=edit_xs_this.find('.server_td').eq(1).attr('id');
        server_td_second=server_td_second.split(',')
        var get_txt=gettext('编辑操作权限');
        add_operation(get_txt,server_td_first,server_td_second,'edit',edit_xs_this);
    });



    function add_operation(get_txt,server_td_first,server_td_second,oper,xs_this){
        if(oper == 'edit') {
            var btn=[gettext('确定')]
        }else{
            var btn=[gettext('创建')]
        }
        var content='<div class="layui-form" id="add_jurisdiction">' +
            '     <div class="layui-form-item">' +
            '      <label class="layui-form-label">'+gettext('选择服务')+'</label>' +
            '      <div class="layui-input-block">' +
            '      <select id="products" name="products" lay-filter="products">' +
            '        <option value="" selected>'+gettext('请选择')+'</option>' + products_list+
            '      </select>' +
            '      </div>'+
            '     </div>' +
            '     <div class="layui-form-item">' +
            '       <label class="layui-form-label">'+gettext('操作名称')+'</label>' +
            '       <div class="layui-input-block">' +
            '        <input type="radio" name="operation" lay-filter="operation" value="'+gettext('所有操作')+'" title="'+gettext('所有操作')+'" checked="">' +
            '        <input type="radio" name="operation" lay-filter="operation" value="'+gettext('特定操作')+'" title="'+gettext('特定操作')+'">' +
            '       </div>' +
            '       <div class="layui-input-block spe_operation" style="display: none;">' +
                        '<div class="select_div" style="display: inline-block">' +
                        '     <label id="select_all" class="select_label" style="margin-bottom: 0;" for=""><input readonly="readonly" value="" placeholder="'+gettext('请选择')+'" type="text"><i class="down"></i></label>' +
                        '     <div class="select_show">' +
                                '<div class="layui-input-block checkbox_a" id="checkbox_user">' +

                                '</div>'+
                                '<div class="layui-input-block">' +
                                '      <button class="checkBtn fl" id="determine" lay-submit lay-filter="determine">'+gettext('确定')+'</button>' +
                                '</div>'+
                              '</div>'+
                        '</div>'+
                    '</div>'+
            '       <div class="layui-input-block" style="display: none;">' +
            '        <button class="checkBtn fl" lay-filter="button_layero" id="button_sub" ></button>' +
            '       </div>'+
            '     </div>'+
            '</div>';
        layer.open({
            type: 1
            ,title: get_txt
            ,area: ['500px', '360px']
            ,btnAlign: 'l'
            ,shade:0
            ,id: 'permissions'
            ,skin:'layer_class'
            ,content:content
            ,btn: btn
            ,yes: function(index_ado){
                // window.location.reload();
                var products=$('#products').val();
                var products_value=[];
                var products_title=[]
                if(products==''){
                    var lay_cont=gettext('服务不能为空');
                    lay_tips(lay_cont);
                    return;
                }else{
                    products_title=[$('#products option:selected').text()];
                    products_value=[$('#products').val()];
                }

                var operation_val='';
                var operation = document.getElementsByName('operation');  //caozuo

                var perm_type=document.getElementsByName('perm_type');
                var perm_value=[];
                var perm_id=[];
                for(var i=0;i<operation.length;i++){
                    if(operation[i].value == gettext('所有操作') && operation[i].checked){

                        for(var j=0;j<perm_type.length;j++){
                            perm_value.push(perm_type[j].value);
                            perm_value=[gettext('所有操作')];
                            perm_id.push(perm_type[j].id);
                        }
                    }else if(operation[i].value == gettext('特定操作') && operation[i].checked){
                        for(var j=0;j<perm_type.length;j++){
                            if(perm_type[j].checked){
                                perm_value.push(gettext(perm_type[j].value));
                                perm_id.push(perm_type[j].id);
                            }
                        }
                    }
                }
                if(operation_val==gettext('特定操作') && $('#operation_name').val()==''){
                    var lay_cont=gettext('操作名称不能为空');
                    lay_tips(lay_cont);
                    return;
                }
                var table_list= {
                       // 'services': products_title,
                       // 'operation_name': perm_value,
                       'perm_id': perm_id,
                       'products_value': products_value,
                    }

                var server_list='<tr>'+
                        '<td class="server_td" id="'+products_value+'">'+products_title+'</td>' +
                        '<td class="server_td" id="'+perm_id+'">'+perm_value+'</td>' +
                        '<td><a class="layui-btn layui-btn-xs edit_xs" lay-event="edit">'+gettext('编辑')+'</a><a class="layui-btn layui-btn-xs del" lay-event="del">'+gettext('删除')+'</a></td>'
                        // '<td class="server_td">'+add_input[i]+'</td>' +
                    '</tr>';

                if(oper == 'edit'){
                    xs_this.replaceWith(server_list);
                }else{
                    $('#server_tbody').append(server_list);
                }

                // reset_password();
                form.render();
                layer.close(index_ado);
                var username=$('#username').val();   //新建用户
                var authority_arr=[];   //操作权限
                var td_List = $("#server_tbody tr .server_td");
                var td_length = $('#server_tbody .server_td').length;
                for(var j=0;j<td_length;j++){
                    var td_Arr = td_List.eq(j).attr('id');
                    if(td_Arr !=''){
                       authority_arr+=td_Arr+',';
                    }
                }
                var authority_split=authority_arr.split(',');
                authority_split.pop();
                if(parent_id[2]=='admin_group_details_views'){   //新建角色
                    var data={
                        perm_list:authority_split,
                        group_id:role_group_id,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    }
                }else{
                   var data={
                        username: username,
                        perm:authority_split,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    }
                }


                data_aggregation(data);
                table_list;
                return;


            }

        });
        if(lan == 'en'){
            $('.layui-form-label').width(140)
        }

        $('select[name="products"] option').each(function(){
            $(this).attr('id');
            if(server_td_first == $(this).val()){
                $(this).prop('selected',true);
            }
            form.render();
        });
        // console.log(this_perm)

        var products_data = function(this_perm,server_td_second,oper){
            var operation_list='';
            for(var perm_all  in perm){
                if(perm_all==this_perm){
                    var perm_all=perm[perm_all]
                    // console.log(perm[perm_all])
                    for(var opera in perm_all){
                        var operation=perm_all[opera];
                        if(operation.id != 'client_api_info') {
                            operation_list += '<input id="' + operation.id + '" title="' + gettext(operation.name) + '" type="checkbox" name="perm_type" value="' + operation.name + '" lay-skin="primary">';
                        }

                    }
                    if(oper == 'edit' && perm_all.length != server_td_second.length){
                        $('input[name="operation"]').each(function(){
                            if($(this).val() == gettext('特定操作')){
                                $(this).attr('checked',true);
                                $('.spe_operation').show();
                            }
                        })
                    }
                }else if(this_perm==gettext('所有操作')){
                    var perm_all=perm[perm_all]
                   for(var operation in perm_all){
                        var operation=perm_all[operation];
                        if(operation.id != 'client_api_info') {
                            operation_list += '<input id="' + operation.id + '" title="' + gettext(operation.name) + '" type="checkbox" name="perm_type" value="' + operation.name + '" lay-skin="primary">';
                        }
                   }
                }
                //
             }
             $('#checkbox_user').html(operation_list);
             form.render()
             if(oper == 'edit'){
                var perm_type_name=document.getElementsByName('perm_type');
                for(var i=0;i<perm_type_name.length;i++){
                    for(var server in server_td_second){
                        if(perm_type_name[i].id == server_td_second[server]){
                            perm_type_name[i].checked = true;

                        }
                    }
                }
             }



        }
        products_data(server_td_first,server_td_second,oper)

        form.on('select(products)', function(obj){   //选择服务
            var this_perm=obj.value;
            products_data(this_perm,server_td_second,oper);
            form.render();
        });



        $('#determine').click(function(e){
            var perm_type_list= {
                    'perm_type_id':'',
                    'perm_type_value':''
                }
            var perm_type = document.getElementsByName('perm_type');
            for(var i=0;i<perm_type.length;i++){
                if(perm_type[i].checked){
                    perm_type_list.perm_type_id += perm_type[i].id+',';
                    perm_type_list.perm_type_value += gettext(perm_type[i].value)+','
                }
            }
            var perm_value=perm_type_list.perm_type_value.slice(0,-1);
            var perm_id=perm_type_list.perm_type_id.slice(0,-1);
            $('#select_all input').val(perm_value);
            $('.select_label input').attr('title',perm_id);
            e.stopPropagation();
            $('.select_div').removeClass('current');
        })


        $('.select_div').click(function(e){
            e.stopPropagation();
            var service_selected =$('select[name="products"] option:selected').val();
            if(service_selected != ''){
                $(this).parent().addClass('current')
            }
        });
        $('.select_label').click(function(e){    //弹窗
            if($(this).parent().hasClass('current')){
                $(this).parent().removeClass('current')
            }else{
                var service_selected =$('select[name="products"] option:selected').val();

                if(service_selected != ''){
                    $(this).parent().addClass('current')
                }else if(service_selected == ''){
                    lay_tips(gettext('请先选择服务'))
                    return;
                }

            }
            e.stopPropagation();
        });


        document.onclick = function(){
            $('.select_div').removeClass('current');
        };


        form.on('radio(operation)', function(data){
           if(data.value==gettext('特定操作')){
               if(oper == 'edit'){
                   server_td_second;

                   var perm_type = document.getElementsByName('perm_type');
                   for(var i=0;i<perm_type.length;i++){
                        if(perm_type[i].id == server_td_second[i]){
                            perm_type[i].checked=true;
                        }
                   }
               }

               $('.spe_operation').show();
           }else{
               $('.spe_operation').hide();
           }
           form.render();
        });

        var authority_arr=[];   //操作权限

        if($('#server_tbody .server_td').length !=0){
            var td_List = $("#server_tbody tr .server_td");
            var td_length = $('#server_tbody .server_td').length;
            for(var j=0;j<td_length;j++){
                var td_Arr = td_List.eq(j).attr('id');
                if(td_Arr !=''){
                   authority_arr+=td_Arr+',';
                }
            }
            var authority_split=authority_arr.split(',');
            $('#add_jurisdiction option').each(function(){
                for(var j=0;j<authority_split.length;j++){
                    if(authority_split[j]==$(this).val()){
                        $(this).attr('disabled','disabled');
                        // $(this).attr('selected',true);

                    }else if(oper== 'edit' && $(this).val()==xs_this.find('td:first-child').attr('id')){
                        $(this).attr('disabled',false);
                    }
                }
            });

        }
        form.render();
    }

    if(parent_id[2] =='admin_parent_details'){   //用户详情操作
        document.getElementById("edit").onclick = edit;  //编辑
        function edit(){
            $('.user_add').show();
            $('.user_details').hide();
        }
        document.getElementById("user_cancel").onclick = user_cancel;   //取消
        function user_cancel(){
            $('.user_add').hide();
            $('.user_details').show();
        }

        document.getElementById("user_sure").onclick = user_sure; //确定
        function user_sure(){
            var username=$('#username').val();   //新建用户
            var company=$('#company').val();
            var contacts=$('#contacts').val();
            var mobile=$('#mobile').val();
            var email=$('#email').val();
            var user_id='';
            var user_value='';
            var user_type = document.getElementsByName('user_type');
            for(var i=0;i<user_type.length;i++){
                if(user_type[i].checked){
                    user_id = user_type[i].id;
                    user_value = user_type[i].value;
                }
            }
            var authority_arr=[];   //操作权限
                var td_List = $("#server_tbody tr .server_td");
                var td_length = $('#server_tbody .server_td').length;
                for(var j=0;j<td_length;j++){
                    var td_Arr = td_List.eq(j).attr('id');
                    if(td_Arr !=''){
                       authority_arr+=td_Arr+',';
                    }
                }
                var authority_split=[];
                if(authority_arr !=''){
                    authority_split=authority_arr.split(',');
                }

                authority_split.pop();
            var data={
                username: username,
                company: company,
                linkman: contacts,
                mobile: mobile,
                email: email,
                user_type: user_id,
                perm:authority_split,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            }
            data_aggregation(data);
        }

        document.getElementById("reset_password").onclick = reset_password; //重置密码
        // var perm_type_in=perm_type;
        function reset_password(){
            var content='<div class="layui-form" id="add_jurisdiction">' +
                '     <div class="layui-form-item">' +
                '      <label class="layui-form-label" style="width:110px;">控制台密码</label>' +
                '      <div class="layui-input-block">' +
                '<input id="password" type="text" name="password"  lay-verify="password" placeholder="" autocomplete="off" class="layui-input">' +
                '<p class="mistake"></p>'+
                '      </div>'+
                '     </div>' +
                '</div>';
            layer.open({
                type: 1
                ,title: '重置密码'
                ,area: ['500px', '240px']
                ,btnAlign: 'l'
                ,shade:0
                ,id: 'permissions'
                ,content:content
                ,btn: ['确定']
                ,yes: function(index_ado){
                    var username=$('#username').val();
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
    }

    $(document).on('click','.switch_login',function(){
        var obj=$(this);
        var this_text=$(this).text();
        var status;
        layer.open({
            title:gettext('控制台登录')
            ,content: gettext('确定开启/关闭控制台访问权限')
            ,btnAlign: 'c'
            ,area:['400px','200px']
            ,shade:0
            ,btn: [gettext('确定'), gettext('取消')]
            ,yes: function(index){
                var username=$('#username').val();
                if(this_text=='OFF'){
                    status=1;
                }else{
                    status=0;
                }
                var data_url={
                    username: username,
                    is_active:status,
                    csrfmiddlewaretoken: $.cookie('csrftoken')
                }
                data_aggregation(data_url);
                if(status==1){
                    obj.addClass('layui-form-onswitch');
                    obj.find('em').text('ON');
                }else{
                    obj.removeClass('layui-form-onswitch');
                    obj.find('em').text('OFF');
                }
                form.render();
                layer.close(index);
            }

        });
        return false;
    });

    /*form.on('submit(add_new_key)',function(){  //

        $.ajax({
            type: "POST",
            url: '/base/ajax/admin_open_parent_api/',
            data: {
                username:username,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){

                if(res.status){
                    // console.log(res)
                    window.location.reload();
                }else{
                    res_msg(res);
                }
            }
        });
    });*/

});
