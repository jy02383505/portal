//提交
layui.use('layer',function(){

    var layer=layui.layer;
    var csrftoken_first=$.cookie('csrftoken');
    var csrftoken_key=csrftoken_first.slice(0,16);
    var csrftoken_last=csrftoken_first.slice(48,64);

    function encrypt(word) {      //加密
        var key = CryptoJS.enc.Utf8.parse(csrftoken_key); //16位
        var iv = CryptoJS.enc.Utf8.parse(csrftoken_last);
        var encrypted = '';
        if (typeof(word) == 'string') {
            var srcs = CryptoJS.enc.Utf8.parse(word);
            encrypted = CryptoJS.AES.encrypt(srcs, key, {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            });
        } else if (typeof(word) == 'object') { //对象格式的转成json字符串
            data = JSON.stringify(word);
            var srcs_data = CryptoJS.enc.Utf8.parse(data);
            encrypted = CryptoJS.AES.encrypt(srcs_data, key, {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            })
        }
        return encrypted.ciphertext.toString();
    }

    function decrypt(word){      //解密代码
        if(word != null){
            var key = CryptoJS.enc.Utf8.parse(csrftoken_key);
            var iv = CryptoJS.enc.Utf8.parse(csrftoken_last);
            var encryptedHexStr = CryptoJS.enc.Hex.parse(word);
            var srcs = CryptoJS.enc.Base64.stringify(encryptedHexStr);
            var decrypt = CryptoJS.AES.decrypt(srcs, key, {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            });
            var decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
            return decryptedStr.toString();
        }
    }


    document.onkeydown = function (e){
        var theEvent = window.event || e;
        var code = theEvent.keyCode || theEvent.which;
        if(code == 13){
            login();
            return false;
        }
    }

    jQuery(function(){
         //获取cookie的值
         var username = $.cookie('username');
         var password = $.cookie('password');

         if(password != null){
             var key='e0274b6f';
             var password_open=CryptoJS.AES.decrypt(password,key).toString(CryptoJS.enc.Utf8);
             $('#username').val(username);
             $('#password').val(password_open);
             if(username != null && username != '' && password != null && password != ''){ //选中保存秘密的复选框
              $("#remember_password").addClass('group_checked');
             }
         }
         //将获取的值填充入输入框中

    });
    window.login = function(){
        // 登录
        var uname = $('#username').val();
        var pwd = $('#password').val();
        var password_key = encrypt(pwd);    //密码加密

        var key='e0274b6f';
        var password_cook= CryptoJS.AES.encrypt(pwd, key);

        if ($('#remember_password').hasClass('group_checked')) {//保存密码
            $.cookie('username', uname, {expires: 7, path: '/'});
            $.cookie('password', password_cook, {expires: 7, path: '/'});
        } else {//删除cookie
            $.cookie('username', '', {expires: -1, path: '/'});
            $.cookie('password', '', {expires: -1, path: '/'});
        }
        var index = layer.load(1);
        $.ajax({

            url: "/base/ajax/login/",
            data: {
                username: uname,
                password: password_key,
                pl:pwd.length,   //
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            /*xhrFields   : {withCredentials: true},
            crossDomain : true,*/
            type: 'post',
            async: false,
            error: function () {
                layer.close(index);
                var edit_msg = '<p class="mistake">' + internation_trans.communication + '</p>';
                $('#uname_tip').html(edit_msg);
                $('#uname_tip').show();
            },
            success: function (data) {
                layer.close(index);
                if (data.status) {
                    var task_data = data.menus;
                    task_data = JSON.stringify(task_data);
                    localStorage.setItem("task_data", task_data);
                    window.location.href = '/base/base/';

                } else {
                    var edit_msg = '<p class="mistake">' + gettext(data.msg)+ '</p>';
                    $('#uname_tip').html(edit_msg);
                    $('#uname_tip').show();
                }
            },

        });
    }

});

//注册
window.onload=function(){
    $("#register").click(function () {
      location.href='/accounts/register/';
    });
}

//忘记密码
$(document).ready(function(){
    $(".logoin-input input").focus(function(){
      $('#uname_tip').hide();
    });
});
$(document).on('click','#remember_password',function(){   //记住密码
    if($(this).hasClass('group_checked')){
        $(this).removeAttr("checked", false);
        $(this).removeClass('group_checked');
    }else{
        $(this).prop("checked",true);
        $(this).addClass('group_checked');
    }
});

$('.logoin-input input').each(function(){    //删除账号和密码
    if($(this).val()==''){
        $(this).parent().find('.delete_image').hide();
    }else{
        $(this).parent().find('.delete_image').show();
    }
});
$(document).on('click','.delete_image',function(){
    $(this).parent().find('input').val('');
    $(this).hide();
    $(this).parent().find('input').css('cssText','border:1px solid #2b80e2 !important');
    $(this).parent().find('input').focus();

});

//翻译
function selectlang() {
    var str="/i18n/setlang/";
    myform = document.getElementById('testform');
    myform.method = "POST";
    myform.action = str;
    if ($("#user_lang_en") && $("#user_lang_en").html() =='中文'){
        $("#language").val("zh-Hans");}
    else
        $("#language").val("en");
    myform.submit();
}


