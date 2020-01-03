var page_list='';    //导航
var add_cert_list_ajax='';        //添加证书
var cols=[];    //table表头
var is_update='';
var cert_detail_array=cert_detail;
if(parent_oblique[2]=='admin_cert_create' || parent_oblique[2]=='admin_cert_edit'){     //新建用户
    add_cert_list_ajax='/cert/ajax/admin_cert_create_or_edit/';
    page_list='/cert/admin_cert_ssl_manage/page/';
}else if(parent_oblique[2]=='client_cert_edit' || parent_oblique[2]=='client_cert_create'){
    add_cert_list_ajax='/cert/ajax/client_cert_create_or_edit/';
    page_list='/cert/client_cert_ssl_manage/page/';

}
if(parent_oblique[2]=='admin_cert_create' || parent_oblique[2]=='client_cert_create'){     //上传证书
    $('.user_add').show();
    $('.user_details').hide();
    is_update=0;
}else if(parent_oblique[2]=='admin_cert_edit' || parent_oblique[2]=='client_cert_edit'){   //更新证书
    $('.user_add').hide();
    $('.user_details').show();
    is_update=1;
}
layui.use(['form','table','element','layer'], function(){
    var form = layui.form;
    var table = layui.table;
    var layer=layui.layer;

    form.on('submit(lay_submit)',function(){   //用户信息
        var username='';
        if(is_staff == 'True'){
            if(parent_oblique[2]=='admin_cert_create'){     //新建用户
                username=$('select[name="username"] option:selected').val();
            }else if(parent_oblique[2]=='admin_cert_edit'){
                username=cert_detail_array.username;
            }
        }

        if(parent_oblique[2]=='admin_cert_create' && username=='' ){     //新建用户
            lay_cont=gettext('用户名不能为空');
            lay_tips(lay_cont);
            return;
        }
        var cert_name='';
        if(parent_oblique[2]=='admin_cert_create' || parent_oblique[2]=='client_cert_create'){     //新建用户
            cert_name=$('input[name="cert_name"]').val();
        }else if(parent_oblique[2]=='admin_cert_edit' || parent_oblique[2]=='client_cert_edit'){
            cert_name=cert_detail_array.cert_name;
        }

        if(cert_name==''){
            var lay_cont=gettext('证书名称不能为空');
            lay_tips(lay_cont);
            return;
        }
        var certificate=$('textarea[name="certificate"]').val();
        if(certificate==''){
            var lay_cont=gettext('证书不能为空');
            lay_tips(lay_cont);
            return;
        }
        var private_key=$('textarea[name="private_key"]').val();
        if(private_key==''){
            var lay_cont=gettext('私钥不能为空');
            lay_tips(lay_cont);
            return;
        }

        var cert_value = encrypt(certificate);    //密码加密
        var key_value = encrypt(private_key);    //密码加密

        var remark=$('input[name="remarks"]').val();

        var email_reg=/^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/;   //邮箱

        var lay_email=$('input[name="lay_email"]').val();
        if(lay_email == ''){
            var lay_cont=gettext('邮箱不能为空');
            lay_tips(lay_cont);
            return;
        }
        if(!email_reg.test(lay_email)){
            var lay_cont=gettext('邮箱格式不正确');
            lay_tips(lay_cont);
            return;
        }
        var times=$('select[name="times"] option:selected').val();
        $.ajax({
            type: "POST",
            url: add_cert_list_ajax,
            data: {
                cert_name:cert_name,
                username:username,
                cert_value:cert_value,
                key_value:key_value,
                cert_pl:certificate.length,
                key_pl:private_key.length,
                email:lay_email,
                remark:remark,
                period:times,
                is_update:is_update,
                // cert_from:0,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            dataType : 'json',
            async:false,
            success: function(res){
                if(res.status==true){
                    layui_nav_each(page_list,page_list);
                }else{
                    res_msg(res);
                }

            }
        });

    });

    form.render();
});
