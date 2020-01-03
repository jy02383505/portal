var domain_list='';  //当前导航地址
var admin_modify_domain_conf_ajax='';  //修改配置接口
var cert_list_ajax=''; // 证书列表

if(is_staff=='True'){     //管理员端域名列表
    domain_list='/cdn/admin_get_domain_list/page/';
    cert_list_ajax='/cdn/ajax/admin_cdn_get_cert/';
    admin_modify_domain_conf_ajax='/cdn/ajax/admin_cdn_edit_domain/';
    var default_cache=default_cache;
}else if(is_staff == 'False'){
    domain_list='/cdn/client_get_domain_list/page/';
    cert_list_ajax='/cdn/ajax/client_cdn_get_cert/';
    admin_modify_domain_conf_ajax='/cdn/ajax/client_cdn_edit_domain/';
}

layui.use(['table','form','layer','element'], function() {
    var form = layui.form;
    var table = layui.table;
    var layer = layui.layer;
    var element = layui.element;

    var caching_rules_list='';   //默认缓存规则
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
        if(default_cache_in.ttl<60){
            select_time=gettext('秒');
            caching_times=default_cache_in.ttl;
        }else if(default_cache_in.ttl>=60 && default_cache_in.ttl<3600){
            select_time=gettext('分');
            caching_times=default_cache_in.ttl/60;
        }else if(default_cache_in.ttl>=3600 && default_cache_in.ttl<86400){
            select_time=gettext('小时');
            caching_times=default_cache_in.ttl/3600;
        }else if(default_cache_in.ttl>=86400){
            select_time=gettext('天');
            caching_times=default_cache_in.ttl/86400;
        }

            if(default_cache_in.rule == '/.*'){
                caching_rules_list +='<tr id="cdn_type_last"><td class="cache_td" id="'+default_cache_in.type+'"><span>'+ gettext(cache_name)+'</span></td><td class="cache_td" id="'+default_cache_in.rule+'"><span>'+gettext('全部文件')+'</span></td>' ;
            }else{
                caching_rules_list +='<tr id="cdn_type_tr"><td class="cache_td" id="'+default_cache_in.type+'"><span>'+ gettext(cache_name)+'</span></td><td class="cache_td" id="'+default_cache_in.rule+'"><span>'+default_cache_in.rule+'</span></td>' ;
            }

        caching_rules_list += '<td class="cache_td" id="'+default_cache_in.ttl+'"><span>'+parseInt(caching_times)+'</span><span>'+select_time+'</span></td><td>' ;
        if(default_cache_in.rule != '/.*'){
            caching_rules_list +='<div class="cache_sort"><span class="move_down"></span><span class="move_up"></span></div>' ;
        }
        caching_rules_list +='<div class="cache_btn user_add"><a class="layui-btn layui-btn-xs layui_edit" lay-event="edit">'+gettext('编辑')+'</a>' +
         '<a class="layui-btn layui-btn-xs layui_del" lay-event="del">'+gettext('删除')+'</a></div></td></tr>';
    }

    $('#cache_tbody').html(caching_rules_list);
    $('#cdn_type_last .layui_del').addClass('btn_gray').removeClass('layui_del');
    /*var $('#cache_tbody tr').length
    for(){

    }*/
    table.render();

    $(document).on('click','.conf_edit',function(){
        var conf_this=$(this).parents('.lay_configure');
        $(this).hide();
        conf_this.find('.user_details').hide();
        conf_this.find('.user_add').show();
        conf_this.find('input,button').removeAttr('disabled');
        form.render();
        if($(this).attr('id')=='2'){
            conf_this.find('.layui-btn').removeClass('layui-btn-gray');
        }

    });


    form.on('submit(lay_submit_basic)',function(){
        var conf_this=$(this).parents('.lay_configure');
        var data_num=1;
        window.data_search(conf_this,data_num);
    });
    form.on('submit(lay_submit_cache)',function(){
        var conf_this=$(this).parents('.lay_configure');
        var data_num=2;
        window.data_search(conf_this,data_num);
    });
    form.on('submit(lay_submit_conf_cert)',function(){
        var conf_this=$(this).parents('.lay_configure');
        var data_num=3;
        window.data_search(conf_this,data_num);
    });

    $(document).on('click','.lay_cancel',function(){
        var conf_this=$(this).parents('.lay_configure');
        if(conf_this.find('.conf_edit').attr('id')=='2'){
            conf_this.find('button').addClass('layui-btn-gray');
        }
        conf_this.find('.user_details,.conf_edit').show();
        conf_this.find('.user_add').hide();
        // conf_this.find('.cache_conf button').addClass('layui-btn-gray');
        conf_this.find('input,.layui-form-item button').attr('disabled','disabled');
        form.render();
    });

    window.data_search = function(conf_this,data_num){
        var loading = top.layer.load(1, {
                shade: false
            });
        var user_id=$('#user_id').text();
        var domain=$('#domain').text();
      /*  var src_type='';
        var src_value='';                      //源站地址
        var src_back_type='';
        var src_back_value='';
        var src_host='';
        var ignore_cache_control='';
        var ignore_query_string='';*/

        var cert=$('#cert_name').text();
        var src_type=$('input[name="src_type"]:checked').val();  //回源方式
        if(src_type=='ip'){
            var src_value=$('#src_type_text').val();
        }else{
            var src_value=$('#src_type_input').val();

        }

        var src_back_type=$('input[name="src_back_type"]:checked').val();  //备份源站类型
        if(src_back_type=='ip'){
            var src_back_value=$('#src_back_text').val();
        }else if(src_back_type=='dmn'){
            var src_back_value=$('#src_back_input').val();
        }

        if(src_back_value == ''){
            src_back_type=''
        }
        var source_host_type=$('input[name="source_host_type"]:checked').val();
        var src_host='';
        if(source_host_type == 1){
            src_host=$('input[name="domain_src_host"]').val();  //回源host
        }

        if($('input[name="ignore_cache_control"]').is(':checked',true)){    //header配置
            var ignore_cache_control=1;
        }else{
            var ignore_cache_control=0;
        }
        if($('input[name="ignore_query_string"]').is(':checked',true)){    //参数配置
            var ignore_query_string=1;
        }else{
            var ignore_query_string=0;
        }
        function group(array, subGroupLength) {
              var index = 0;
              var newArray = [];
              while(index < array.length) {
                  newArray.push(array.slice(index, index += subGroupLength));
              }
              return newArray;
        }
        var cache_rule=[];                            //缓存规则
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

        if(data_num == 1){
            if(src_value == ''){
                lay_tips(gettext('源站地址不能为空'),loading);
                return;
            }
        }else if(data_num == 2){
            if(cache_array == ''){
                lay_tips(gettext('缓存规则不能为空'),loading);
                return;
            }
        }else if(data_num == 3){
            cert=$('select[name="cert"] option:selected').val();
            if(cert == ''){
                lay_tips(gettext('证书不能为空'),loading);
                return;
            }
        }else{
            cert=$('#cert_name').text();
        }

        $.ajax({
            type: "POST",
            url: admin_modify_domain_conf_ajax,
            data: {
                user_id:user_id,
                domain:domain,
                src_type:src_type,
                src_value:src_value,
                src_host:src_host,
                src_back_type:src_back_type,
                src_back_value:src_back_value,
                ignore_cache_control:ignore_cache_control,
                ignore_query_string:ignore_query_string,
                cache_rule:JSON.stringify(cache_array),
                cert_name:cert,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            // async:false,
            success: function(res){

                top.layer.close(loading)
                if(res.status==true){
                    // layui_nav_each(domain_list,domain_list);
                    if(data_num ==1){
                        window.location.reload();
                    }else{
                        if(data_num ==2){
                            $('button').addClass('layui-btn-gray');
                            // console.log(ignore_cache_control)
                            if(ignore_cache_control ==0 ){
                                $('input[name="ignore_cache_control"]').removeAttr('checked')
                            }else{
                                $('input[name="ignore_cache_control"]').is(':checked',true)
                            }
                            if(ignore_query_string ==0 ){
                                $('input[name="ignore_query_string"]').removeAttr('checked')
                            }else{
                                $('input[name="ignore_cache_control"]').is(':checked',true)
                            }
                            $('.cache_btn').addClass('user_add');
                        }
                        $('.domain_conf,.conf_edit').show();
                        // $('.conf_edit').hide();
                        $('#domain_status').text(gettext('配置中'))
                        conf_this.find('.user_details').show();
                        conf_this.find('.user_add').hide();
                        $('input,button').attr('disabled','disabled');

                    }
                    // window.location.reload();
                    form.render();
                }else{
                    res_msg(res);
                }

            }
        });
    };
    // data_search();
    form.render();
});
