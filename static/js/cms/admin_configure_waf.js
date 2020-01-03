
var domain_id=parent_oblique[parent_oblique.length-2];
var safe_domain=parent_split[parent_split.length-1];   //域名
var create=parent_split[parent_split.length-2];   //接入cdn状态
/*console.log(parent_oblique)
console.log(domain_id)*/
var waf_conf;
var admin_sec_domain_conf_list='/sec/admin_sec_domain_conf/page/';   //创建或者绑定成功
var admin_waf_binding_ajax_list='/sec/ajax/admin_domain_waf_binding/';   //绑定waf接口
var waf_remove_ajax_list='admin_domain_waf_set_cdn';   //接入 移出ＣＤＮ
var set_waf_ajax_list='admin_domain_set_waf';   //启用 停用waf
var admin_delete_waf_ajax_list='/sec/ajax/admin_domain_del_waf/';   //创建waf;
var page_list='/sec/admin_sec_domain_list/page/';
var check_waf_ajax_list='admin_check_domain_waf_status';
var admin_set_domain_ajax_list='/sec/ajax/admin_set_domain_waf_conf';
var add_waf_cert_ajax_list='admin_upload_waf_cert';//添加证书
var admin_domain_waf_create='/sec/admin_domain_waf_create/page/';   //创建waf;
var channel_list='/sec/admin_sec_domain_list/page/';   //导航页面

// create
// 1  第一次创建接入cdn
// 2  再接入cdn
// 3  再次接入时，直接进入CDN检查确认页面
// 4  再次接入时，接入方式和回源地址不匹配，进入waf配置编辑页面
// 5 or 6  WAF再次接入CDN检查确认页面

var create_waf=document.getElementById('create_waf');  //创建waf
var move_basic_configure=document.getElementById('move_basic_configure');  //移除cdn
var basic_configure=document.getElementById('basic_configure');    //基础配置
if(create != 1 && whetherBind == 'False'){
    $('#access_in_cdn').text(gettext('再接入CDN'))
}else{
    $('#access_in_cdn').text(gettext('接入CDN'))
}
if(parent_oblique[2]=='admin_domain_waf_create'){    //创建waf
    if(waf_status_safe===1){
        $('#waf_status').text(gettext('创建中'));
    }
    $('#basic_configure').show();
    $('#create_first,.configuration_tap,#create_waf_first,.user_details').hide();
    $('#domain_create,#domain_second,#create_time_line,.user_add').show();
    admin_set_domain_ajax_list='/sec/ajax/admin_domain_waf_create/';   //创建waf接口
}else if(parent_oblique[2]=='admin_domain_waf_register'){           // 创建waf
    $('#opening_waf').show();
}else if(parent_oblique[2]=='admin_sec_domain_conf'){
    admin_set_domain_ajax_list='/sec/ajax/admin_set_domain_waf_conf/';  //编辑waf
    $('#domain_second').show();
}else if(parent_oblique[2]=='admin_domain_waf_conf_fail'){
    $('#domain_second').show();
}
var domain=$('#domain').text();
if(waf_status_safe=== ''){
    $('#domain_second').hide();
}else if(waf_status_safe==3 || waf_status_safe==2 || waf_status_safe==1 || waf_status_safe===0) {    //waf基础配置
    $('#create_time_line').show();
    if(waf_status_safe==3) {    //接入成功
        $('#opening_waf,#opening_waf_first').hide();
        $('#domain_second').show();
    }else if(waf_status_safe==2){  //未接入
        if(create == 3){
            $('.user_details,#preservation,#pre_again').hide();
            $('.user_add,#confirm_access').show();
            $('.waf_conf input,.waf_conf select,.waf_conf textarea').attr('disabled', true)
        }else if(create == 4){
            $('.user_details,#preservation').hide();
            $('.user_add,#pre_again').show();
            $('.cdn_conf input,.cdn_conf select').attr('disabled', true)

        }else if(create == 5 || create == 6){
            basic_configure.style.display='none';
            move_basic_configure.style.display='block';
        }else{
            $('#basic_configure,#domain_second,#domain_create').show();
            $('#opening_waf').hide();
        }

    }else if(waf_status_safe===0){
        $('#domain_second').show();
    }else if(waf_status_safe===1){

    }
}else{

}

