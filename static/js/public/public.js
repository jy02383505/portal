var task_data_text = localStorage.getItem("task_data");  //执行时间
task_data = JSON.parse(task_data_text); //转为JSON
var menus=menus;
var user_perm=user_perm;
var lan=parent.document.getElementById('lang').value;

layui.use(['element','table','layer'], function(){   //导航栏
    var element = layui.element;
    if(menus  != null){
        var mean='';
        for(var i=0;i<menus.length;i++){
            if(lan == 'en'){
                menus[i].name=menus[i].en_code
            }
            if(menus[i].child==''){
                mean +='<li class="layui-nav-item layui-nav-itemed layui_li">' +
                '<a href="javascript:;">'+menus[i].name+'</a>' +
                '</li>';
            }else{
                // if(menus[i].show_flag == true) {
                    mean += '<li class="layui-nav-item layui-nav-itemed">' +
                    '<a href="javascript:;" >' + menus[i].name + '</a>';
                    mean += '<dl class="layui-nav-child">';
                    for (var j = 0; j < menus[i].child.length; j++) {
                        if(lan == 'en'){
                            menus[i].child[j].name=menus[i].child[j].en_code
                        }
                        mean += '<dd><a href="?#='+menus[i].child[j].url+'='+menus[i].order+','+menus[i].child[j].order+'" url="' + menus[i].child[j].url + '">' + menus[i].child[j].name + '</a></dd>';
                    }
                    mean += '</dl>';
                    mean += '</li>';
                // }
            }
        }

        $('#layui-nav').html(mean);
    }

    element.render();
    // document.getElementById('iframe_admin').contentWindow.location.reload(true);
    element.on('nav(navigation)', function(elem){
        var layui_url=elem.attr('href');
        var layui_href=layui_url.split('=');
        $('#iframe_admin').attr('src',layui_href[1]);
        $('#iframe_admin').attr('url',layui_href[2]);
        parent.layer.closeAll();
    });

    var url=location.href.split('=');
    $(function(){
        if(url.length==1){
            var layui_url=$('#layui-nav li:first-child dl dd:first-child a').attr('url');
            $('#iframe_admin').attr('src',layui_url);
            $('#layui-nav li:first-child dl dd:first-child ').attr('class','layui-this');
        }else{
            $('#iframe_admin').attr({'src':url[1],'url':url[2]});

        }
        // $('.layui-nav .layui-nav-child dd').removeClass('layui-this');
        $('.layui-nav .layui-nav-child a').each(function(){
            var iframe_src=$('#iframe_admin').attr('url');
            var layui_url=$(this).attr('href');
            var layui_href=layui_url.split('=');
            if(layui_href[2] == iframe_src && iframe_src != '/'){
                $(this).parent().attr('class','layui-this');
            }
        });
    });

    setTimeout(function () {
        window.addEventListener("popstate", function () {   //浏览器回退按钮监听
            window.location.reload();
            if(url.length==1){
                var layui_url=$('#layui-nav li:first-child dl dd:first-child a').attr('url');
                $('#iframe_admin').attr('src',layui_url);
                $('#layui-nav li:first-child dl dd:first-child ').attr('class','layui-this');
            }else{
                $('#iframe_admin').attr('src',url[1]);
                $('#iframe_admin').attr('url',url[2]);
            }
            $('.layui-nav .layui-nav-child a').each(function(){
                var iframe_src=$('#iframe_admin').attr('url');
                var layui_url=$(this).attr('href');
                var layui_href=layui_url.split('=');
                if(layui_href[2] == iframe_src && iframe_src != '/'){
                    $(this).parent().attr('class','layui-this');
                }
            });
        }, false);
    }, 500);

});







