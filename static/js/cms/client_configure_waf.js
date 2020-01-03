layui.use(['table','form','laypage','element'], function() {

    $('.edit_add').on('click',function(){
        $(this).parents('.label_item').find('.user_details').hide();
        $(this).parents('.label_item').find('.user_add').show();
    })

    var default_rules='';
    var default_sure=document.getElementById('default_sure');
    var self_sure=document.getElementById('self_sure');
    default_sure.onclick=function(){
        var obj=this;
        var default_waf_mode=$('#waf_default option:selected').val();
        var waf_name=$('#waf_default option:selected').text();
        var waf_default_cname=$('#waf_default_cname').text();
        var self_waf_mode='';
        waf_sure(default_waf_mode,self_waf_mode,obj,waf_name,waf_default_cname);
    };
    self_sure.onclick=function(){
        var obj=this;
        var self_waf_mode=$('#waf_self option:selected').val();
        var waf_name=$('#waf_self option:selected').text();
        var waf_self_cname=$('#waf_self_cname').text();
        var default_waf_mode='';
        waf_sure(default_waf_mode,self_waf_mode,obj,waf_name,waf_self_cname);
    };

    window.waf_sure=function(default_waf_mode,self_waf_mode,obj,waf_name,waf_cname){
        if(waf_name == waf_cname){
            lay_tips(gettext('该防御模式未修改'))
            return;
        }
        // var index = layer.load(1);
        var loading = top.layer.load(1, {
            shade: [0.4,'#fff']
        });
        $.ajax({      //配置页面基础信息
            type: "POST",
            url: set_ajax_list,
            data: {
                domain_id: domain_id,
                default_waf_mode: default_waf_mode,
                self_waf_mode: self_waf_mode,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async: false,
            success: function (res) {
                parent.layer.close(loading);
                if(res.status==true){
                    window.location.reload();
                }else{
                    res_msg(res);
                }

            }
        })
    }

});
