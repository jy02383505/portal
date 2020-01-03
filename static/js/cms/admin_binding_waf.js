var parent_href=window.parent.location.href;  //浏览器url
var parent_url=parent_href.split('=');
var parent_split=parent_url[1].split('/');
var parent_page=parent_split[parent_split.length-3];

var domain_id='';
var all_rules_ajax=''//开启关闭规则接口
if(parent_url.length>3){
    parent_page=parent_split[parent_split.length-4];
    domain_id=parent_split[parent_split.length-2];
    // domain_id=parent_url[parent_url.length-2]
}else{
    parent_page=parent_split[parent_split.length-4];
}

var admin_set_domain_ajax_list='';   //创建 or 保存 waf
var time_line=document.getElementById('time_line');   //进度条
var opening_waf=document.getElementById('opening_waf');   //开通WAF
var create_waf=document.getElementById('create_waf');  //创建waf
var create_first=document.getElementById('create_first');          //绑定WAF
var create_second=document.getElementById('create_second');        //绑定
var basic_configure=document.getElementById('basic_configure');    //基础配置
var move_basic_configure=document.getElementById('move_basic_configure');  //移除cdn

var create_waf_ajax_list='admin_domain_waf_binding';   //绑定waf接口
var admin_sync_domain_ajax_list='admin_sync_domain_waf_conf'; //获取waf基础信息
var waf_remove_ajax_list='admin_domain_waf_set_cdn';   //接入 移出ＣＤＮ
var set_waf_ajax_list='admin_domain_set_waf';   //启用 停用waf
var url='admin_sec_domain_conf';
var page_list='/sec/admin_sec_domain_list/page/';
var check_waf_ajax_list='admin_check_domain_waf_status';
var admin_set_domain_ajax_list='/sec/ajax/admin_set_domain_waf_conf';
var add_waf_cert_ajax_list='admin_upload_waf_cert';//添加证书
var admin_domain_waf_create='/sec/admin_domain_waf_create/page/';   //创建waf;

if(parent_page=='admin_sec_domain_conf'){
    admin_set_domain_ajax_list='/sec/ajax/admin_set_domain_waf_conf/';  //编辑waf
    opening_waf.style.display='block';
}
else if(parent_page=='admin_domain_waf_create'){
    $('.user_details').hide();
    $('.user_add').show();
    create_second.style.display = 'block';
    admin_set_domain_ajax_list='/sec/ajax/admin_set_domain_waf_conf/';  // 创建waf
}
else if(parent_page=='admin_domain_waf_register'){
    opening_waf.style.display='block';
}

var domain=$('#domain').text();
console.log(waf_status_safe);
if(waf_status_safe==3) {
    opening_waf.style.display='none';
}else if(waf_status_safe==2){
    time_line.style.display='block';
    create_first.style.display='none';
    opening_waf.style.display='none';

}else if(waf_status_safe==0){
    create_second.style.display = 'block';
    time_line.style.display='block';
}else

opening_waf.onclick=function(){    //开通waf
    var index_ado;
      $.ajax({
            type: "POST",
            url: '/sec/ajax/'+check_waf_ajax_list+'/',
        data: {
            domain_id:domain_id,
            csrfmiddlewaretoken: $.cookie('csrftoken')
        },
        async:false,
        error:function(){
            lay_tips(gettext('通讯异常'));
        },
        success: function(res){
            console.log(res);
            console.log(res.check_result);
            if(res.status){
                layer.close(index_ado);
                if(res.check_result == 'is_create'){       //创建

                    create_first.style.display='block';
                    opening_waf.style.display='none';
                    time_line.style.display='block';
                }else if(res.check_result == 'is_binding'){     //绑定
                    create_first.style.display='block';
                    opening_waf.style.display='none';
                    time_line.style.display='block';
                }
                if(res.waf_switch==0){
                    $('#domain_status').text(gettext('启用'));
                }else{
                    $('#domain_status').text(gettext('禁用'));
                }
            }else{
                if(res.msg !='' && res.msg != undefined){
                    lay_tips(res.msg);
                }else{
                    lay_tips(gettext('通讯异常'));
                }

            }

        }
      })
};