//waf状态



layui.use(['table','form','laypage','element'], function() {
    var form = layui.form;
    var table = layui.table;
    var layer = layui.layer;
    var element=layui.element;
    var url_domain = admin_sec_domain_conf_list + domain_id + '/';
    form.on('submit(opening_waf)',function(){   //开通waf
        var loading = top.layer.load(1, {
            shade: [0.4,'#fff']
        });
        $.ajax({
            type: "POST",
            url: '/sec/ajax/'+check_waf_ajax_list+'/',
            data: {
                domain_id:domain_id,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            // async:false,
            error:function(){
                lay_tips(gettext('通讯异常'));
            },
            success: function(res){
                top.layer.close(loading)
                if(res.status){
                    $('#opening_waf').hide();
                    if(res.check_result == 'is_create'){       //创建
                        $('#create_waf_first,#create_time_line').show();
                        $('#waf_status').text(gettext('创建中'));
                    }else if(res.check_result == 'is_binding'){     //绑定
                        $('#domain_binding,#create_time_line,#opening_waf_first').show();
                        $('#waf_status').text(gettext('绑定中'));
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
    });

    form.on('radio(waf_mode)',function(data){    //选择WAF接入CDN方式
        if(data.value==2){
            $('#waf_conf_h5').text(gettext('边缘回WAF配置'));
            $('#waf_conf_label').text(gettext('边缘回WAF地址-CNAME'));
            $('#access_type_name').text(gettext('WAF回上层配置'))
            if(parent_oblique[2] =='admin_domain_waf_create'){
                $('#waf_address').text(waf_origin);
                $("input[name=domain_back_source][value='2']").prop("checked","true");
            }
        }else{
            $('#waf_conf_h5').text(gettext('上层回WAF配置'));
            $('#waf_conf_label').text(gettext('上层回WAF地址-CNAME'));
            $('#access_type_name').text(gettext('WAF回源站配置'))
            if(parent_oblique[2] =='admin_domain_waf_create'){
                $('#waf_address').text('');
                $("input[name=domain_back_source][value='2']").removeAttr("checked");
            }
        }

        form.render();
    })
    form.on('radio(domain_back_source)',function(data){    //选择WAF回源方式
        var waf_mode=$('input[name="waf_mode"]:checked').val();
        if(data.value==2 && waf_mode==2){
            $('#waf_address').text(waf_origin);
        }else{
            $('#waf_address').text('');
        }
        form.render();
    });

    form.on('submit(create_waf)',function(){
        //创建waf
         create=1;
         var url=admin_domain_waf_create+ domain_id +'/';
         layui_nav_each(url,page_list,create,safe_domain);
    });

    form.on('submit(create_pine)',function(){   //绑定waf
        var index_ado;
        var waf_mode=$('input[name="waf_mode"]:checked').val();
        var waf_point=$('#waf_point option:selected').val();
        if(waf_mode=='' || waf_mode==undefined){
            var lay_cont='需选择WAF接入CDN方式';
            lay_tips(lay_cont);
            return;
        }else if(waf_point==''){
            var lay_cont='WAF接入点不能为空';
            lay_tips(lay_cont);
            return;
        }
        $.ajax({
            type: "POST",
            url: admin_waf_binding_ajax_list,
            data: {
                domain_id:domain_id,
                access_type:waf_mode,
                short_name:waf_point,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            error:function(){
                lay_tips(gettext('通讯异常'));
            },
            success: function(res){
                if(res.status){
                    layer.close(index_ado);
                    var url_upload=admin_sec_domain_conf_list+domain_id+'/';
                    layui_nav_each(url_upload,page_list,safe_domain);
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
                            parent.window.location.reload();
                            basic_configure.style.display='block';
                            move_basic_configure.style.display='none';

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
    }
    form.on('submit(stop_waf)',function(){   //停用waf
        var switch_status=0;
        var lay_cont=gettext('确定停用青松WAF服务？');
        var determine_outage=gettext('确定停用');
        waf_status(switch_status,lay_cont,determine_outage)
    });

    form.on('submit(open_waf)',function(){   //启用waf
        var switch_status=1;
        var lay_cont=gettext('确定启用青松WAF服务？');
        var determine_outage=gettext('确定启用');
        waf_status(switch_status,lay_cont,determine_outage)
    });

    form.on('submit(delete_waf)',function(){   //删除waf
        // document.getElementById('iframe_admin').contentWindow.location.reload(true);
        parent.layer.open({
          title:gettext('提示'),
              type: 1,
              align:'center',
              shade:0,
              area:['500px','220px'],
              offset:'auto',
              btnAlign: 'c',
              btn:[gettext('确定删除'),gettext('取消')],
              content:'<div class="lay_content" style="padding: 20px 100px;text-align: center">'+gettext('确定删除青松WAF服务')+'</div>',  //这里content是一个普通的String
              yes:function(){
                $.ajax({
                    type: "POST",
                    url: admin_delete_waf_ajax_list,
                    data: {
                        domain_id:domain_id,
                        csrfmiddlewaretoken: $.cookie('csrftoken')
                    },
                    dataType : 'json',
                    error:function(){
                        lay_tips(gettext('通讯异常'));
                    },
                    async:false,
                    success: function(res){

                        if(res.status){
                            layui_nav_each(channel_list,channel_list);
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

    form.on('submit(cancel_submit)',function(){   //取消
        if(create == 4){
            layui_nav_each(url_domain, page_list,safe_domain);

        }else{
            $('.user_details').show();
            $('.user_add').hide();
        }


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
            '<label class="layui-form-label" style="">'+gettext("证书名")+'</label>' +
            '<div class="layui-input-block">' +
            '    <input id="cert_name" type="text" name="title" lay-verify="title" autocomplete="off" placeholder="" class="layui-input">' +
            '</div></div>'+
            '<div class="layui-form-item">' +
            '<label class="layui-form-label" style="">'+gettext("公钥")+'</label>' +
            '<div class="layui-input-block" >' +
            '    <textarea placeholder="" id="public_key" style="height:200px;width:90%;" class="layui-textarea"></textarea>' +
            '</div></div>'+
            '<div class="layui-form-item">' +
            '<label class="layui-form-label" style="">'+gettext("私钥")+'</label>' +
            '<div class="layui-input-block">' +
            '    <textarea placeholder="" id="private_key" style="height:200px;width:90%;" class="layui-textarea"></textarea>' +
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

    form.on('submit(move_out_cdn)',function(){    //移出cdn
        basic_configure.style.display='none';
        $('#move_basic_configure input[type="checkbox"]').prop('checked',false);
        move_basic_configure.style.display='block';
        form.render();
    });
    form.on('submit(access_in_cdn)',function(){    //接入cdn
        if(create == 1 ){    //第一次接入
            basic_configure.style.display='none';
            $('#move_basic_configure input[type="checkbox"]').prop('checked',false);
            move_basic_configure.style.display='block';
        }else{
            $('.waf_conf input,.waf_conf textarea,.waf_conf select').attr('disabled', true)
            $('.cdn_conf input,.cdn_conf select').prop('disabled', false);
            $('#preservation,#pre_again').hide();
            $('#confirm_access').show();

        }
        $('.user_details').hide();
        $('.user_add,#waf_host').show();
        form.render();

    });

    form.on('submit(back_access)',function() {    //确认接入前返回
        $('.waf_conf input,.waf_conf textarea,.waf_conf select').prop('disabled', false);
        $('.cdn_conf input,.cdn_conf select').attr('disabled', true)
        $('.user_details,#preservation,#pre_again').show();
        $('.user_add,#confirm_access').hide();
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
        $.ajax({
            type: "POST",
            url: '/sec/ajax/'+waf_remove_ajax_list+'/',
            data: {
                domain_id:domain_id,
                switch:switch_status,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:true,
            error:function(){
                lay_tips(gettext('通讯异常'));
            },
            success: function(res){
                if(res.status){
                    // window.location.reload();
                    // console.log(location.href)
                    var url_upload = admin_sec_domain_conf_list + domain_id + '/';
                    if(switch_status == 0){
                        layui_nav_each(url_upload, page_list,2,safe_domain);
                    }else{
                        layui_nav_each(url_upload, page_list,safe_domain);
                    }
                    // location.replace(location.href);
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

    form.on('submit(edit_cdn)',function(){   //编辑
       /* $('.user_details').hide();
        $('').show();*/
        $('.waf_conf input,.waf_conf textarea,.waf_conf select').prop('disabled', false)
        $('.cdn_conf input,.cdn_conf select').attr('disabled', true)
        $('.user_details,#confirm_access,.pre_again').hide();
        $('.user_add,#waf_host,#preservation').show();
        /*if(whetherBind == 'False'){
            $('.waf_conf input,.waf_conf textarea,.waf_conf select').prop('disabled', false)
            $('.cdn_conf input,.cdn_conf select').attr('disabled', true)
            $('#confirm_access,.pre_again').hide();
            $('#preservation').show();
        }*/
        form.render();

    });


    form.on('submit(establish)',function() {    //创建
        var create=1;
        create_preservation(create);
    });

    form.on('submit(preservation)',function(){    //保存
        create_preservation();
    });

    form.on('submit(confirm_access)',function() {    //确认接入
        create=5;
        create_preservation(5);
    });

    form.on('submit(pre_again)',function() {    //接入时waf配置和接入方式不匹配
        create=6;
        create_preservation(6);
    });




    var create_preservation = function (create) {     //保存 or  创建

        var url_upload = admin_sec_domain_conf_list + domain_id + '/';   //跳转地址
        // var layer_loading=layer.load(2);   //加载条
        var waf_mode = document.getElementsByName('waf_mode');   //接入方式
        var access_type = '';
        var access_name = '';
        for (var i = 0; i < waf_mode.length; i++) {
            if (waf_mode[i].checked) {
                access_type = waf_mode[i].value;
                access_name = waf_mode[i].title;
            }

        }

        var waf_short_name = $('#waf_short_name option:selected').val();   //接入点
        var access_point = waf_short_name.split('/')[0];

        var src_type='';
        if(create == 1){
            var domain_back_source = document.getElementsByName('domain_back_source');  //回源方式
            for (var i = 0; i < domain_back_source.length; i++) {
                if (domain_back_source[i].checked) {
                    src_type = domain_back_source[i].value;
                }
            }
        }else{
            var waf_host = $('#waf_host').text().replace(/^\s+|\s+$/g,"");
            for(var src_type_in in src_type_conf){
                var src_type_in=src_type_conf[src_type_in];
                if(src_type_in.name == waf_host){
                    src_type=src_type_in.id;
                }
            }
        }


        var src_address='';    ///WAF回源地址
        var ip_reg = /^((([1-9][0-9])|([0-9])|((1[0-9][0-9])|(2[0-4][0-9])|(25[0-5])))\.){3}(([1-9][0-9])|([0-9])|((1[0-9][0-9])|(2[0-4][0-9])|(25[0-5])))$/;
        var port_reg=/^[0-9]+$/;
        if(src_type==1){
            src_address=$('#waf_address').val().replace(/\n/g,",");
            var ip_nub=0;
            var ip_all=src_address.split(',');
            for(var i=0;i<ip_all.length;i++){
                if(!ip_reg.test(ip_all[i])){
                    ip_nub++;
                }
            }
        }else{
            src_address = $('#waf_address').val();
        }
        var src_port = $('#waf_port').val();  //回源端口

        if(access_type == ''){
            lay_tips(gettext('请选择WAF接入CDN方式'))
            return;
        }else if(src_type == ''){
            lay_tips(gettext('请选择WAF回源方式'))
            return;
        }else if(src_address == '') {
            lay_tips(gettext('请输入WAF回源地址'))
            return;
        }else if(src_port == ''){
            lay_tips(gettext('请输入回源端口'))
            return;
        }

        if(src_type==1 && ip_nub !=0){
            lay_tips(gettext('WAF回源地址格式不正确，请重新输入'))
            return;
        }
        if(!port_reg.test(src_port)){
            lay_tips(gettext('WAF回源端口格式不正确，请重新输入'))
            return;
        }
        var loading = top.layer.load(1, {
            shade: [0.4,'#fff']
        });
        var ssl_status = '';
        if (document.getElementsByName('open_https')[0].checked) {
            ssl_status = 1;
        } else {
            ssl_status = 0;
        }
        var cert_id=$('.service_cert').attr('id');
        if(ssl_status == 0){
            cert_id = '';
        }else if(ssl_status ==1 && cert_id =='None' || cert_id ==''){
            lay_tips(gettext('请上传证书'),loading);
            return;
        }

        var waf_default = $('#waf_default option:selected').val();
        var waf_custom = $('#waf_custom option:selected').val();
        var waf_cname_type = waf_short_name.split('/')[1];   //cname

        if(create == 5 && src_type==2 && access_type == 2 && src_address != waf_origin ){
            layer.close(loading);
            var lay_content='<div class="lay_content" style="padding: 20px 50px;text-align: center">waf的回源地址，与“'+gettext(access_name)+'”接入方式不匹配<a class="blue" id="go_waf_conf" style="display:block;" href="javascript:;">'+gettext('前往编辑waf配置')+'</a></div>'
            parent.layer.open({
              title:gettext('提示'),
                  type: 1,
                  align:'center',
                  shade:0,
                  area:['500px','250px'],
                  offset:'auto',
                  btnAlign: 'c',
                  btn:[gettext('确定')],
                  content:lay_content,  //这里content是一个普通的String
                  yes:function(){
                        parent.layer.closeAll();
                  },
                  cancel: function(){
                        parent.layer.closeAll();
                  }

            });
            $(parent.document).on('click','#go_waf_conf',function(){
                parent.layer.closeAll();
                $('.cdn_conf input,.cdn_conf select').attr('disabled', true);
                $('.waf_conf input,.waf_conf textarea,.waf_conf select').prop('disabled', false)
                $('#pre_again').show();
                $('#confirm_access').hide();
                form.render();
            });
            return;
        }
        $.ajax({
            type: "POST",
            url: admin_set_domain_ajax_list,
            data: {
                domain_id: domain_id,
                access_type: access_type,  //waf接入方式
                access_point_cname:waf_cname_type,     //cname
                short_name: access_point,    //接入点
                src_type: src_type,
                src_address: src_address,
                src_port: src_port,
                src_host: '',
                cert_id: cert_id,  //证书id
                ssl_status: ssl_status,
                default_waf_mode: waf_default,
                self_waf_mode: waf_custom,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            // async: false,
            error: function () {
                lay_tips(gettext('通讯异常'));
            },
            success: function (res) {
                parent.layer.close(loading);
                if(res.status === -1 || res.status === 1){
                    if(res.status == 1){
                        var num='loading';
                    }else if(res.status == -1){
                        var num=404;
                    }
                    url_upload='/sec/admin_domain_waf_conf_fail/page/';
                    layui_nav_each(url_upload, page_list,num,safe_domain);
                }else if (res.status === 2 || res.status === true) {
                    if(create == 3){
                        layui_nav_each(url_upload, page_list,create,safe_domain);
                    }else if(create == 5 || create == 6){
                        layui_nav_each(url_upload, page_list,create,safe_domain);
                    }else{
                        if (parent_oblique[2] == 'admin_sec_domain_conf') {
                            // window.location.reload();
                            layui_nav_each(url_upload, page_list,create,safe_domain);
                        }else if (parent_oblique[2] == 'admin_domain_waf_create') {
                            layui_nav_each(url_upload, page_list,create,safe_domain);
                        }
                    }
                }else{

                    if (res.msg != '' && res.msg != undefined) {
                        lay_tips(res.msg);
                    } else {
                        lay_tips(gettext('通讯异常'));
                    }
                }

            }
        })
    }
    form.on('submit(cancel)',function(){   //取消编辑

        $('.user_details').hide();
        $('.user_add').show();
    });
    form.on('submit(back_cdn)',function(){   //返回
        if(create == 1){
            $('.user_details,#basic_configure').show();
            $('.user_add,#waf_host,#move_basic_configure').hide();
        }else if(create == 5){
            layui_nav_each(url_domain, page_list,'3',safe_domain);
        }else if(create == 6){
            layui_nav_each(url_domain, page_list,'4',safe_domain);
        }else{
            $('#move_basic_configure').hide();
            $('#basic_configure').show();
        }
    });
    form.render();
});

