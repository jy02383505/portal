
var create_binding_ajax='';
var url='/base/admin_bind_cms_parent/page/';
var details='/base/admin_cms_details/page/';    //详情页面
if(parent_oblique[2] == 'admin_cms_details'){
    create_binding_ajax='/base/ajax/admin_binding_user_contract/';
}else if(parent_oblique[2] == 'admin_create_binding'){
    // create_binding_ajax='/base/ajax/admin_cdn_create_domain/';
    create_binding_ajax='/base/ajax/admin_user_binding/';
}


var parent_href=window.parent.location.href;  //浏览器url
var parent_url=parent_href.split('=');
var binding_url='admin_bind_cms_parent';
var contract_array=contract;

layui.use(['form','table','element','layer'], function(){
    var form = layui.form;
    var table = layui.table;
    var layer=layui.layer;

    if(parent_oblique[2] == 'admin_cms_details') {     //合同
        var contract_list='';
        for (var contract  in contract_array) {

            var contract_in = contract_array[contract].product;
            var product_name_array = [];
            var product_code_array = [];
            for (var contract_pro in contract_in) {
                product_name_array.push(contract_in[contract_pro].product_name);
                product_code_array.push(contract_in[contract_pro].product_code);
            }
            contract_list += '<tr><td class="cache_td"><span>' + contract + '</span></td>' +
                '<td class="cache_td"><span>' + product_name_array + '</span></td>' +
                '<td class="cache_td" style="display: none;"><span>' + product_code_array + '</span></td>' +
                '<td class="cache_td"><span>' + contract_array[contract].start_time + '</span></td>' +
                '<td class="cache_td"><span>' + contract_array[contract].end_time + '</span></td>'+
                '<td><span></span></td>' +
                 '<td><div class="cache_btn"><a class="layui-btn layui-btn-xs layui_edit" lay-event="edit">'+gettext('解绑')+'</a>' +
                     '</div></td>'

        }
        $('#server_tbody').html(contract_list);
    }


    form.on('select(customer_account)', function(obj){   //切换用户
       for(var user in user_list){
            var user=user_list[user];
            if(user.user_id==obj.value){
                $('#user_id').text(user.user_id);
                $('#type_name').text(gettext(user.type_name));
                if(user.is_active==true){
                    $('#is_active').text(gettext('启用'));
                }else{
                    $('#is_active').text(gettext('禁用'));
                }
                $('#company').text(gettext(user.company));
            }
        }
    });

    form.on('submit(lay_add_contract)', function() {   //新增合同信息
      var customer_val=$('#customer_account option:selected').val();
      if(customer_val == ''){
          lay_tips(gettext('请选择用户账号'));
          return
      }
      var content='<div class="layui-form con" id="add_jurisdiction">' +
            '<div class="layui-form-item" style="text-align: left;">' +
            ' <label class="layui-form-label" style="padding-left:0;width:66px;">'+gettext("合同编号")+'</label>'+
            '    <input type="text" id="contract_name" value="" name="contract_name" placeholder="">'+
            '    <button class="layui-btn-blue layui-btn" style="margin-left:80px;" lay-submit lay-filter="search_contract_infor" id="search_channel_id">'+gettext('查询')+'</button>'+
            '    <p class="remark_p" style="padding-left: 66px;">'+gettext('输入合同编号查询合同信息')+'</p>'+
            '</div>' +
            '<div class="layui-form-item" id="sales_infor" style="text-align: left;display: none;">' +
            '    <div class="layui-layer-title" style="cursor: move;">'+gettext('合同信息')+'</div>'+
            '<div class="contract_infor" style="padding-bottom: 58px;">'+
            '<div class="layui-form-item">' +
            '   <label class="layui-form-label">'+gettext('合同编号：')+'</label>' +
            '   <div class="layui-input-block" id="contract_number"></div>' +
            '</div>'+
            '<div class="layui-form-item">' +
            '   <label class="layui-form-label">'+gettext('合同开始日期：')+'</label>' +
            '   <div class="layui-input-block" id="con_start_time"></div>' +
            '</div>'+
            '<div class="layui-form-item">' +
            '   <label class="layui-form-label">'+gettext('合同结束日期：')+'</label>' +
            '   <div class="layui-input-block" id="con_end_time"></div>' +
            '</div>'+
            '<div class="layui-form-item tab_border" style="padding-bottom: 10px;">' +
            '   <label class="layui-form-label">'+gettext('合同状态：')+'</label>' +
            '   <div class="layui-input-block" id="con_status"></div>' +
            '</div>'+
            '<h5 class="mian_h5" style="font-size: 14px;padding:10px 0 0;">'+gettext('可选产品名称')+'</h5>'+
            '<table class="layui-hide" id="product_name" lay-filter="product_name"></table>'+
            '</div></div>'+
            '</div>';
      layer.open({
        type: 1
        ,title: gettext('新增合同信息')
        ,area: ['600px', '720px']
        ,shade:0
        ,btnAlign: 'c'
        ,id: 'tips_layer'
        ,content: content
        ,btn: [gettext('确定'),gettext('取消')]
        ,success:function(){

        }
        ,yes: function(index){
            var username='';
            var contract_name=$('#contract_number').text();
            var con_start_time=$('#con_start_time').text();
            var con_end_time=$('#con_end_time').text();
            var con_status=$('#con_status').text();
            var product_name_list=[];
            var product_code_list=[];
            var product_array=[];
            var layTableCheckbox = document.getElementsByName('layTableCheckbox');
            for(var i=1;i<layTableCheckbox.length;i++){
                if(layTableCheckbox[i].checked && layTableCheckbox[i].disabled != true){
                    var parent_node=layTableCheckbox[i].parentNode.parentNode.parentNode;
                    product_array[i]={
                        'product_name': '',
                        'product_code': ''

                    };
                    product_code_list.push(parent_node.childNodes[1].innerText);
                    product_name_list.push(parent_node.childNodes[0].innerText);
                    product_array[i].product_code += parent_node.childNodes[1].innerText;
                    product_array[i].product_name += parent_node.childNodes[0].innerText;


                }
            }
            product_array=removeEmpty(product_array);
            if(product_array == ''){
                lay_tips(gettext('请添加合同信息'));
                return;
            }
            if(parent_oblique[2] == 'admin_cms_details'){
                username=$('#user_name span').text();
                $.ajax({                                      //创建CMS绑定关系
                    type: "POST",
                    // url: '/base/ajax/admin_user_binding/',
                    url:create_binding_ajax,
                    data: {
                        contract_name:contract_name,
                        username:username,
                        start_time:con_start_time,
                        end_time:con_end_time,
                        product_list:JSON.stringify(product_array),
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    },
                    dataType : 'json',
                    error:function(){
                        lay_tips(gettext('通讯异常'));
                    },
                    async:false,
                    success: function(res){
                        if(res.status){
                            layer.close(index);
                            window.location.reload();
                        }else{
                            if(res.msg !='' && res.msg != undefined){
                                lay_tips(res.msg);
                            }else{
                                lay_tips(gettext('通讯异常'));
                            }

                        }
                    }
                })
            }else{

                var caching_rules_list ='<tr><td class="cache_td"><span>'+ contract_name+'</span></td>' +
                 '<td class="cache_td"><span>'+product_name_list+'</span></td>' +
                '<td class="cache_td" style="display: none;"><span>'+product_code_list+'</span></td>' +
                 '<td class="cache_td"><span>'+con_start_time+'</span></td>' +
                 '<td class="cache_td"><span>'+con_end_time+'</span></td>' +
                 '<td><span>'+con_status+'</span></td>' +
                 '<td>' +
                 '<div class="cache_btn"><a class="layui-btn layui-btn-xs layui_edit" lay-event="edit">'+gettext('解绑')+'</a>' +
                 '</div></td></tr>';
                var server_tbody_length=$('#server_tbody tr').length;
                if(server_tbody_length >0){
                    $('#server_tbody').append(caching_rules_list);
                }else{
                    $('#server_tbody').html(caching_rules_list);
                }
                layer.close(index);
            }
        }
      });
      if(lan == 'en'){
        $('.layui-form-label').width(78)
        $('.contract_infor .layui-form-label').width(100)
        $('.remark_p').css('padding-left','88px');
      }

    });


    $(document).on('click','.layui_edit',function(){  //解绑
      var layui_edit_this=$(this);

      layer.alert(gettext('确定解除当前选中账号的绑定关系？'), {
          title:gettext('解绑'),
          icon: 0,
          area:['400px','170px'],
          shade:0,
          btn:[gettext('确定'),gettext('取消')],
          btnAlign:'c',
          yes:function(index) {
              if(parent_oblique[2] == 'admin_cms_details'){
                  var user_name=$('#user_name').text();
                  var username=user_name.replace(/\ +/g,"").replace(/[\r\n]/g,"");
                  var contract_name=layui_edit_this.parents('tr').children('td:first-child').text()
                  $.ajax({
                    type: "POST",
                    url: '/base/ajax/admin_user_relieve_contract/',
                    data: {
                        contract_name:contract_name,
                        username:username,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    },
                    dataType : 'json',
                    error:function(){
                        lay_tips(gettext('通讯异常'));
                    },
                    async:false,
                    success: function(res){
                        if(res.status){
                            layer.close(index);
                            window.location.reload();
                        }else{
                            if(res.msg !='' && res.msg != undefined){
                                lay_tips(res.msg);
                            }else{
                                lay_tips(gettext('通讯异常'));
                            }

                        }
                    }
                  })

              }else{
                  layui_edit_this.parents('tr').remove();
                  layer.close(index);
              }

          }
      });

    });


    var product_list='';
    form.on('submit(search_contract_infor)', function() {  //查找合同

        var username='';
        if(parent_oblique[2] == 'admin_cms_details'){
            username=$('#user_name').text();
            username=username.replace(/\ +/g,"").replace(/[\r\n]/g,"");
        }else{
            username=$('#customer_account option:selected').text();
        }
        var contract_name=$('#contract_name').val();
        $.ajax({                                      //添加频道
            type: "POST",
            url: '/base/ajax/admin_sync_contract_info/',
            data: {
                contract_name:contract_name,
                username:username,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            // dataType : 'json',
            error:function(){
                lay_tips(internation_trans.communication);
            },
            // async:false,
            success: function(res){
                if(res.status){
                    $('#contract_number').text(contract_name);
                    $('#con_start_time').text(res.start_time);
                    $('#con_end_time').text(res.end_time);
                    if(res.is_effective==true){
                        var con_status=gettext('有效');
                    }else{
                        var con_status=gettext('无效');
                    }
                    var product_list=res.product_list;

                    $('#con_status').text(con_status);
                    table.render({
                        elem: '#product_name'
                        ,height: 192
                        ,data: product_list
                        ,even: true //开启隔行背景
                        ,cols: [[ //表头
                             {field: 'product_name', title: gettext('产品名称'), width:'80%'}
                             ,{field: 'product_code', title: gettext('产品ID'), hide:true, width: 80}
                             ,{type: 'checkbox',field: 'checkbox'}
                        ]]
                        ,done:function(){
                            $("[data-field = 'checkbox']").children().each(function (index) {
                                if(index==0){
                                    $(this).css("display","none");
                                }
                            });
                            $("[data-field = 'product_name']").children().each(function (index) {
                                $(this).text(gettext($(this).text()))
                            });
                            $("[data-field='product_code']").css("display","none");
                            $('#sales_infor').show();
                            if(con_status == gettext('已到期')){
                                $("[data-field = 'checkbox'] input[type='checkbox']").prop('disabled',true);
                                form.render();
                            }
                        }
                    });
                    table.render();
                    layer.close();
                    // window.location.reload();
                }else{
                    if(res.msg !='' && res.msg != undefined){
                        lay_tips(res.msg);
                    }else{
                        lay_tips(internation_trans.communication);
                    }

                }
            }
        })

    });

    form.on('submit(lay_submit)', function() {   //提交
        var cms_username=$('#cms_username').val();
        var username=$('#customer_account option:selected').text();
        var user_id=$('#customer_account option:selected').val();

        var cache_rule=[];                            //合同信息
        function group(array, subGroupLength) {
              var index = 0;
              var newArray = [];
              while(index < array.length) {
                  newArray.push(array.slice(index, index += subGroupLength));
              }
              return newArray;
        }

        $('.cache_td').each(function(){
            var cache_id=$(this).text();
            cache_rule.push(cache_id);
        });
        var groupedArray = group(cache_rule, 5);
        var contract_list=[];
        for(var cache_in in groupedArray){
            contract_list[cache_in]={
                'contract_name': '',
                'start_time': '',
                'end_time': '',
                'product_list':[]
            };
            contract_list[cache_in].contract_name += groupedArray[cache_in][0];
            contract_list[cache_in].start_time += groupedArray[cache_in][3];
            contract_list[cache_in].end_time += groupedArray[cache_in][4];

            var product_code_array = groupedArray[cache_in][2].split(',');
            var product_name_array = groupedArray[cache_in][1].split(',');
            product_name_array.push(groupedArray[cache_in][1].split(','));

            var product_array_list=[];
            for(var product_array in product_code_array){
                product_array_list[product_array]={
                    'product_name': '',
                    'product_code': ''

                };
                product_array_list[product_array].product_code += product_code_array[product_array];
                product_array_list[product_array].product_name += product_name_array[product_array];
            }

            contract_list[cache_in].product_list = product_array_list;

        }

        $.ajax({                                      //创建CMS绑定关系
            type: "POST",
            // url: '/base/ajax/admin_user_binding/',
            url:create_binding_ajax,
            data: {
                cms_username:cms_username,
                username:username,
                contract_list:JSON.stringify(contract_list),
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            dataType : 'json',
            error:function(){
                lay_tips(gettext('通讯异常'));
            },
            async:false,
            success: function(res){
                if(res.status){
                    // layui_nav_each(add,url);
                    var url_upload=details+user_id+'/';
                    layui_nav_each(url_upload,url);
                }else{
                    if(res.msg !='' && res.msg != undefined){
                        lay_tips(res.msg);
                    }else{
                        lay_tips(gettext('通讯异常'));
                    }
                }
            }
        })

    });

    table.render();
    form.render();

});