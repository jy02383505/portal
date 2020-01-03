layui.use(['table','form','layer','laypage'], function() {
    var form = layui.form;
    var table = layui.table;
    var layer = layui.layer;
    var form_top = top.layui.form;
    var cache_type_list='';    //缓存类型
    for(var cache in cache_type){
        var cache=cache_type[cache];
        if(cache.id=='suffix'){
            cache_type_list += '<input type="radio" lay-filter="add_cache_type" name="add_cache_type" id="'+cache.id+'" value="'+cache.name+'" ' +
            'title="'+gettext(cache.name)+'" checked>';
        }else{
            cache_type_list += '<input type="radio" lay-filter="add_cache_type" name="add_cache_type" id="'+cache.id+'" value="'+cache.name+'" ' +
            'title="'+gettext(cache.name)+'">';
        }
    }

    form.on('radio(src_type)',function(){    //回源方式切换
        this_input_radio(this,'ip')
    });

    form.on('radio(src_back_type)',function(){    //备份源站类型切换
        var src_back_type_checked = $(this).attr('data-check');
        var src_this=$(this);
        $('input[name="src_back_type"]').each(function () {
           $(this).attr('data-check', "false");
           if(src_back_type_checked == 'true'){
               // $(this).attr('data-check', "false");
               src_this.attr('data-check', "false");
               src_this.prop('checked', false);
           }else{
               $(this).attr('data-check', "false");
               src_this.attr('data-check', "true");
               src_this.prop('checked', true);
           }
        });
        layui.form.render();
        this_input_radio(this,'ip');
    });

    var this_input_radio=function(data,data_ip){
        var this_data=$(data).parents('.layui-form-item').next();
        if(data.value==data_ip){
            this_data.find('.layui-textarea').show();
            this_data.find('.layui-input').hide();
        }else{
            this_data.find('.layui-textarea').hide();
            this_data.find('.layui-input').show();
        }
    };

    form.on('radio(source_host_type)',function(data){    //回源host
        console.log(data.value)
        if(data.value == gettext('默认') || data.value == 0){
            $('input[name="domain_src_host"]').prop("disabled",true);
        }else{
            $('input[name="domain_src_host"]').removeAttr("disabled",false);
            $('input[name="domain_src_host"]').removeClass("layui-disabled");
        }
        if(data.value == gettext('默认')){
            $('#source_host').val($('#domain').val())
        }else if(data.value == gettext('自定义')){
            $('#source_host').val('')
        }
        if(data.value == 0){
            console.log($('#domain').text())
            $('input[name="domain_src_host"]').val($('#domain').text())
        }else if(data.value == 1){
            $('input[name="domain_src_host"]').val('')
        }
    });

    $(document).on('click','.move_up',function(){
        if($(this).attr('class').indexOf('active')<0){
            moveup($(this).parents('tr'));
        }
    });
    $(document).on('click','.move_down',function(){
         if($(this).attr('class').indexOf('active')<0){
             movedown($(this).parents('tr'));
        }
    });

    var add_cache=function(obj,this_edit){

        var this_content='';
        var this_times='';
        var this_company='';

        if(this_edit != undefined){
            this_content=this_edit[1];
            this_times=this_edit[2];
            this_company=this_edit[3];
            var lay_title=gettext('编辑缓存配置')
        }else{
            var lay_title=gettext('添加缓存配置')
        }
        if(this_content==gettext('全部文件')){
            this_content='/.*';
        }
        var content='<div class="layui-form" style="padding:0 20px;">' +
                    '<div class="layui-form-item">' +
                    '   <label class="layui-form-label">'+gettext('缓存类型')+'</label>' +
                    '   <div class="layui-input-block">'+cache_type_list+'</div>' +
                    '</div>'+
                    '<div class="layui-form-item">' +
                    '   <label class="layui-form-label">'+gettext('缓存内容')+'</label>' +
                    '   <div class="layui-input-block">' +
                    '     <input type="text" style="width:248px;" value="'+this_content+'" id="cache_content" name="title" lay-verify="title" autocomplete="off" placeholder="" class="layui-input">'+
                    '   </div>' +
                    '<p class="remark_p" style="padding-left: 100px;">'+gettext('文件类型必须是以.开头的文件后缀，如.jpg')+'</p>'+
                    '</div>'+
                    '<div class="layui-form-item">' +
                    '   <label class="layui-form-label">'+gettext('缓存时间')+'</label>' +
                    '   <div class="layui-input-block cache_layui_select">' +
                            '<input type="text" id="caching_times" name="title" value="'+this_times+'" lay-verify="title" autocomplete="off" placeholder="" class="layui-input">'+
                            '<div class="layui-input-block" style="margin-left: 8px;">'+
                                '<select name="select_time" id="select_time" >' +
                                    '<option value="1">'+gettext('秒')+'</option>' +
                                    '<option value="60">'+gettext('分')+'</option>' +
                                    '<option value="3600">'+gettext('小时')+'</option>' +
                                    '<option value="86400">'+gettext('天')+'</option>' +
                                '</select>'+
                            '</div>' +
                        '</div>' +
                    '</div>'+
                '</div>';
        top.layer.open({
            type: 1
            , title: lay_title
            , area: ['460px', '330px']
            , shade: 0
            , btnAlign: 'c'
            , offset: 'auto'
            , id: 'add_cache'
            ,skin:'layer_class'
            , content: content
            , btn: [gettext('确定'), gettext('取消')]
            , yes: function (index_ado) {
                 var add_cache_val=$('input[name="add_cache_type"]:checked',parent.document).val();
                 var add_cache_id=$('input[name="add_cache_type"]:checked',parent.document).attr('id');
                 var cache_content=$('#cache_content',parent.document).val();
                 var caching_times=$('#caching_times',parent.document).val();
                 var select_time=$('#select_time option:selected',parent.document).text();
                 var select_val=$('#select_time option:selected',parent.document).val();
                 var last_td='<td class="cache_td" id="'+add_cache_id+'"><span>'+gettext(add_cache_val)+'</span></td>' +
                     '<td class="cache_td" id="'+cache_content+'"><span>'+cache_content+'</span></td>' +
                     '<td class="cache_td" id="'+caching_times*select_val+'"><span>'+caching_times+'</span><span>'+select_time+'</span></td>' +
                     '<td><div class="cache_sort"><span class="move_down"></span><span class="move_up"></span></div>' +
                     '<div class="cache_btn"><a class="layui-btn layui-btn-xs layui_edit" lay-event="edit">'+gettext('编辑')+'</a>' +
                     '<a class="layui-btn layui-btn-xs layui_del" lay-event="del">'+gettext('删除')+'</a></div></td>';
                 if(obj !=undefined && obj.attr('id') == 'cdn_type_last'){
                     var cache_tbody_tr='<tr id="cdn_type_last">'+last_td+'</tr>'
                 }else{
                     var cache_tbody_tr='<tr>'+last_td+'</tr>'
                 }
                 if($('#cache_tbody').html()==''){
                     $('#cache_tbody').html(cache_tbody_tr);
                 }else if($('#cache_tbody').html() !='' && this_edit == undefined){
                     if($('#cache_tbody tr:last-child').attr('id')=='cdn_type_last'){
                         $('#cache_tbody tr:last-child').before(cache_tbody_tr);
                     }else{
                         $('#cache_tbody').append(cache_tbody_tr);
                     }

                 }else if(this_edit != undefined){
                     obj.replaceWith(cache_tbody_tr);
                 }

                 $('#cdn_type_last .layui_del').addClass('btn_gray').removeClass('layui_del');
                 top.layer.close(index_ado);
                 table.render();

            }

        });


        if(obj !=undefined && obj.attr('id') == 'cdn_type_last'){
            $('input[name="add_cache_type"],#cache_content',parent.document).attr('disabled','disabled');
            $('input[name="add_cache_type"],#cache_content',parent.document).addClass('layui-btn-gray');
        }

        if(lan == 'en'){
            $('.layui-layer-content .layui-form-label',parent.document).width(102)
            $('.remark_p',parent.document).css('padding-left','112px');
        }
        $('select[name="select_time"] option',parent.document).each(function(){
            if(this_company == $(this).text()){
                $(this).attr('selected',true)
            }
        })

        var cache_type_radio=function(data){   //缓存类型提示

            var remark_p_text='';
            if(data=='文件' || data==gettext('文件')){
                remark_p_text=gettext('文件类型必须是以.开头的文件后缀，如.jpg')
            }else if(data=='文件夹' || data==gettext('文件夹')){
                if(obj !=undefined &&  obj.attr('id') == 'cdn_type_last'){
                    remark_p_text='the path to the entire site is /.*'
                }else{
                    remark_p_text=gettext('文件夹必须是以/开头的文件后缀，如/abc')
                }

            }else if(data=='全路径'){
                remark_p_text=gettext('全路径必须以“/”开头，支持*匹配某一类型文件')
            }
            $('#add_cache',parent.document).find('.remark_p').text(remark_p_text);

        };
        form_top.on('radio(add_cache_type)',function(data){    //缓存类型提示切换
            cache_type_radio(data.value);
        });

        if(this_edit != undefined){    //编辑缓存规则

            var add_cache_type=parent.document.getElementsByName('add_cache_type');
            for(var i=0;i<add_cache_type.length;i++){
                if(gettext(add_cache_type[i].value)==this_edit[0]){
                    add_cache_type[i].checked=true;
                }
            }
            cache_type_radio(this_edit[0]);
            $('#select_time option').each(function(){
                if($(this).text()==this_edit[3]){
                    $(this).attr('selected',true);
                }
            });
        }


        form_top.render();
    };
    form.on('submit(add_cache)',function(){   //添加缓存规则
        add_cache();
    });
    $(document).on('click','.layui_del',function(){   //删除缓存规则
        var lay_del=gettext('确定删除此条缓存配置？');
        var obj=$(this).parents('tr');
        lay_delete(lay_del,obj);

    })

    $(document).on('click','.layui_edit',function(){     //编辑缓存规则
        var obj=$(this).parents('tr');
        var this_edit=[];
        obj.find('.cache_td span').each(function(){
            this_edit.push($(this).text());
        });
        add_cache(obj,this_edit);

    });

    form.on('submit(priority_adjust)',function(){    //调整优先级
        var cache_tbody_tr_length=document.getElementById('cache_tbody').childNodes.length;
        if(cache_tbody_tr_length >1){
            var cache_tbody_html=$('#cache_tbody').html();
            initTable();
            $('.cache_sort').show();
            $('.cache_btn').hide();
            $("#add_cache_id").addClass("layui-btn-gray").prop("disabled",true);
            form.on('submit(sure_sort)',function(){
                $("#add_cache_id").removeClass("layui-btn-gray").removeAttr("disabled",false);
                $('.cache_sort').hide();
                $('.cache_btn').show();

            });
            form.on('submit(cancel_sort)',function(){
                $('#cache_tbody').html(cache_tbody_html);
                $('.cache_sort').hide();
                $('.cache_btn').show();
                $("#add_cache_id").removeClass("layui-btn-gray").removeAttr("disabled",false);

            });
        }
    });
    function initTable(){
        $('#cache_tbody tr .move_up').removeClass('active');
        $('#cache_tbody tr .move_down').removeClass('active');
        $('#cache_tbody tr:first-child .move_up').addClass('active');
        if($('#cache_tbody tr:last-child').attr('id')=='cdn_type_last'){
            $('#cache_tbody tr:last-child').prev('tr').find('.move_down').addClass('active');
        }else{
            $('#cache_tbody tr:last-child .move_down').addClass('active');
        }

    };
    function moveup(obj){
        var html=$(obj).html();
        $(obj).prev().before("<tr>"+html+"</tr>");
        $(obj).remove();
        initTable();
    }
    function movedown(obj){
        var html=$(obj).html();
        $(obj).next().after("<tr>"+html+"</tr>");
        $(obj).remove();
        initTable();
    }

    $(".layui-icon-help").hover(function() {
        $(this).parent().find('.remarks_span').show();
    }, function() {
        $(this).parent().find('.remarks_span').hide();
    });
    $('.ssl_cert').on('click',function(){
        var cert_list='';
        if(is_staff == 'True'){
            cert_list='/cert/admin_cert_ssl_manage/page/'
        }else if(is_staff == 'False'){
            cert_list='/cert/client_cert_ssl_manage/page/'
        }
        layui_nav_each(cert_list,cert_list);
        form.render();
    })
})

