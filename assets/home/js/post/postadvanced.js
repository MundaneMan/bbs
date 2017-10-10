$(function () {
    xmbbs = {
        notieFun: function (msg) {
            var s1 = "<div class='modal_full in'><div class='modal-backdrop'></div><div class='modal'><span class='close'></span><h3>" + langgobale[150].string + "</h3><div>",
                s2 = "</div></div></div>";
            $("body").append(s1 + msg + s2);
            $(".modal_full").fadeIn("normal", function () {
                setTimeout(function () {
                    $(".modal_full").fadeOut("fast", function () {
                        $(this).remove()
                    })
                }, 1e3)
            })
        }, charCodeAtFun: function (val) {
            var realLength = 0;
            for (var i = 0, len = val.length; i < len; i++) {
                var charCode = val.charCodeAt(i);
                if (charCode >= 0 && charCode <= 128) realLength += 1; else realLength += 3
            }
            return realLength
        }, countInstances: function (mainStr, subStr) {
            var count = offset = 0;
            do {
                offset = mainStr.indexOf(subStr, offset);
                if (offset != -1) {
                    count++;
                    offset += subStr.length
                }
            } while (offset != -1);
            return count
        }, sendMessagge: function (flagtype, msg, realLength) {
            var _t = this;
            var forum_id = $(".selectPlate").find("span").attr("value");
            if (forum_id == 0) {
                _t.notieFun(langgobale[5].string);
                return false
            }
            var title = $(".importtopic input").val();
            if (title) {
                if (realLength > 90) {
                    _t.notieFun(langgobale[6].string);
                    return false
                }
            } else {
                _t.notieFun(langgobale[7].string);
                return false
            }
            var classifyval = $(".selectclassify").children("span").attr("value");
            if (classifyval == 0) {
                _t.notieFun(langgobale[9].string);
                return false
            }
            var moldval = $(".selectgenre").children("span").attr("value");
            if (moldval == 0) {
                _t.notieFun(langgobale[8].string);
                return false
            }
            if (!UE.getEditor("editor").hasContents()) {
                _t.notieFun(langgobale[10].string);
                return false
            }
            if (_t.charCodeAtFun(UE.getEditor("editor").getContentTxt()) < 5) {
                _t.notieFun(langgobale[11].string);
                return false
            }
            var invitationconval = UE.getEditor("editor").getContent().replace(/<img [^>]*aid=['"]([^'"]+)[^>]*>/g, "[attachimg]" + "$1" + "[/attachimg]").replace(/<span[^>]* aid="([^'"]+)".*?>.*?<\/span><\/span><\/span>/g, "[attach]" + "$1" + "[/attach]");
            var addition = {};
            var checkbox = $(".title_select input[type='checkbox']");
            for (var i = 0, len = checkbox.length; i < len; i++) {
                var o = checkbox.eq(i);
                var name = o.attr("name");
                if (o[0].checked) {
                    addition[name] = 1
                } else {
                    addition[name] = 0
                }
            }
            var json = {
                title: title,
                forum_id: forum_id,
                mold: moldval,
                classify: classifyval,
                invitationcon: invitationconval,
                addition: addition
            };
            var Isverifycode = $(".verifycode");
            if (Isverifycode.length == 1) {
                var token = $(".J_code").attr("data-token"), verifycode = $(".J_code").val();
                if (typeof token == "undefined" || token == "" || typeof verifycode == "undefined" || verifycode == "") {
                    _t.notieFun(langgobale[175].string);
                    return false
                }
                json.token = token;
                json.verifycode = verifycode
            }
            if (flagtype == 0) {
                json.status = 6
            }
            $.ajax({
                url: "/thread/add", data: json, dataType: "json", type: "POST", success: function (data) {
                    if (data.header.code == 5e5) {
                        var href = hosturl + "/t-" + data.body.tid;
                        window.scroll(0, 0);
                        var success = '<div class="sendSuccess"><div class="con"><p>' + msg + "</p>" + '<a href="' + href + '">' + "[" + langgobale[177].string + "]" + "</a>" + '<a href="' + href + '" class="link">' + langgobale[178].string + "</a>" + "</div></div>";
                        $(".postwrap").append(success);
                        setTimeout(function () {
                            window.location.href = href
                        }, 3e3)
                    } else {
                        _t.notieFun(data.header.desc)
                    }
                }
            })
        }, sendInvitation: function () {
            var _t = this;
            var addition = {};
            var realLength = 0;
            $(".importtopic input").keyup(function (e) {
                var val = $(this).val();
                realLength = _t.charCodeAtFun(val);
                if (realLength > 90) {
                    _t.notieFun(langgobale[3].string);
                    $(".importtopic .label").html(langgobale[3].string);
                    return false
                } else {
                    $(".importtopic .label").html(langgobale[173].string + (90 - realLength) + langgobale[174].string);
                    return true
                }
            });
            document.onkeydown = function (event) {
                var e = event || window.event;
                var a = e.keyCode;
                if (a == 13 && event.ctrlKey) {
                    $(".J_sendInvitation").click()
                }
            };
            $(".J_sendInvitation").on("click", function () {
                _t.sendMessagge(1, langgobale[176].string, realLength)
            });
            $(".J_savedraft").on("click", function () {
                _t.sendMessagge(0, langgobale[180].string, realLength)
            })
        }, init: function () {
            var _t = this;
            _t.sendInvitation()
        }
    };
    xmbbs.init()
});