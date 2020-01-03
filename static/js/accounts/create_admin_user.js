layui.use(['form','table','element','layer'], function(){
    var form = layui.form;
    form.on('submit(confirm)',function(){
        var password_reg = /([a-zA-Z0-9!@#$%^&*()_?<>{}]){5,12}/;
        var username=$('#username').val();
        var password=$('#password').val();
        var password_again=$('#password_again').val();
        var role=$('#role option:selected').val();
        if(username==''){
            var lay_cont=gettext('管理员不能为空');
            lay_tips(lay_cont);
            return;
        }
        if(password==''){
            var lay_cont=gettext('登录密码不能为空');
            lay_tips(lay_cont);
            return;
        }
        if(!password_reg.test(password)){
            var lay_cont=gettext('密码必须6到12位');
            lay_tips(lay_cont);
            return;
        }
        if(password_again==''){
            var lay_cont=gettext('确认密码不能为空');
            lay_tips(lay_cont);
            return;
        }
        if(password != password_again){
            var lay_cont=gettext('两次密码不一致,请重新输入');
            lay_tips(lay_cont);
            return;
        }
        if(role==''){
            var lay_cont=gettext('角色不能为空');
            lay_tips(lay_cont);
            return;
        }

        $.ajax({
            type: "POST",
            url: '/base/ajax/create_admin_user/',
            data: {
               username: username,
               password: password,
               group_id: role,
               csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){

                if(res.status==true){
                    layui_nav_each(layui_url,layui_url);
                }else{
                    res_msg(res);
                }
            }
        });
    })

});
