layui.use(['form'], function(){
    var form=layui.form;
    form.on('submit(lay_submit)',function(){
        var password=document.getElementById('password').value
        var new_password=document.getElementById('new_password').value
        var confirm_password=document.getElementById('confirm_password').value
        if(password  =='' || new_password == '' || confirm_password == ''){
            lay_tips(gettext('密码不能为空'))
            return;
        }else if(!regExp.test(new_password) || !regExp.test(confirm_password)){
            lay_tips(gettext('密码格式不正确'))
            return;
        }else if(new_password != confirm_password){
            lay_tips(gettext('两次密码不一致'))
            return;
        }
        $.ajax({
            type: "POST",
            url: '/base/ajax/client_reset_password/',
            data: {
                password: new_password,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async: false,
            success: function (res) {
                console.log(res)
                if(res.status){
                   // window.location.href='/base/logout/'
                }else{
                    lay_tips(res)
                }

            }
        })
    })
})

$(".layui-icon-help").hover(function() {
    $(this).parent().find('.remarks_span').show();
}, function() {
    $(this).parent().find('.remarks_span').hide();
});