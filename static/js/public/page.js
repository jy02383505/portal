//分页
var lan=parent.document.getElementById('lang').value;
function toPage(curr,count,limit){

    layui.use('laypage', function(){
        var laypage = layui.laypage;
        laypage.render({
            elem: 'page'
            ,count:count             //总条数
            ,curr:curr               //当前页
            ,layout: ['count', 'prev', 'page', 'next', 'skip']
            ,prev: '<em><</em>'
            ,next: '<em>></em>'
            ,skip:'go'
            ,limit:limit
            // ,layout: ['prev', 'page', 'next','skip']
            ,jump: function(obj,first){

                /*if(lang>'en'){
                    $('.layui-laypage-count').text(internation_trans.total+count);
                }*/
                if(lan == 'zh'){
                    $('.layui-laypage-count').text('共'+count+'条');
                }else{
                    $('.layui-laypage-count').text('Total '+count);
                }
                var laypage_txt='<input type="text" min="1" value="1" class="layui-input">' +
                        '<button type="button" class="layui-laypage-btn">Go</button>';
                $('.layui-laypage-skip').html(laypage_txt);
                $(".layui-laypage-skip").find("input").val(curr);
                if(!first){
                    data_search();
               }
            }
        });
    })
}
