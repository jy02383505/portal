var parent_href=window.parent.location.href;  //浏览器url
var parent_split=parent_href.split('=');

if(parent_split.length>1){
    var parent_oblique=parent_split[1].split('/');
}
var layui_url=$('#layui-nav .layui-nav-child .layui-this a',parent.document).attr('url');   //被选中导航url
var regExp=/^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,21}$/;   //密码验证   6-20位数字、字母组合，区分大小写
var lan=parent.document.getElementById('lang').value;        //获取语言

function removeEmpty(arr){       //去掉空数组
  for(var i = 0; i < arr.length; i++) {
   if(arr[i] == "" || typeof(arr[i]) == "undefined") {
      arr.splice(i,1);
      i = i - 1; // i - 1 ,因为空元素在数组下标 2 位置，删除空之后，后面的元素要向前补位
    }
   }
   return arr;
}

function split_array(arr, len){   //分数组
    var a_len = arr.length;
    var result = [];
    for(var i=0;i<a_len;i+=len){
        result.push(arr.slice(i,i+len));
    }
    return result;
}

//进制
function fmoney(s, n) {
    n = n > 0 && n <= 20 ? n : 2;
    s = parseFloat((s + "").replace(/[^\d\.-]/g, "")).toFixed(n) + "";
    var l = s.split(".")[0].split("").reverse(), r = s.split(".")[1];
    t = "";
    for (i = 0; i < l.length; i++) {
    t += l[i] + ((i + 1) % 3 == 0 && (i + 1) != l.length ? "," : "");
    }
    return t.split("").reverse().join("") + "." + r;
}

var csrftoken_first=$.cookie('csrftoken');    //加密
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

function numFormat(num){    //千分位
  var res=num.toString().replace(/\d+/, function(n){ // 先提取整数部分
       return n.replace(/(\d)(?=(\d{3})+$)/g,function($1){
          return $1+",";
        });
  })
  return res;
}
/*layui.use(['layer'], function(){
    var layer=layui.layer;*/

    var lay_load = function(){    //加载loading
        parent.layer.load(1);
    };

    var lay_tips =function(lay_cont,layer_loading){    //报错信息
        if(lan == 'en') {
            var area = ['500px', '200px'];
        }else{
            var area = ['420px','200px'];
        }
        parent.layer.open({
            title:gettext('提示'),
            type: 1,
            shade:0,
            area:area,
            offset:'auto',
            content:'<div class="lay_content" style="padding:20px 40px;">'+lay_cont+'</div>',  //这里content是一个普通的String
            end:function(){
                  layer.close(layer_loading);
                  top.layer.close(layer_loading)

            }
        });
    };

    var lay_tips_second=function(lay_cont,lay_title){
        layer.alert(lay_cont, {
            title:lay_title,
            icon: 0,
            shade:0,
            area:['500px','230px'],
            btn:[gettext('确定'),gettext('取消')],
            btnAlign:'c',
            // skin: 'layer-ext-moon', //该皮肤由layer.seaning.com友情扩展。关于皮肤的扩展规则，去这里查阅
            yes:function() {

            }
        });
    }

    var lay_delete =function(lay_del,obj){    //删除信息
        layer.open({
              title:gettext('删除'),
              skin:'skin_class',
              type: 1,
              shade:0,
              area:['400px','200px'],
              btn: [gettext('确定'),gettext('取消')],
              content:'<div class="lay_content">'+lay_del+'</div>',  //这里content是一个普通的String
              yes:function(index){
                  layer.close(index);
                  obj.remove();

              }
        });
    };
// });/**/
var parent_url='';   //跳转页面
var parent_name='';

var layui_nav_each=function(url,sort_list,data_name,data_domain){    //跳转页面
    //url   跳转url     //sort_list   导航url        //data_name   参数1       //data_domain   参数2
    parent_split=parent_href.split('=');
    $('.layui-nav a',parent.document).each(function(){
        var url_a=$(this).attr('href');
        var url_split=url_a.split('=');
        if(url_split[1]==sort_list){
            /*if(parent_split.length==1){
                parent_url=parent_split[0]+'?#='
            }else{
                parent_url=parent_split[0]+'='
            }*/
            /*if(parent_split.length==1){
                client_url='?#='+url + '=' + url_split[2]+parent_name
            }else{
                client_url='='+url + '=' + url_split[2]+parent_name
            }*/

            if(data_name != undefined){
                parent_name= '='+data_name
            }
            if(data_domain != undefined){
                parent_name= '='+data_name +'='+ data_domain
            }
            parent.layer.closeAll();
            var client_url='?#='+url + '=' + url_split[2]+parent_name;  //子页面
            //var iframe_url=
            // window.parent.location.href = parent_url + url + '=' + url_split[2]+parent_name;

            parent.window.history.pushState({status: 0} ,'' ,client_url);
            parent.document.getElementById('iframe_admin').contentWindow.location.reload(true);
            $('#iframe_admin',parent.document).attr('src',url);
            $('#iframe_admin',parent.document).attr('url',url_split[2]);
            $('#layui-nav li dd',parent.document).removeClass('layui-this');
            $(this).parent().addClass('layui-this').siblings().removeClass('layui-this');
            //
        }
    })

};


$(document).on('click','.layui-icon-return',function(){   //返回导航页面
    var url_list=$('.layui-nav .layui-this a',parent.document).attr('url');
    layui_nav_each(url_list,url_list);
})


var layui_nav_key=function(page_list,parent_split,domain_page,domain_id,domain_key){    //跳转页面
    $('.layui-nav a',parent.document).each(function(){
        var url_a=$(this).attr('href');
        var url_split=url_a.split('=');
        if(url_split[1]==page_list){
            $("#container",parent.document).attr('src','/base/'+domain_page+'/page/');
            $("#container",parent.document).attr('url',url_split[2]);
            if(parent_url.length==1){
                window.parent.location.href=parent_split+'?=/sec/'+domain_page+'/page/'+domain_id+'/='+url_split[2]+'='+domain_key;
            }else{
                window.parent.location.href=parent_split+'=/sec/'+domain_page+'/page/'+domain_id+'/='+url_split[2]+'='+domain_key;
            }
        }
    })
};


var lay_time = function(lay_cont){    //刷新提示
    layer.msg('<p class="time_loading"><img alt="nova portal" style="display:inline-block;" src="/static/image/time_loading.png" />'+lay_cont+'</p>', {
        title:gettext('提示'),
        time: 2000, //不自动关闭
      area:['500px','150px']
    });
};

var fuzzy_search=function(this_value,storeId){     //模糊查询
    setTimeout(function(){
        var rowsLength=storeId.childNodes.length;
        for(var i=0;i<rowsLength;i++){
            if(storeId.childNodes[i].className.indexOf('layui-form-checkbox') !== -1){
                var searchText = storeId.childNodes[i].innerText;
                if(searchText.match(this_value)){

                    storeId.childNodes[i].style.display='inline-block';
                }else{
                    storeId.childNodes[i].style.display='none';
                }
            }
        }
    },200);
};

var res_msg=function(res){    //列表获取报错
    if(res.msg !='' && res.msg != undefined){
        lay_tips(res.msg);
    }else{
        lay_tips(gettext('通讯异常'));
    }
};
var res_table=function(res,table_list,curr){   //table报错
    if(table_list !='' && table_list !=undefined){
       var count=res.page_info.total;
       toPage(curr,count);
       $('#page').show();
    }else{
        $('#page').hide();
        table_list=[];
    }
};




