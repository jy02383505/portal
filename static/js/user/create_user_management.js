var parent_href=window.parent.location.href;  //浏览器url
var parent_url=parent_href.split('=');

var ajax_list='';  //页面列表
var navigation_url='';  //操作列表

if(parent_url[1]=='/base/create_child_user/page/'){     //新建用户

    ajax_list='create_child_user';
    navigation_url='parent_child_list';
    var cols=[
          {field:'username',title:'用户名' }
          ,{field:'email',title:'邮箱'}
          ,{field:'mobile',title: '电话'}
          ,{field:'remark',title:'备注'}
          ,{field:'password',title: '登录密码',templet: function (d){
            return "<p class='password_eye' id='"+d.password+"' >******</p>"}}
          ,{field:'secret_key',title:'密钥'}
        ]

}
console.log(perm_strategy_list);
var strategy_list='';
for(var perm_strategy in perm_strategy_list){
    var perm_strategy=perm_strategy_list[perm_strategy];
    strategy_list +='<li id="'+perm_strategy.id+'"><p>'+perm_strategy.name+'</p><span>'+perm_strategy.remark+'</span></li>'
}

$('.policy').html(strategy_list);

layui.use(['form','table','element','layer'], function(){
    var form = layui.form;
    var table = layui.table;
    var layer=layui.layer;
    var lay_tips =function(lay_cont){    //报错信息
        layer.open({
              title:'提示',
              type: 1,
              shade:0,
              btn:'确定',
              btnAlign: 'c', //按钮居中
              content:'<div class="lay_content" style="padding: 20px 100px;">'+lay_cont+'</div>'  //这里content是一个普通的String
        });
    };


    document.getElementById('step_first').onclick=step_first;
    function step_first(){

        //var password_reg=/^[\\S]{6,12}$/;   //密码
        var password_reg = /([a-zA-Z0-9!@#$%^&*()_?<>{}]){5,11}/;
        var email_reg=/^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/;   //邮箱
        var phone_reg=/^1[34578]\d{9}$/;   //手机号
        if(parent_url[1]=='/base/create_parent_user/page/'){     //新建用户
           var username=$('#username').val();
            if(username==''){
                var lay_cont='用户名不能为空';
                lay_tips(lay_cont);
                return;
            }
            var company=$('#company').val();
            if(company==''){
                var lay_cont='公司名称不能为空';
                lay_tips(lay_cont);
                return;
            }
            var mobile=$('#mobile').val();
            if(!phone_reg.test(mobile) && mobile !=''){
                var lay_cont='联系电话格式不正确';
                lay_tips(lay_cont);
                return;
            }
            var email=$('#email').val();
            if(!email_reg.test(email) && email !=''){
                var lay_cont='邮箱格式不正确';
                lay_tips(lay_cont);
                return;
            }
            var password=$('#password').val();
            if(password==''){
                var lay_cont='控制台密码不能为空';
                lay_tips(lay_cont);
                return;
            }
            if(!password_reg.test(password)){
                var lay_cont='密码必须6到12位';
                lay_tips(lay_cont);
                return;
            }

        }else if(parent_url[1]=='/base/admin_group_create/page/'){   //新建角色
            var name=$('#name').val();
            if(name==''){
                var lay_cont='角色不能为空';
                lay_tips(lay_cont);
                return;
            }

        }
        document.getElementById('lay_form').style.display='none';
        document.getElementById('lay_second').style.display='block';
        document.getElementById('strategy').style.display='block';
        alert(1);

        $('.progress li:nth-child(2)').addClass('active');
    }

    document.getElementById("step_pre").onclick = step_pre;
    function step_pre(){

        document.getElementById('lay_form').style.display='block';
        document.getElementById('lay_second').style.display='none';
        $('.progress li:nth-child(2)').removeClass('active');
    }

    $(document).on('click','.policy li',function(){       //新建用户
        $(this).clone();
        var img='<img src="/static/image/bin.png" />';
        if(!$(this).hasClass('gray')){
            if($('.added').html()==''){
                $('.added,.permission_ul').html($(this).clone());

            }else{
                $('.added,.permission_ul').prepend($(this).clone());
            }
        }
        $(this).addClass('gray');
        $('.added li').append(img);

    });
    $(document).on('click','.added li img',function(){       //新建用户
        // $(this).clone();
        var add_id=$(this).parent().attr('id');
        $('.policy li').each(function(){
            if($(this).attr('id')==add_id){
                $(this).removeClass('gray');
            }

        });
        $(this).parent('li').remove();

    });


    document.getElementById("step_third").onclick = step_third;
    function step_third(){
        //window.location.href=''
        // ;
          //window.location.href='';

        document.getElementById('lay_second').style.display='block';
        document.getElementById('lay_last').style.display='none';
        $('.progress li:nth-child(3)').removeClass('active');
    }


    //页面数据
    function data_aggregation(){
        var username=$('#username').val();   //新建用户
        var email=$('#email').val();
        var mobile=$('#mobile').val();
        var remarks=$('#remark').val();
        var password=$('#password').val();
 /*       var user_id='';
        var user_value='';
        var user_type = document.getElementsByName('user_type');
        for(var i=0;i<user_type.length;i++){
            if(user_type[i].checked){
                user_id = user_type[i].id;
                user_value = user_type[i].value;
            }
        }

        // var access_id='';
        var access_value=[];
        var access_type = document.getElementsByName('access_type');
        for(var i=0;i<access_type.length;i++){
            if(access_type[i].checked){
                access_value.push[access_type[i].value];
            }

        }*/
        if(parent_url[1]=='/base/create_child_user/page/'){
            if(document.getElementById('is_api').checked==true){
               var is_api='1'
            }else{
               var is_api='0'
            }

            if(document.getElementById('is_active').checked){
               var is_active='1';
            }else{
               var is_active='0'
            }

            if(document.getElementById('reset_password').checked){
               var reset_password='1';
            }else{
               var reset_password='0'
            }
        }
        var permission_id=[];
        $('.permission_ul li').each(function(){
            permission_id.push($(this).attr('id'));
        });

        var role_list={
               'username': username,
               'mobile': mobile,
               'email': email,
               'password':password,
               'reset_password':reset_password,
               'remarks':remarks,
               'is_api':is_api,
               'is_active':is_active,
               'perm_strategy':permission_id
        }
        return role_list;
    }
    document.getElementById("step_next").onclick = step_next;
    function step_next(){
        var aggregation=data_aggregation();
        console.log(aggregation);
        $('.progress li:nth-child(3)').addClass('active');

        table.render({
            elem: '#role_table'
            ,data:[aggregation]
            ,cols: [cols]
            ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
            ,done:function(res, curr, count){

            },
        });
        document.getElementById('lay_form').style.display='none';
        document.getElementById('lay_second').style.display='none';
        document.getElementById('lay_last').style.display='block';
    }
    $(document).on('click','.password_eye',function(){
        if($(this).hasClass('eye')){
            $(this).text('******');
            $(this).removeClass('eye');
        }else{

            $(this).text($(this).attr('id'));
            $(this).addClass('eye');
        }

    })

    document.getElementById("step_over").onclick = step_over;
    function step_over(){
        var aggregation=data_aggregation();
        console.log(aggregation);
        $.ajax({
            type: "POST",
            url: '/base/ajax/'+ajax_list+'/',
            data:{
                username: aggregation.username,
                mobile: aggregation.mobile,
                email: aggregation.email,
                remark: aggregation.remarks,
                reset_password: aggregation.reset_password,
                password: aggregation.password,
                is_api:aggregation.is_api,
                is_active:aggregation.is_active,
                perm_strategy:aggregation.perm_strategy,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            async:false,
            success: function(res){
                console.log(res);
                if(res.status){
                    $('.layui-nav a',parent.document).each(function(){
                        var url_a=$(this).attr('href');
                        var url_split=url_a.split('=');
                        if(url_split[1]=='/base/'+navigation_url+'/page/') {
                            $("#container", parent.document).attr('src', '/base/' + navigation_url + '/page/');
                            $("#container", parent.document).attr('url', url_split[2]);
                            window.parent.location.href = parent_url[0] + '=/base/' + navigation_url + '/page/=' + url_split[2];
                        }
                    })
                }else{
                    lay_tips(res.msg);

                }
            }
        });
    }

});
