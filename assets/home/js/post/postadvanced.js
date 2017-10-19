
//-------内容提示还剩余多少可输入字数----------
_editor = CKEDITOR.replace('ckeditor');
//控制帖子的最大长度
var maxlength = 10000;
_editor.on('key', function (event) {

    var oldhtml = _editor.document.getBody().getHtml();
    var description = oldhtml.replace(/<.*?>/ig, "");
    var _slen = maxlength - description.length - 1;
    var _label = $("#canwrite");
    //alert(description.length);
    if (description.length >= maxlength) {
        //alert("最多可以输入"+maxlength+"个文字，您已达到最大字数限制");
        //_editor.setData(oldhtml);
        _label.css({"background-color": "red"});
        _label.html("还可以输入" + _slen + "个字,超出部分将不会被保存.");
    } else {
        _label.css({"background-color": "white"}).html("还可以输入" + _slen + "字");
    }
});

//----------发布帖子和暂存帖子-------------------
$("#btn_publish").click(function () {
    $("#form_publish").submit();
});
//var editor = CKEDITOR.replace('editor');
var editor = _editor;
$(function () {
    if (window.localStorage) {
        storage_name = "article_tmp";
        $("#save").click(function () {
            var text = editor.getData();
            window.localStorage.setItem(storage_name, text);
        });
        var text = window.localStorage.getItem(storage_name);
        if (text) {
            editor.setData(text);
        }
        setInterval(function () {
            $("#save").click();
        }, 10000);
    } else {
        $("#save").click(function () {
            alert("你的浏览器不支持临时存储");
        });
    }
});

//--------------标题提示还剩余多少可输入字数----------------------------
$(".importtopic input").keyup(function (e) {
    var val = $(this).val();
    var realLength = val.length;
    if (realLength > 90) {
        $(this).val(val.substring(0, 90));
        return false
    }
    $(".importtopic .label").html("还可输入 " + (90 - realLength) + " 个字符");
    if (90 == realLength) {
        $(".importtopic .label").css({"color": "red"});
    } else {
        $(".importtopic .label").css({"color": "#8c8c8c"});
    }
});

//--------即时预览本地图片-----------------------------------
function getFileUrl(sourceId) {
    var url;
    if (navigator.userAgent.indexOf("MSIE") >= 1) { // IE
        url = document.getElementById(sourceId).value;
    } else if (navigator.userAgent.indexOf("Firefox") > 0) { // Firefox
        url = window.URL.createObjectURL(document.getElementById(sourceId).files.item(0));
    } else if (navigator.userAgent.indexOf("Chrome") > 0) { // Chrome
        url = window.URL.createObjectURL(document.getElementById(sourceId).files.item(0));
    }
    return url;
}

function preImg(sourceId, targetId) {
    var url = getFileUrl(sourceId);
    var imgPre = document.getElementById(targetId);
    imgPre.src = url;
}
$("#main_photo").dblclick(function () {
   // alert("双击");
   $("#imgOne").trigger("click");
});
//-------------------------------------------------------------