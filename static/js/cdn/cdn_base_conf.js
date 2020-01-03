var user_id=parent_oblique[parent_oblique.length-2];  // 用户id
var navigation_list=''; //导航页
if(parent_oblique[2] == 'admin_cdn_base_conf'){
    navigation_list='/cdn/admin_cdn_user_list/page/';
}
layui.use(['table','form','element'], function() {
    var form = layui.form;
    var table = layui.table;
    var layer = layui.layer;
    form.on('submit(submit_cdn_conf)',function(){
        var opt=$('input[name="opt_conf"]:checked').val();
        var cc_cms_template=$('input[name="cc_cms_template"]:checked').val();
        var cc_icp_check=$('input[name="cc_icp_check"]:checked').val();
        if(cc_cms_template == undefined){
            lay_tips(gettext('请选择CMS解析模板配置'));
            return;
        }else if(cc_icp_check == undefined){
            lay_tips(gettext('请选择ICP检测频率配置'));
            return;
        }
        $.ajax({
            type: "POST",
            url: '/cdn/ajax/admin_cdn_user_set_conf/',
            data: {
                user_id:user_id,
                opt:[opt],
                cc_cms_template:cc_cms_template,
                cc_icp_check:cc_icp_check,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            error:function(){
                lay_tips(gettext('通讯异常'));
            },
            success: function(res){

                if(res.status){
                    layer.close();
                    layui_nav_each(navigation_list,navigation_list);
                }else{
                    res_msg(res);

                }

            }
        })

    })


});