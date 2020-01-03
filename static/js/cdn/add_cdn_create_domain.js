var admin_cdn_create_ajax=''; //添加域名接口
var domain_list=''; //域名列表页面
var cert_list_ajax='';    //获取证书

if(is_staff == 'True'){
    domain_list='/cdn/admin_get_domain_list/page/';
    admin_cdn_create_ajax='/cdn/ajax/admin_cdn_create_domain/';
    cert_list_ajax='/cdn/ajax/admin_cdn_get_cert/';
}else if(is_staff == 'False'){
    domain_list='/cdn/client_get_domain_list/page/';
    admin_cdn_create_ajax='/cdn/ajax/client_cdn_create_domain/';
    cert_list_ajax='/cdn/ajax/client_cdn_get_cert/';
}



var default_cache_data=default_cache;
layui.use(['table','form','layer','laypage'], function() {
    var form = layui.form;
    var table = layui.table;
    var layer = layui.layer;

    var cdn_type_last='<tr id="cdn_type_last"><td class="cache_td" id="path"><span>'+ gettext('文件夹')+'</span></td>' +
                     '<td class="cache_td" id="/.*"><span>'+gettext('全部文件')+'</span></td>' +
                     '<td class="cache_td" id="0"><span>0</span><span>'+gettext('秒')+'</span></td>' +
                     '<td><div class="cache_sort"></div>' +
                     '<div class="cache_btn"><a class="layui-btn layui-btn-xs layui_edit" lay-event="edit">'+gettext('编辑')+'</a>' +
                     '<a class="layui-btn layui-btn-xs btn_gray" lay-event="del">'+gettext('删除')+'</a></div></td></tr>';
    var cdn_type_fun=function(data){
        var caching_rules_list='';   //默认缓存规则
        for(var default_cache in default_cache_data){
            if(default_cache==data){
                var default_cache=default_cache_data[default_cache];
                for(var default_cache_in in default_cache){
                    var default_cache_in=default_cache[default_cache_in];

                    var cache_name='';
                    for(var cache in cache_type){
                        var cache=cache_type[cache];
                        if(cache.id==default_cache_in.type){
                            cache_name=cache.name;
                        }
                    }
                    var caching_times='';
                    var select_time='';
                    if(default_cache_in.TTL<60){
                        select_time=gettext('秒');
                        caching_times=default_cache_in.TTL;
                    }else if(default_cache_in.TTL>=60 && default_cache_in.TTL<3600){
                        select_time=gettext('分');
                        caching_times=default_cache_in.TTL/60;
                    }else if(default_cache_in.TTL>=3600 && default_cache_in.TTL<86400){
                        select_time=gettext('小时');
                        caching_times=default_cache_in.TTL/3600;
                    }else if(default_cache_in.TTL>=86400){
                        select_time=gettext('天');
                        caching_times=default_cache_in.TTL/86400;
                    }
                    caching_rules_list +='<tr id="cdn_type_tr"><td class="cache_td" id="'+default_cache_in.type+'"><span>'+ gettext(cache_name)+'</span></td>' +
                     '<td class="cache_td" id="'+default_cache_in.urls+'"><span>'+default_cache_in.urls+'</span></td>' +
                     '<td class="cache_td" id="'+default_cache_in.TTL+'"><span>'+caching_times+'</span><span>'+select_time+'</span></td>' +
                     '<td><div class="cache_sort"><span class="move_down"></span><span class="move_up"></span></div>' +
                     '<div class="cache_btn"><a class="layui-btn layui-btn-xs layui_edit" lay-event="edit">'+gettext('编辑')+'</a>' +
                     '<a class="layui-btn layui-btn-xs layui_del" lay-event="del">'+gettext('删除')+'</a></div></td></tr>';

                }


            }

        }
        $('#cache_tbody').html(caching_rules_list+cdn_type_last);
        table.render();
    }
    form.on('radio(cdn_type)',function(data){   //切换加速类型
        cdn_type_fun(data.elem.id);
    });
    cdn_type_fun($('input[name="cdn_type"]:checked').attr('id'));   //默认加速类型

    form.on('select(username)',function(data){    //切换用户
        user_id=data.value;
        var cdn_type_list='';
        if(data.value != ''){
            for(var user_name in user_list){
                var user_name=user_list[user_name];
                if(user_name.id == data.value){
                    for(var user_cdn in user_name.user_cdn_type){
                        var user_cdn=user_name.user_cdn_type[user_cdn];
                        cdn_type_list += '<input type="radio" name="cdn_type" lay-filter="cdn_type" lay-skin="primary" ' +
                        'id="'+user_cdn.id+'" value="' +user_cdn.check_name + '" title="'+user_cdn.name+'">'
                    }

                }

            }
        }else{
            for(var user_cdn in cdn_type){
                var user_cdn=cdn_type[user_cdn];
                cdn_type_list += '<input type="radio" name="cdn_type" lay-filter="cdn_type" lay-skin="primary" ' +
                'id="'+user_cdn.id+'" value="' +user_cdn.check_name + '" title="'+user_cdn.name+'">'
            }
        }
        $('#cdn_type_id').html(cdn_type_list);
        $('input[name="cdn_type"]').eq(0).prop('checked',true);
        var cdn_type_input=$('input[name="cdn_type"]').attr('id');
        cdn_type_fun(cdn_type_input);
        user_data(user_id);
        form.render();

    });

    function user_data(user_id){
        $.ajax({
            type: "POST",
            url: cert_list_ajax,
            data: {
                user_id:user_id,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            error:function(){
                lay_tips(gettext('通讯异常'));
            },
            success: function(res){
                if(res.status){
                    var cert_list=res.cert_list;
                    var cert_name_list='';
                    for(var cert in cert_list){
                        var cert=cert_list[cert];
                        cert_name_list +='<option value="'+cert.cert_name+'">'+cert.cert_name+'</option>'
                    }
                    $('select[name="cert"]').html('<option value="">'+gettext('请选择')+'</option>'+cert_name_list);
                    // layer.close(index_ado);
                    // window.location.reload();
                }else{
                    res_msg(res);

                }

            }
        })
    }
    if(is_staff == 'False'){
        user_data(user_id) //客户端
    }

    form.on('checkbox(protocol_type)',function(data){    //切换协议类型
        var selection_cert=document.getElementById('selection_cert');
        if(data.value == 'https' && data.elem.checked){
            selection_cert.style.display='block';
        }else if(data.value == 'https' && !data.elem.checked){
            selection_cert.style.display='none';
        }
    });



    form.on('submit(lay_submit)',function(){    //添加域名
        var user_id=$('select[name="username"] option:selected').val();
        if(user_id == ''){
            lay_tips(gettext('用户名不能为空'));
            return;
        }else if(user_id == undefined){
            user_id='';
        }
        var cert=$('select[name="cert"] option:selected').val();
        var contract_name='';
        if(is_staff == 'True'){
            for(var user in user_list){
                var user=user_list[user];
                if(user.id == user_id){
                    contract_name=user.contract_name;
                }
            }
        }else{
            contract_name=user_list.contract_name;
        }

        var domain=$('#domain').val();  //加速域名
        var cdn_type=$('input[name="cdn_type"]:checked').val();  //加速类型
        // var protocol_type=$('input[name="protocol_type"]').val();  //协议类型
        var protocol_type=document.getElementsByName('protocol_type');
        var protocol=[];
        for(var i=0;i<protocol_type.length;i++){
            if(protocol_type[i].checked){
                protocol.push(protocol_type[i].value);
            }
        }

        var src_type=$('input[name="src_type"]:checked').val();  //回源方式
        var src_value='';                                //源站地址
        if(src_type=='ip'){
            src_value=$('#src_type_text').val();
        }else{
            src_value=$('#src_type_input').val();

        }

        var src_back_type=$('input[name="src_back_type"]:checked').val();  //备份源站类型
        var src_back_value='';                                //源站地址
        if(src_back_type=='ip'){
            src_back_value=$('#src_back_text').val();
        }else if(src_back_type=='dmn'){
            src_back_value=$('#src_back_input').val();

        }
        if(src_back_value == ''){
            src_back_type=''
        }

        var src_host=$('input[name="domain_src_host"]').val();  //回源host

        if($('input[name="src_back_type"]').is(':checked',true)){    //header配置
            var ignore_cache_control=1;
        }else{
            var ignore_cache_control=0;
        }
        if($('input[name="ignore_query_string"]').is(':checked',true)){    //参数配置
            var ignore_query_string=1;
        }else{
            var ignore_query_string=0;
        }
        var cache_rule=[];                            //缓存规则
        function group(array, subGroupLength) {
              var index = 0;
              var newArray = [];
              while(index < array.length) {
                  newArray.push(array.slice(index, index += subGroupLength));
              }
              return newArray;
        }

        $('.cache_td').each(function(){
            var cache_id=$(this).attr('id');
            cache_rule.push(cache_id);
        });
        var groupedArray = group(cache_rule, 3);
        var cache_array=[];
        for(var cache_in in groupedArray){
            cache_array[cache_in]={
                'type': '',
                'rule': '',
                'ttl': ''
            };
            cache_array[cache_in].type += groupedArray[cache_in][0];
            cache_array[cache_in].rule += groupedArray[cache_in][1];
            cache_array[cache_in].ttl += groupedArray[cache_in][2];
        }

        $.ajax({
            type: "POST",
            url: admin_cdn_create_ajax,
            data: {
                user_id:user_id,
                domain:domain,
                contract_name:contract_name,
                cdn_type:cdn_type,
                protocol:JSON.stringify(protocol),
                cert_name:cert,   //证书
                src_type:src_type,
                src_value:src_value,
                src_host:src_host,
                src_back_type:src_back_type,
                src_back_value:src_back_value,
                ignore_cache_control:ignore_cache_control,
                ignore_query_string:ignore_query_string,
                // cache_rule:cache_array,
                cache_rule:JSON.stringify(cache_array),
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            error:function(){
                lay_tips(gettext('通讯异常'));
            },
            success: function(res){
            
                if(res.status){
                    layui_nav_each(domain_list,domain_list);
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
    form.render();
    table.render();

});