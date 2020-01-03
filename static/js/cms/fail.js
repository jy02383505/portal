var create=parent_split[parent_split.length-2];   //接入cdn状态
var safe_domain=parent_split[parent_split.length-1];   //域名
$('#domain').text(safe_domain);
if(create == 'loading'){
    $('#waf_status').text(gettext('创建中'))
    $('#waf_loading,#create_time_line').show();
}else if(create == '404'){
    $('#waf_status').text(gettext('创建失败'))
    $('#waf_fail,#create_time_line').show();
}