function setIframeHeight(iframe) {
    var iframe_height=$(".body_list").height();
    if (iframe) {
        var iframeWin = iframe.contentWindow || iframe.contentDocument.parentWindow;
        if (iframeWin.document.body) {
            iframe.height = iframe_height;
        }
    }
}

$("#iframe_admin",parent.document).each(function () {

    var that = $(this);
    (function(){
        setTimeout(function() {
            setIframeHeight(that[0]);
        }, 500)
    })(that)
});

$("#iframe_admin",parent.document).each(function () {
    var that = $(this);
    var times=(function () {
        setInterval(function () {
            setIframeHeight(that[0]);
        }, 200)
    })(that)
    clearInterval(times);
});




