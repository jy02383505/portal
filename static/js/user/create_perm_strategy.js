var parent_href=window.parent.location.href;  //浏览器url
var parent_url=parent_href.split('=');
var ajax_list='';
var navigation_url='';
var role_group_id='';
console.log(role_group_id);
if(parent_url[1] !='/base/parent_create_perm_strategy/page/'){
    console.log(111);
    var username=$('#username').text();
    var parent_id=parent_url[1].split('/');
    role_group_id=parent_id[parent_id.length-2];
    ajax_list='edit_perm_strategy';  //页面列表
    navigation_url='parent_get_perm_strategy';  //操作列表
    if($('#strategy_type').text()==internation_trans.custom_strategy){
        document.getElementById("add_permissions").onclick = add_permissions;
    }

}else{
    console.log(222);
    ajax_list='create_perm_strategy';  //页面列表
    navigation_url='parent_get_perm_strategy';  //操作列表
    var obj_id='';
    document.getElementById("add_permissions").onclick = add_permissions;
}

console.log(ajax_list);
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

    if(parent_url[1] !='/base/parent_create_perm_strategy/page/'){   //管理员详情

        var server_list='';
        var sums_all=[];
        for(var i=0;i<parent_perm_type.length;i++){
            var user_perm_id=parent_perm_type[i].id;
            var user_perm_value=parent_perm_type[i].name;
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
            for(var perm_all  in parent_perm){
                if(perm_all==user_perm_type[i].id){
                    console.log(perm_all);
                    var perm_all=parent_perm[perm_all];
                    for(var operation in perm_all){
                        var operation=perm_all[operation];
                        sums_all[i].perm_id += operation.id+',';                                   //流量和
                        sums_all[i].perm_value += operation.name+',';
                    }
                }
            }

        }
        console.log(sums_all);
        // str.substr(str.length-1,1)
        for(var i=0;i<sums_all.length;i++){
            console.log(sums_all[i].perm_id);
            if(sums_all[i].perm_value[sums_all[i].perm_value.length-1]==',' && sums_all[i].perm_id !=''){

                var perm_value=sums_all[i].perm_value.substr(0,sums_all[i].perm_value.length-1);
            }else{
                var perm_value='';
            }
            if(sums_all[i].perm_id[sums_all[i].perm_id.length-1]==',' && sums_all[i].perm_id !=''){

                var perm_id=sums_all[i].perm_id.substr(0,sums_all[i].perm_id.length-1);
            }else{
                var perm_id='';
            }
            if($('#strategy_type').text()==internation_trans.custom_strategy){
                var a_del='<a class="layui-btn layui-btn-danger layui-btn-xs del" lay-event="del">'+internation_trans.del+'</a>'
            }else{
                var a_del='';
            }

            server_list +='<tr><td class="server_td" id="'+sums_all[i].user_perm_id+'">'+sums_all[i].user_perm_value+'</td>'+
            '<td class="server_td" id="'+perm_id+'">'+perm_value+'</td>'+
            '<td class="server_td" id=""></td>' +
            '<td>'+a_del+'</td></tr>'
        }
        $('#server_tbody').html(server_list);
    }

    //添加操作权限
    console.log(parent_url[1]);
    console.log($('#strategy_type').text());
    /*if(parent_url[1] !='/base/parent_create_perm_strategy/page/' && $('#strategy_type').text()==internation_trans.custom_strategy){
        document.getElementById("add_permissions").onclick = add_permissions;
    }else{
        // document.getElementById("add_permissions").onclick = add_permissions;
    }*/
    if(parent_url[1] =='/base/parent_create_perm_strategy/page/'){
        document.getElementById("add_permissions").onclick = add_permissions;
    }else{
        // document.getElementById("add_permissions").onclick = add_permissions;
    }

    // var perm_type_in=perm_type;
    var products_list ='';      //选择服务列表
    for(var perm_type_in in user_perm_type){
        var perm_data=user_perm_type[perm_type_in];
        products_list+='<option value="'+perm_data.id+'">'+perm_data.name+'</option>'
    };
    function add_permissions(){
        var content='<div class="layui-form" id="add_jurisdiction">' +
            '     <div class="layui-form-item">' +
            '      <label class="layui-form-label">'+internation_trans.is_services+'</label>' +
            '      <div class="layui-input-block">' +
            '      <select id="products" name="interest" lay-filter="products">' +
            '        <option value="-1" selected>'+internation_trans.please_choose+'</option>' + products_list+
            '      </select>' +
            '      </div>'+
            '     </div>' +
            '     <div class="layui-form-item">' +
            '       <label class="layui-form-label">'+internation_trans.operation_name+'</label>' +
            '       <div class="layui-input-block">' +
            '        <input type="radio" name="operation" lay-filter="operation" value="'+internation_trans.all_operation+'" title="'+internation_trans.all_operation+'" checked="">' +
            '        <input type="radio" name="operation" lay-filter="operation" value="'+internation_trans.spe_operation+'" title="'+internation_trans.spe_operation+'">' +
            '       </div>' +
            '       <div class="layui-input-block spe_operation" style="visibility:hidden;">' +
                        '<div class="select_div" style="display: inline-block">' +
                        '     <label id="select_all" class="select_label" style="margin-bottom: 0;" for=""><input readonly="readonly" value="" placeholder="'+internation_trans.please_choose+'" type="text"><i class="down"></i></label>' +
                        '     <div class="select_show">' +
                                '<div class="layui-input-block checkbox_a" id="checkbox_user">' +

                                '</div>'+
                                '<div class="layui-input-block">' +
                                '      <button class="checkBtn fl" id="determine" lay-submit lay-filter="determine">'+internation_trans.sure+'</button>' +
                                '</div>'+
                              '</div>'+
                        '</div>'+
                    '</div>'+
            '       <div class="layui-input-block" style="display: none;">' +
            '        <button class="checkBtn fl" lay-filter="button_layero" id="button_sub" ></button>' +
            '       </div>'+
            '     </div>'+
            '     <div class="layui-form-item">' +
            '       <label class="layui-form-label">'+internation_trans.resources+'</label>' +
            '       <div class="layui-input-block">' +
            '        <input type="radio" name="resources" lay-filter="resources" value="'+internation_trans.all_resources+'" title="'+internation_trans.all_resources+'" checked="">' +
            '        <input type="radio" name="resources" lay-filter="resources" value="'+internation_trans.spe_resources+'" title="'+internation_trans.spe_resources+'">' +
            '       </div>' +
            '       <div class="layui-input-block spe_resources" style="visibility:hidden;">' +
                        '<div class="select_div" style="display: inline-block">' +
            '               <select name="role" id="role" lay-filter="role">' +
            '                    <option value="">'+internation_trans.please_choose+'</option>' +
            '               </select>'+
                        '</div>'+
                    '</div>'+
            '       <div class="layui-input-block" style="display: none;">' +
            '        <button class="checkBtn fl" lay-filter="button_layero" id="button_sub" ></button>' +
            '       </div>'+
            '     </div>'+
            '</div>';
        layer.open({
            type: 1
            ,title: internation_trans.add_operation
            ,area: ['500px', '460px']
            ,btnAlign: 'l'
            ,shade:0
            ,id: 'permissions'
            ,content:content
            ,btn: [internation_trans.creation]
            ,yes: function(index_ado){

                var products=$('#products').val();
                var products_value=[];
                var products_title=[]
                if(products=='-1'){
                    var lay_cont=internation_trans.cannot_empty;
                    lay_tips(lay_cont);
                    return;
                }else{
                    products_title=[$('#products option:selected').text()];
                    products_value=[$('#products').val()];
                }
                /*else if(products=='所有产品'){
                    var products = document.getElementById('products');
                    for(var i=2;i<products.length;i++){
                        products_value.push(products[i].value);
                        // products_title.push(products[i].innerText);
                        products_title=['所有产品'];
                    }
                }*/

                var operation_val='';
                var operation = document.getElementsByName('operation');  //caozuo
                var perm_type=document.getElementsByName('perm_type');
                var perm_value=[];
                var perm_id=[];
                for(var i=0;i<operation.length;i++){
                    if(operation[i].value == internation_trans.all_operation && operation[i].checked){

                        for(var j=0;j<perm_type.length;j++){
                            perm_value.push(perm_type[j].value);
                            perm_value=[internation_trans.all_operation];
                            perm_id.push(perm_type[j].id);
                        }
                    }else if(operation[i].value == internation_trans.spe_operation && operation[i].checked){
                        for(var j=0;j<perm_type.length;j++){
                            if(perm_type[j].checked){
                                perm_value.push(perm_type[j].value);
                                perm_id.push(perm_type[j].id);
                            }
                        }
                    }
                }

                var resources = document.getElementsByName('resources');
                var given_resources=document.getElementsByName('given_resources');   //资源
                var resources_value=[];
                var resources_id=[];
                for(var i=0;i<resources.length;i++){
                    if(resources[i].value == internation_trans.all_resources && resources[i].checked){

                        for(var j=0;j<given_resources.length;j++){
                            resources_value.push(given_resources[j].value);
                            resources_value=[internation_trans.all_resources];
                            resources_id.push(given_resources[j].id);
                        }
                    }else if(resources[i].value == internation_trans.spe_resources && operation[i].checked){
                        for(var j=0;j<given_resources.length;j++){
                            if(given_resources[j].checked){
                                resources_value.push(given_resources[j].value);
                                resources_id.push(given_resources[j].id);
                            }
                        }
                    }
                }
                if(operation_val==internation_trans.spe_operation && $('#operation_name').val()==''){
                    var lay_cont=internation_trans.operation_cannot_empty;
                    lay_tips(lay_cont);
                    return;
                }
                if(operation_val==internation_trans.spe_resources && $('#operation_name').val()==''){
                    var lay_cont=internation_trans.resources_cannot_empty;
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
                        '<td class="server_td" id="'+resources_id+'">'+resources_value+'</td>' +
                        '<td><a class="layui-btn layui-btn-danger layui-btn-xs del" lay-event="del">'+internation_trans.del+'</a></td>'
                        // '<td class="server_td">'+add_input[i]+'</td>' +
                    '</tr>';

                $('#server_tbody').append(server_list);
                $('#authority_tbody').append(server_list);
                form.render();
                layer.close(index_ado);

                if(parent_url[1] !='/base/parent_create_perm_strategy/page/'){
                    var data={
                        name: username,
                    };
                    data_aggregation(data,index_ado);
                }

                // data_aggregation(table_list);

            }

        });


        form.on('select(products)', function(obj){   //选择服务
            var operation_list='';
            var this_perm=obj.value;
           for(var perm_all  in perm){

                if(perm_all==this_perm){
                    var perm_all=perm[perm_all]
                    for(var operation in perm_all){
                        var operation=perm_all[operation];
                         operation_list+='<input id="'+operation.id+'" title="'+operation.name+'" type="checkbox" name="perm_type" value="'+operation.name+'" lay-skin="primary">';
                    }
                }else if(this_perm=='所有产品'){
                    var perm_all=perm[perm_all]
                   for(var operation in perm_all){
                        var operation=perm_all[operation];
                         operation_list+='<input id="'+operation.id+'" title="'+operation.name+'" type="checkbox" name="perm_type" value="'+operation.name+'" lay-skin="primary">';
                   }
                }
                //
            }

           $('#checkbox_user').html(operation_list);
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
                    perm_type_list.perm_type_value += perm_type[i].value+','
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
            $(this).addClass('current')
        });
        $('.select_label').click(function(e){    //弹窗
            if($(this).parent().hasClass('current')){
                $(this).parent().removeClass('current')
            }else{
                $(this).parent().addClass('current')
            }
            e.stopPropagation();

        });
        document.onclick = function(){
            $('.select_div').removeClass('current');
        };


        form.on('radio(operation)', function(data){
           if(data.value=='特定操作'){
               $('.spe_operation').css('visibility','visible');
           }else{
               $('.spe_operation').css('visibility','hidden');
           }
        });
        form.on('radio(resources)', function(data){
           if(data.value=='特定资源'){
               $('.spe_resources').css('visibility','visible');
           }else{
               $('.spe_resources').css('visibility','hidden');
           }
        });

        var authority_arr=[];   //操作权限
        if($('#permissions_table .server_td').length !=0){
            var td_List = $("#permissions_table tr .server_td");
            var td_length = $('#permissions_table .server_td').length;
            for(var j=0;j<td_length;j++){
                var td_Arr = td_List.eq(j).attr('id');
                if(td_Arr !=''){
                   authority_arr+=td_Arr+',';
                }
            }
            var authority_split=authority_arr.split(',')
            $('#products option').each(function(){
                for(var j=0;j<authority_split.length;j++){

                    if(authority_split[j]==$(this).val()){
                        $(this).attr('disabled','disabled');
                        // $(this).attr('selected',true);
                    }
                }
            });

        }
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
            ,content: internation_trans.delete_service
            ,btn: [internation_trans.yes_del,internation_trans.no_del]
            ,yes: function(index_ado){
                obj.parents('tr').remove();
                if(parent_url[1] !='/base/parent_create_perm_strategy/page/'){

                    var data={
                        name: username,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    };
                    data_aggregation(data,index_ado);
                }
                layer.close(index_ado);


            }
        });
        form.render();
    });

    if(parent_url[1]=='/base/parent_create_perm_strategy/page/'){
        document.getElementById("sure").onclick = sure;
        function sure(){
            var username=$('#username').val();   //新建用户
            var describe=$('#describe').val();

            var role_list={
                   'name': username,
                   'describe': describe,
            };

            data_aggregation(role_list);
            // return role_list;
        }
    }

    //页面数据
    function data_aggregation(aggregation){
        var authority_arr=[];   //操作权限
        var td_List = $("#permissions_table tr .server_td");
        var td_length = $('#permissions_table .server_td').length;

        var authority_split='';
        if(td_length !=0){
            for(var j=0;j<td_length;j++){
                var td_Arr = td_List.eq(j).attr('id');
                if(td_Arr !=''){
                   authority_arr+=td_Arr+',';
                }
            }
            if(authority_arr.substr(authority_arr.length-1)==','){
                authority_arr=authority_arr.substr(0,authority_arr.length-1);
            }
            authority_split=authority_arr.split(',');

        }
        console.log(aggregation);
        $.ajax({
            type: "POST",
            url: '/base/ajax/'+ajax_list+'/',
            data:{
                name: aggregation.name,
                remark: aggregation.describe,
                obj_id:role_group_id,
                perm:authority_split,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                console.log(res);
                if(res.status){
                    $('.layui-nav a',parent.document).each(function(){
                        var url_a=$(this).attr('href');
                        var url_split=url_a.split('=');
                        if(url_split[1]=='/base/'+navigation_url+'/page/') {
                            $("#container", parent.document).attr('src', '/base/' + navigation_url + '/page/');
                            $("#container", parent.document).attr('url', url_split[2]);
                            window.parent.location.href = parent_url[0] + '=/base/' + navigation_url + '/page/=' + url_split[2];
                        }
                    })
                }else{
                    lay_tips(res.msg);

                }
            }
        });
    }



    /*function sure(){
        var aggregation=data_aggregation();

    }
*/
});
