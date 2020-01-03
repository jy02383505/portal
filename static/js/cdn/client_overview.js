var flow_month=document.getElementById('flow_month')
var bandwidth_month=document.getElementById('bandwidth_month')
var index = top.layer.load(1, {
    shade: [0.4,'#fff']
});
$.ajax({
    type: "POST",
    url: '/cdn/ajax/client_cdn_overview_data/',
    data: {
        csrfmiddlewaretoken: $.cookie('csrftoken')
    },
    // async:false,
    success: function(res){

        top.layer.close(index)
        if(res.status){
            var sum_cdn_flux=res.sum_cdn_flux;
            var sum_cdn_zero = parseInt(sum_cdn_flux);
            var sum_cdn_length = sum_cdn_zero.toString().length;
            if(sum_cdn_length>9){
                sum_cdn_flux=sum_cdn_flux/1000000;
                $('#flow_company').text('TB')
            }else if(sum_cdn_length>6){
                sum_cdn_flux=sum_cdn_flux/1000;
                $('#flow_company').text('GB')
            }else if(sum_cdn_flux <1){
                sum_cdn_flux=sum_cdn_flux*1000;
                $('#flow_company').text('KB')
            }
            flow_month.innerText=fmoney(sum_cdn_flux)

            var max_cdn=res.max_cdn;
            var max_cdn_zero = parseInt(max_cdn);
            var max_cdn_length = max_cdn_zero.toString().length;
            if(max_cdn_length>9){
                max_cdn=max_cdn/1000000;
                $('#bandwidth_company').text('TB')
            }else if(max_cdn_length>6){
                max_cdn=max_cdn/1000;
                $('#bandwidth_company').text('GB')
            }else if(sum_cdn_flux <1){
                max_cdn=max_cdn*1000;
                $('#bandwidth_company').text('KB')
            }
            bandwidth_month.innerText=fmoney(max_cdn)
        }
    }
})
var add_domain_list='/cdn/client_cdn_create_domain/page/';
var page_list='/cdn/client_get_domain_list/page/';


//本月总流量较上月同时段对比
layui.use(['table','form','layer','element'], function(){
    var form = layui.form;
    var table = layui.table;
    var element = layui.element;
    form.on('submit(add_domain)',function(){
        if(contract == '' || contract == undefined){
            lay_tips(gettext('您账号下的CDN合同已到期，暂时无法创建新的域名'))
        }else{
            layui_nav_each(add_domain_list,page_list);
        }

    })

})