var ajax_list='';  //页面列表
var navigation_url='';  //操作列表
var cols=[];    //table表头

if(parent_oblique[2]=='create_parent_user'){     //新建用户
    ajax_list='create_parent_user';
    navigation_url='admin_parent_list';
    cols=[
          {field:'username',title:gettext('用户名')}
          ,{field:'company',title:gettext('公司名称')}
          ,{field:'contacts',title: gettext('联系人')}
          ,{field:'email',title:gettext('联系邮箱')}
          ,{field:'mobile',title: gettext('联系电话')}
          ,{field:'user_value',title:gettext('用户类型')}
        ]

}else if(parent_oblique[2]=='admin_group_create'){   //新建角色
    ajax_list='admin_group_create';
    navigation_url='admin_group_manage';
    cols=[
          {field:'name',title:gettext('用户名') }
          ,{field:'describe',title:gettext('描述')}
          ,{field:'remarks',title: gettext('备注')}
        ]
}

layui.use(['form','table','element','layer'], function(){
    var form = layui.form;
    var table = layui.table;
    var layer=layui.layer;

    form.on('submit(next_step_first)',function(){   //用户信息
        //var password_reg=/^[\\S]{6,12}$/;   //密码
        var password_reg = /([a-zA-Z0-9!@#$%^&*()_?<>{}]){5,11}/;
        var email_reg=/^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/;   //邮箱
        var phone_reg=/^1[34578]\d{9}$/;   //手机号
        if(parent_oblique[2]=='create_parent_user'){     //新建用户
           var username=$('#username').val();
            if(username==''){
                var lay_cont=gettext('用户名不能为空');
                lay_tips(lay_cont);
                return;
            }
            var company=$('#company').val();
            if(company==''){
                var lay_cont=gettext('公司名称不能为空');
                lay_tips(lay_cont);
                return;
            }
            var mobile=$('#mobile').val();
            /*if(!phone_reg.test(mobile) && mobile !=''){
                var lay_cont=gettext('联系电话格式不正确');
                lay_tips(lay_cont);
                return;
            }*/
            var email=$('#email').val();
            if(!email_reg.test(email) && email !=''){
                var lay_cont=gettext('邮箱格式不正确');
                lay_tips(lay_cont);
                return;
            }
            var password=$('#password').val();
            if(password==''){
                var lay_cont=gettext('控制台密码不能为空');
                lay_tips(lay_cont);
                return;
            }
            if(!password_reg.test(password)){
                var lay_cont=gettext('密码必须6到12位');
                lay_tips(lay_cont);
                return;
            }

        }else if(parent_oblique[2]=='admin_group_create'){   //新建角色
            var name=$('#name').val();
            if(name==''){
                var lay_cont=gettext('角色不能为空');
                lay_tips(lay_cont);
                return;
            }

        }
        document.getElementById('lay_form').style.display='none';
        document.getElementById('lay_second').style.display='block';
        $('.progress li:nth-child(2)').addClass('active');
    });


    form.on('submit(step_pre)',function(){ // 上一步
        document.getElementById('lay_form').style.display='block';
        document.getElementById('lay_second').style.display='none';
        $('.progress li:nth-child(2)').removeClass('active');
    });

    form.on('submit(step_third)',function(){    //下一步
        document.getElementById('lay_second').style.display='block';
        document.getElementById('lay_last').style.display='none';
        $('.progress li:nth-child(3)').removeClass('active');
    })

    /*document.getElementById("step_third").onclick = step_third;
    function step_third(){

    }
*/


    form.on('submit(add_permissions)',function() {   ////添加操作权限
        var get_txt=gettext('添加操作权限');
        add_permissions(get_txt);
    });
    $(document).on('click','.edit_xs',function(){    //编辑操作权限
        var edit_xs_this=$(this).parents('tr');
        var server_td_first=edit_xs_this.find('.server_td').eq(0).attr('id');
        var server_td_second=edit_xs_this.find('.server_td').eq(1).attr('id');
        server_td_second=server_td_second.split(',')
        var get_txt=gettext('编辑操作权限');
        add_permissions(get_txt,server_td_first,server_td_second,'edit',edit_xs_this);
    });

    // document.getElementById("add_permissions").onclick = add_permissions;
    // var perm_type_in=perm_type;
    var products_list ='';      //选择服务列表
    for(var perm_type_in in perm_type){
        var perm_data=perm_type[perm_type_in];
        products_list+='<option value="'+perm_data.id+'">'+gettext(perm_data.name)+'</option>'
    }
    function add_permissions(get_txt,server_td_first,server_td_second,oper,xs_this){
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
            '        <input type="radio" name="operation" lay-filter="operation" value="所有操作" title="'+gettext('所有操作')+'" checked="">' +
            '        <input type="radio" name="operation" lay-filter="operation" value="特定操作" title="'+gettext('特定操作')+'">' +
            '       </div>' +
            '       <div class="layui-input-block spe_operation" style="display: none;">' +
                        '<div class="select_div" style="display: inline-block">' +
                        '     <label id="select_all" class="select_label" style="margin-bottom: 0;" for=""><input readonly="readonly" value="" placeholder="'+gettext('请选择')+'" type="text"><i class="down"></i></label>' +
                        '     <div class="select_show">' +
                                '<div class="layui-input-block checkbox_a" id="checkbox_user">' +

                                '</div>'+
                                '<div class="layui-input-block">' +
                                '      <button class="checkBtn fl" id="determine" lay-submit lay-filter="determine">'+gettext("确定")+'</button>' +
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
                    if(operation[i].value == '所有操作' && operation[i].checked){

                        for(var j=0;j<perm_type.length;j++){
                            perm_value.push(perm_type[j].value);
                            perm_value=[gettext('所有操作')];
                            perm_id.push(perm_type[j].id);
                        }
                    }else if(operation[i].value == '特定操作' && operation[i].checked){
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
                       'perm_id': perm_id,
                       'products_value': products_value,
                    }

                var server_list='<tr>'+
                        '<td class="server_td" id="'+products_value+'">'+products_title+'</td>' +
                        '<td class="server_td" id="'+perm_id+'">'+perm_value+'</td>' +
                        '<td><a class="layui-btn  layui-btn-xs edit_xs" lay-event="edit">'+gettext('编辑')+'</a><a class="layui-btn  layui-btn-xs del" lay-event="del">'+gettext('删除')+'</a></td>'
                        // '<td class="server_td">'+add_input[i]+'</td>' +
                    '</tr>';

                // $('#server_tbody').append(server_list);
                form.render();
                layer.close(index_ado);

                if(oper == 'edit'){
                    xs_this.replaceWith(server_list);
                }else{
                    $('#server_tbody').append(server_list);
                }
                table_list
                return

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


        var products_data = function(this_perm,server_td_second,oper){

            var operation_list='';
            for(var perm_all  in perm){

                if(perm_all==this_perm){
                    var perm_all=perm[perm_all]
                    for(var operation in perm_all){
                        var operation=perm_all[operation];
                        if(operation.id != 'client_api_info') {
                            operation_list += '<input id="' + operation.id + '" title="' + gettext(operation.name) + '" type="checkbox" name="perm_type" value="' + operation.name + '" lay-skin="primary">';
                        }
                    }
                    if(oper == 'edit' && perm_all.length != server_td_second.length){
                        $('input[name="operation"]').each(function(){
                            if($(this).val() == '特定操作'){
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
        /*form.on('radio(operation)', function(data){
           if(data.value==gettext('特定操作')){
               $('.spe_operation').show();
           }else{
               $('.spe_operation').hide();
           }
        });
        form.on('select(operation)', function(data){
           if(data.value==gettext('特定操作')){
               $('.spe_operation').show();
           }else{
               $('.spe_operation').hide();
           }
        });*/

        form.on('radio(operation)', function(data){
           if(data.value=='特定操作'){
               if(oper == 'edit'){
                   // server_td_second;
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
            var td_List = $("#server_tbody .server_td");
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

    $(document).on('click','#server_tbody .del',function(){   //删除操作权限
        $(this).parents('tr').remove();

    });
    $(document).on('click','#authority_tbody .del',function(){   //删除操作权限
        var authority_tbody_length=$('#authority_tbody tr').length;
        if(authority_tbody_length == 1){
            lay_tips(gettext('操作权限不能为空'));
        }else{
            $(this).parents('tr').remove();
        }
    });


    //页面数据
    function data_aggregation(){
        var username=$('#username').val();   //新建用户
        var company=$('#company').val();
        var contacts=$('#contacts').val();
        var mobile=$('#mobile').val();
        var email=$('#email').val();
        var password=$('#password').val();
        var user_id='';
        var user_value='';

        // var access_id='';
        var access_value=[];
        var access_type = document.getElementsByName('access_type');
        for(var i=0;i<access_type.length;i++){
            if(access_type[i].checked){
                access_value.push[access_type[i].value];
            }

        }
        if(parent_oblique[2]=='create_parent_user'){
            if(document.getElementById('is_api').checked==true){
               var is_api='1'
            }else{
               var is_api='0'
            }

            if(document.getElementById('is_active').checked){
               var is_active='1';
            }else{
               var is_active='0'
            }
        }

        var name_val=$('#name').val();   //新建角色
        var describe=$('#describe').val();
        var remarks=$('#remarks').val();

        var authority_arr=[];   //操作权限
        var td_List = $("#authority_tbody tr .server_td");
        var td_length = $('#authority_tbody .server_td').length;
        for(var j=0;j<td_length;j++){
            var td_Arr = td_List.eq(j).attr('id');
            if(td_Arr !=''){
               authority_arr+=td_Arr+',';
            }
        }
        var authority_split=authority_arr.split(',');
        authority_split.pop();


        var role_list={
               'username': username,
               'company': company,
               'contacts': contacts,
               'mobile': mobile,
               'email': email,
               'user_id': user_id,
               'user_value':user_value,
               'password':password,
               'perm':authority_split,
               'name':name_val,
               'describe':describe,
               'remarks':remarks,
               'is_api':is_api,
               'is_active':is_active
        }
        return role_list;
    }

    form.on('submit(step_next)',function(){  // 下一步

        $('.progress li:nth-child(3)').addClass('active');

        var table_tr_length=$('#server_tbody tr').length;
        if(table_tr_length==0){
            var lay_cont=gettext('操作权限不能为空');
            lay_tips(lay_cont);
            return;
        }
        var server_tbody_html=$('#server_tbody').html();
        $('#authority_tbody').html(server_tbody_html);
        $('#authority_tbody .edit_xs').remove();
        var aggregation=[data_aggregation()];

        table.render({
            elem: '#role_table'
            ,data:aggregation
            ,cols: [cols]
            , even: true //开启隔行背景
            ,cellMinWidth: 80
            ,done:function(){

            }
        });
        /*table.render({
            elem: '#role_table'
            ,data:aggregation
            ,cols: [cols]
            ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
            ,done:function(res, curr, count){

            }
        });*/
        table.render();
        document.getElementById('lay_form').style.display='none';
        document.getElementById('lay_second').style.display='none';
        document.getElementById('lay_last').style.display='block';
    });

    form.on('submit(step_over)',function() {   //完成
        var aggregation = data_aggregation();

        if (parent_oblique[2] == 'create_parent_user') {     //新建用户
            var data = {
                username: aggregation.username,
                company: aggregation.company,
                linkman: aggregation.contacts,
                mobile: aggregation.mobile,
                email: aggregation.email,
                password: aggregation.password,
                is_api: aggregation.is_api,
                is_active: aggregation.is_active,
                perm: aggregation.perm,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            }

        } else if (parent_oblique[2] == 'admin_group_create') {   //新建角色
            var data = {
                name: aggregation.name,
                desc: aggregation.describe,
                remark: aggregation.remarks,
                perm_list: aggregation.perm,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            }
        }

        $.ajax({
            type: "POST",
            url: '/base/ajax/' + ajax_list + '/',
            data: data,
            async: false,
            success: function (res) {
                if (res.status) {
                    var url_upload = '/base/' + navigation_url + '/page/';
                    layui_nav_each(url_upload, url_upload);
                } else {
                    res_msg(res);
                }
            }
        });
    })

});
