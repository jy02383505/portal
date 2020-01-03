var safe_domain=parent_split[parent_split.length-1];   //域名
var domain_id=parent_oblique[parent_oblique.length-2]; //域名id
var safe_data=parent_oblique[parent_oblique.length-4]; //域名 配置/统计
var safe_url='';   //导航地址

if(is_staff == 'True'){
    safe_url='/sec/admin_sec_domain_list/page/';

}else if(is_staff == 'False'){
    safe_url='/sec/parent_sec_domain_list/page/';
}

$('#domain').attr('domain_id',domain_id);
$('#domain').text(safe_domain);
$('#waf_domain').text(safe_domain);

layui.use('form', function() {
    var form = layui.form;

    var channel_select=document.getElementById('channel_select');
    if(safe_data == 'admin_domain_waf_register' || safe_data == 'admin_domain_waf_create'){
        $('.conf_a ').hide();
    }
    var channel_select_option= channel_select.options;
    for (var i=0;i<channel_select_option.length;i++){
        if(channel_select_option[i].value==safe_data){
            channel_select_option[i].selected=true;
        }
    }
    form.on('select(channel_select)',function(obj){
        var this_value=obj.value;
        var url_upload='/sec/'+this_value+'/page/'+domain_id+'/';
        layui_nav_each(url_upload,safe_url,safe_domain);
    })

    if(lan=='en'){
        $('.channel_choice ').width(165);
    }else{
        $('.channel_choice').width(80);
    }

    form.render();
})


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