layui.use(['table','form','laypage','element'], function() {
    var form = layui.form;
    var table = layui.table;
    var layer = layui.layer;
    var element=layui.element;
    form.on('submit(create_waf)',function() {   //创建waf
         var url=admin_domain_waf_create+ domain_id +'/';
         layui_nav_each(url,page_list);
    })
    form.on('submit(create_pine)',function(){   //绑定waf
        var index_ado;
        var waf_mode=$('input[name="waf_mode"]:checked').val();
        var waf_point=$('#waf_point option:selected').val();
        if(waf_mode=='' || waf_mode==undefined){
            var lay_cont=gettext('需选择WAF接入CDN方式');
            lay_tips(lay_cont);
            return;
        }else if(waf_point==''){
            var lay_cont=gettext('WAF接入点不能为空');
            lay_tips(lay_cont);
            return;
        }
        $.ajax({
            type: "POST",
            url: '/sec/ajax/'+create_waf_ajax_list+'/',
            data: {
                domain_id:domain_id,
                access_type:waf_mode,
                access_short_name:waf_point,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            error:function(){
                lay_tips(gettext('通讯异常'));
            },
            success: function(res){
                if(res.status){
                    layer.close(index_ado);
                    var domain=$('#domain').text();
                    var url_upload='/sec/'+url+'/page/'+domain_id+'/';
                    layui_nav_each(url_upload,page_list,domain);
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
    if(waf_status_safe==3 || waf_status_safe==2 || waf_status_safe==0){
        var index_ado;                   //基础信息
        var waf_conf;
        $.ajax({
            type: "POST",
            url: '/sec/ajax/'+admin_sync_domain_ajax_list+'/',
            data: {
                domain_id:domain_id,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            error:function(){
                lay_tips(gettext('通讯异常'));
            },
            success: function(res){
                if(res.status){
                    layer.close(index_ado);
                    waf_conf=res.waf_conf;
                    if(waf_conf.ssl_status==0){
                        $('#waf_agreement').text(gettext('不启用https'));
                        $('.certificate').hide();
                        document.getElementsByName('open_https')[0].checked =false;
                    }else {
                        $('#waf_agreement').text(gettext('启用https'));
                        $('.certificate').show();
                        document.getElementsByName('open_https')[0].checked =true;
                    }
                    form.render('checkbox');
                    var waf_point_name='';     //接入点
                    var waf_point=document.getElementById('waf_short_name');
                    for(var i=0;i<access_point_conf.length;i++){
                        if(access_point_conf[i].name == waf_conf.access_point){
                            waf_point_name=access_point_conf[i].name;
                            waf_point.options[i].selected = 'selected';
                        }
                    }
                    $('#waf_point_address').text(gettext(waf_point_name));

                    var waf_default_cname='';    //默认规则防御模式
                    var waf_default=document.getElementById('waf_default');
                    for(var i=0;i<waf_default_mode_conf.length;i++){
                        if(waf_default_mode_conf[i].id==waf_conf.default_waf_mode){
                            waf_default_cname=waf_default_mode_conf[i].cname;
                            waf_default.options[i].selected = 'selected';
                        }
                    }
                    $('#waf_default_cname').text(gettext(waf_default_cname));

                    var waf_self_cname='';     //自定义规则防御模式
                    var waf_self=document.getElementById('waf_custom');
                    for(var i=0;i<waf_self_mode_conf.length;i++){
                        if(waf_self_mode_conf[i].id == waf_conf.self_waf_mode){
                            waf_self_cname=waf_self_mode_conf[i].cname;
                            waf_self.options[i].selected = 'selected';
                        }
                    }
                    $('#waf_self_cname').text(gettext(waf_self_cname));

                    var waf_host_cname='';     //回源方式
                    var domain_back_source=document.getElementsByName('domain_back_source');
                    for(var i=0;i<src_type_conf.length;i++){
                        if(waf_conf.source_is_ip==true && src_type_conf[i].id==1){
                            waf_host_cname=src_type_conf[i].name;
                            domain_back_source[i].checked =true;
                        }else if(waf_conf.source_is_ip==false && src_type_conf[i].id==2){
                            waf_host_cname=src_type_conf[i].name;
                            domain_back_source[i].checked =true;
                        }
                    }
                    $('#waf_host').text(gettext(waf_host_cname));


                    var access_type_conf_list='';
                    for(var access_type in  access_type_conf){
                        var access_type=access_type_conf[access_type];
                        if(waf_conf.access_type==access_type.id){
                            $('.waf_cdn').text(access_type.name);
                            access_type_conf_list +='<input type="radio" name="waf_mode" checked lay-filter="waf_mode" value="'+access_type.id+'" title="'+access_type.name+'">'
                        }else if(access_type.id==1){
                            access_type_conf_list +='<input type="radio" name="waf_mode" disabled lay-filter="waf_mode" value="'+access_type.id+'" title="'+access_type.name+'">'
                        }else{
                            access_type_conf_list +='<input type="radio" name="waf_mode" lay-filter="waf_mode" value="'+access_type.id+'" title="'+access_type.name+'">';
                        }
                    }
                    $('#access_type_conf').html(access_type_conf_list);  //接入方式
                    $('.waf_point_address').text(waf_conf.access_point);

                    $('.waf_address').text(waf_conf.source_addr);
                    $('.waf_port').text(waf_conf.port);$('.waf_port').val(waf_conf.port);
                    $('.waf_service').text(waf_conf.domain);$('.waf_service').val(waf_conf.domain);
                    $('#waf_certificate').text(waf_conf.cert_name);
                    $('.service_cert').val(waf_conf.cert_name);//服务证书
                    $('.service_cert').attr('id',waf_conf.cert_id);//服务证书
                    $('.waf_cname').text(waf_conf.access_point_cname+'('+ waf_conf.access_point +')');
                    $('#waf_cname_type').val(waf_conf.access_point_cname+'('+ waf_conf.access_point +')');
                    $('#service').text(waf_conf.provider_name);
                    if(parent_page=='admin_sec_domain_conf'){
                        create_second.style.display='block';
                    }
                    if(waf_status_safe==3) {
                        create_second.style.display = 'block';
                        time_line.style.display='block';
                    }
                }else{
                    if(res.msg !='' && res.msg != undefined){
                        lay_tips(res.msg);
                    }else{
                        lay_tips(gettext('通讯异常'));
                    }

                }

            }
        })
    }

    form.on('submit(move_out_cdn)',function(){    //移出cdn
        basic_configure.style.display='none';
        move_basic_configure.style.display='block';

    });

    form.on('submit(access_in_cdn)',function(){    //接入cdn
        basic_configure.style.display='none';
        move_basic_configure.style.display='block';

    });


    function sure_move_cdn(switch_status,tip_txt){   //接入移除cdn
        var sure_cdn = document.getElementsByName('sure_cdn');  //服务商
        var move_cdn_length=0;
        for(var i=0;i<sure_cdn.length;i++){
            if(sure_cdn[i].checked){
                move_cdn_length++;
            }
        }
        if(sure_cdn.length != move_cdn_length || move_cdn_length ==0){
            lay_tips(tip_txt);
            return
        }
        var confirm_cdn_preload=0;
        var confirm_cdn_http_layered=0;
        var confirm_cdn_https_layered=0;
        if(waf_conf.confirm_cdn_preload==true){
            confirm_cdn_preload=1;
        }
        if(waf_conf.confirm_cdn_http_layered==true){
            confirm_cdn_http_layered=1;
        }
        if(waf_conf.confirm_cdn_https_layered==true){
            confirm_cdn_https_layered=1;
        }
        $.ajax({
            type: "POST",
            url: '/sec/ajax/'+waf_remove_ajax_list+'/',
            data: {
                domain_id:domain_id,
                switch:switch_status,
                confirm_cdn_preload:confirm_cdn_preload,
                confirm_cdn_http_layered: confirm_cdn_http_layered,
                confirm_cdn_https_layered: confirm_cdn_https_layered,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            error:function(){
                lay_tips(gettext('通讯异常'));
            },
            success: function(res){
                if(res.status){
                    layer.close(index_ado);
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

    }

    form.on('submit(sure_move_cdn)',function(){   //确认移除cdn
        var switch_status=0;
        var tip_txt=gettext('在移出 WAF 前，请先确认 CDN 服务是否正常！');
        sure_move_cdn(switch_status,tip_txt);

    });
    form.on('submit(sure_access_cdn)',function(){   //确认接入cdn
        var switch_status=1;
        var tip_txt=gettext('在接入 WAF 前，请先确认 CDN 服务是否正常！');
        sure_move_cdn(switch_status,tip_txt);

    });

    function  waf_status(switch_status,lay_cont,determine_outage){  //开启停用waf
        parent.layer.open({
          title:gettext('提示'),
          type: 1,
          align:'center',
          shade:0,
          area:['500px','220px'],
          offset:'auto',
          btnAlign: 'c',
          btn:[determine_outage,gettext('取消')],
          content:'<div class="lay_content" style="padding: 20px 100px;text-align: center">'+lay_cont+'</div>',  //这里content是一个普通的String
          yes:function(){
              $.ajax({
                type: "POST",
                url: '/sec/ajax/'+set_waf_ajax_list+'/',
                data: {
                    domain_id:domain_id,
                    switch:switch_status,
                    csrfmiddlewaretoken: $.cookie('csrftoken')
                },
                async:false,
                error:function(){
                    lay_tips(gettext('通讯异常'));
                },
                success: function(res){
                    if(res.status){
                        parent.layer.close(index_ado);
                        window.location.reload();
                        basic_configure.style.display='block';
                        move_basic_configure.style.display='none';

                    }else{
                        if(res.msg !='' && res.msg != undefined){
                            lay_tips(res.msg);
                        }else{
                            llay_tips(gettext('通讯异常'));
                        }

                    }

                }
            })

          }
        });


    }
    form.on('submit(stop_waf)',function(){   //停用waf
        var switch_status=0;
        var lay_cont=gettext('确定停用青松WAF服务？');
        waf_status(switch_status,lay_cont,gettext('确定停用'));


    });

    form.on('submit(open_waf)',function(){   //启用waf
        var switch_status=1;
        var lay_cont=gettext('确定启用青松WAF服务？');
        waf_status(switch_status,lay_cont,gettext('确定启用'));
    });

    form.on('submit(edit_cdn)',function(){   //编辑
        $('.user_details').hide();
        $('.user_add').show();
    });
    form.on('submit(cancel_submit)',function(){   //取消
        $('.user_details').show();
        $('.user_add').hide();

    });

    form.on('checkbox(open_https)',function(){ //开启 https
        if(this.checked){
            $('.certificate').show();
        }else{
            $('.certificate').hide();
        }
    });

    form.on('select(waf_short_name)',function(data){    //waf接入点改变边缘回WAF地址-CNAME
        $('#waf_cname_type').val(data.value+'('+this.innerText+')');
        form.render('select');
    });

    form.on('submit(up_new_cert)',function(){   //上传新证书
        var content='<div class="layui-form" id="new_cert" style="padding:0 0px;">' +
            '<div class="layui-form-item">' +
            '<label class="layui-form-label" style="">'+gettext('证书名')+'</label>' +
            '<div class="layui-input-block">' +
            '    <input id="cert_name" type="text" name="title" lay-verify="title" autocomplete="off" placeholder="" class="layui-input">' +
            '</div></div>'+
            '<div class="layui-form-item">' +
            '<label class="layui-form-label" style="">'+gettext('公钥')+'</label>' +
            '<div class="layui-input-block" >' +
            '    <textarea placeholder="" id="public_key" style="height:200px;" class="layui-textarea"></textarea>' +
            '</div></div>'+
            '<div class="layui-form-item">' +
            '<label class="layui-form-label" style="">'+gettext('私钥')+'</label>' +
            '<div class="layui-input-block">' +
            '    <textarea placeholder="" id="private_key" style="height:200px;" class="layui-textarea"></textarea>' +
            // '    <input id="private_key" type="text" name="title" lay-verify="title" autocomplete="off" placeholder="" class="layui-input">' +
            '</div></div></div>';
        top.layer.open({
            type: 1
            ,title: gettext('上传新证书')
            ,area: ['600px', '660px']
            ,btnAlign: 'l'
            ,shade:0
            ,btnAlign: 'c'
            ,id: 'up_new_cert'
            ,content: content
            ,btn: [gettext('上传'),gettext('取消')]
            ,btn: [gettext('上传'),gettext('取消')]
            ,yes: function(index_ado){

                var cert_name=$('#cert_name',parent.document).val();
                var public_val=$('#public_key',parent.document).val();
                var private_val=$('#private_key',parent.document).val();
                var public_key = encrypt(public_val);    //密码加密
                var private_key = encrypt(private_val);    //密码加密
                $.ajax({                                      //添加证书
                    type: "POST",
                    url: '/sec/ajax/'+add_waf_cert_ajax_list+'/',
                    data: {
                        domain_id:domain_id,
                        name:cert_name,   //name
                        cert_value:public_key,
                        key_value:private_key,
                        cert_pl:public_val.length,
                        key_pl:private_val.length,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    },
                    dataType : 'json',
                    error:function(){
                        lay_tips(gettext('通讯异常'));
                    },
                    async:false,
                    success: function(res){
                        if(res.status){
                            parent.layer.close(index_ado);
                            $('.service_cert').val(cert_name);
                            $('.service_cert').attr('id',res.cert_id);
                            // window.location.reload();
                        }else{
                            if(res.msg !='' && res.msg != undefined){
                                lay_tips(res.msg);
                            }else{
                                lay_tips(gettext('通讯异常'));
                            }

                        }
                    }
                })
            }
        });

    });

    form.on('submit(preservation)',function(){   //保存 or  创建

        var waf_mode=document.getElementsByName('waf_mode');   //接入方式
        var access_type='';
        for(var i=0;i<waf_mode.length;i++){
            if(waf_mode[i].checked){
                access_type=waf_mode[i].value;
            }

        }
        var short_name=$('#waf_short_name option:selected').attr('name');
        var domain_back_source=document.getElementsByName('domain_back_source');  //回源方式
        var src_type='';
        for(var i=0;i<domain_back_source.length;i++){
            if(domain_back_source[i].checked){
                src_type=domain_back_source[i].value;
            }
        }
        var src_address=$('#waf_address').val();
        var src_port=$('#waf_port').val();
        var ssl_status='';
        if(document.getElementsByName('open_https')[0].checked){
            ssl_status=1;
        }else{
            ssl_status=0;
        }
        var cert_id=$('.service_cert').attr('id');
        var waf_default=$('#waf_default option:selected').val();
        var waf_custom=$('#waf_custom option:selected').val();
        $.ajax({
            type: "POST",
            url: admin_set_domain_ajax_list,
            data: {
                domain_id:domain_id,
                short_name:short_name,
                access_type:access_type,
                src_type:src_type,
                src_address:src_address,
                src_port:src_port,
                src_host:'',
                cert_id:cert_id,
                ssl_status:ssl_status,
                default_waf_mode:waf_default,
                self_waf_mode:waf_custom,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            error:function(){
                lay_tips(gettext('通讯异常'));
            },
            success: function(res){
                if(res.status){
                    if(parent_page=='admin_sec_domain_conf'){
                        layer.close(index_ado);
                        window.location.reload();
                    } else if(parent_page=='admin_domain_waf_create'){
                        var url_upload='/sec/'+url+'/page/'+domain_id+'/';
                        layui_nav_each(url_upload,page_list,domain);
                    }
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
    form.on('submit(cancel)',function(){   //编辑
        $('.user_details').hide();
        $('.user_add').show();
    });
    form.render();
});

