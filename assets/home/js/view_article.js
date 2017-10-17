$(function () {
    function watchByMobile(argument) {
            var oWatchmobile = $(".watchmobileThread"), oInfor = oWatchmobile.find(".infor"),
                oWatchmobile_picwrap = oWatchmobile.find(".watchmobileThread_picwrap");
            var timer = "";
            oWatchmobile.hover(function () {
                timer = setTimeout(function (argument) {
                    oInfor.addClass("active");
                    oWatchmobile_picwrap.slideDown()
                }, 100)
            }, function (argument) {
                clearTimeout(timer);
                oWatchmobile_picwrap.slideUp("normal", function (argument) {
                    oInfor.removeClass("active")
                })
            })
        };
    watchByMobile();
})



/*$(function () {
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
        }, personLayer: function () {
            var _t = this;
            var timoutid = 0;
            $(".contain_right").delegate(".reply_con .user_head", {
                mouseenter: function () {
                    var _this = $(this);
                    timoutid = setTimeout(function () {
                        var parent = _this.parents("li");
                        if (parent.children(".personLayer").length > 0) {
                            parent.children(".personLayer").show()
                        } else {
                            parent.prepend('<p class="loading">' + langgobale[153].string + "</p>");
                            var uid = parent.attr("u-id");
                            var avatar = _this.attr("src");
                            var username = parent.find(".reply_list_con .auth_name").html();
                            $.ajax({
                                url: hosturl + "/user/getavatar",
                                data: {uid: uid},
                                type: "POST",
                                dataType: "json",
                                success: function (data) {
                                    if (data.header.code == 1e5) {
                                        var dataval = data.body;
                                        var vipstring = "<i class='" + parent.find(".reply_list_con .auth_name").next().attr("class") + "'></i>";
                                        var imggroup = "";
                                        var d = dataval.uvipmedal.data;
                                        for (var obj in d) {
                                            var json = d[obj];
                                            imggroup += "<a href='" + json.link + "' target='_blank'><img src='" + json.image + "'></a>"
                                        }
                                        var s = "<div class='personLayer person'><div class='personLayer_msg'><a href='/user/detail/miid/" + uid + "' target='_blank'><img src='" + avatar + "' class='user_pic'/></a><div class='user_msg'><p><a href='/user/detail/miid/" + uid + "' class='user_name' target='_blank'>" + username + "</a>" + vipstring + "</p><p><span class='txt'>" + dataval.title + "</span></p></div></div><ol class='clearfix'><li><span class='num'>" + dataval.credits + "</span><span class='txt'>" + langgobale[154].string + "</span></li><li class='integral'><span class='num'>" + dataval.exp + "</span><span class='txt'>" + langgobale[55].string + "</span></li><li><span class='num'>" + dataval.devote + "</span><span class='txt'>" + langgobale[155].string + "</span></li></ol><p class='badge'>" + imggroup + "</p><div class='btnwrap'><a class='btn' href='/user/detail/miid/" + uid + "' target='_blank'>" + langgobale[166].string + "</a><span class='btn btn-blue J_sendmsg' u-id='" + uid + "'>" + langgobale[165].string + "</span></div></div> ";
                                        $(".loading").before(s).remove()
                                    } else if (data.header.code == 200004) {
                                        $(".loading").remove();
                                        _t.notieFun(data.header.desc)
                                    } else {
                                        _t.notieFun(data.header.desc)
                                    }
                                }
                            })
                        }
                    }, 500)
                }, mouseleave: function () {
                    clearTimeout(timoutid);
                    $(this).parents("li").children(".personLayer").hide()
                }
            }).delegate(".personLayer", {
                mouseenter: function () {
                    $(this).show()
                }, mouseleave: function () {
                    $(this).hide()
                }
            })
        }, extendClick: function () {
            var $contain_left = $(".contain_left"), $oUnfold = $contain_left.find(".unfold"),
                $oPersonLayer = $contain_left.find(".personLayer"), $oHonor = $contain_left.find(".honor"),
                $oextendBtn = $contain_left.find(".extend_btn");
            $oextendBtn.on({
                click: function () {
                    $oUnfold.show()
                }
            });
            $oUnfold.on({
                mouseleave: function () {
                    $oUnfold.hide()
                }
            })
        }, windowScoll: function () {
            $(".container_wrap").append('<span class="return" >' + langgobale[68].string + "</span>");
            $("body").delegate(".return", "click", function () {
                $("html,body").animate({scrollTop: "0px"}, 200)
            })
        }, escape: function (html) {
            return String(html).replace(/&(?!\w+;)/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;")
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
        }, charCodeAtFun: function (val) {
            var realLength = 0;
            for (var i = 0, len = val.length; i < len; i++) {
                var charCode = val.charCodeAt(i);
                if (charCode >= 0 && charCode <= 128) realLength += 1; else realLength += 2
            }
            return realLength
        }, fastpublishClick: function () {
            var _t = this;
            var $faster_reply = $(".faster_reply");
            var $oReplyarea = $(".reply_area");
            var title_id = $(".filtrate").attr("date-id"), fid = $(".filtrate").attr("f-id"), groupName = "";
            groupName = $(".user_wrap .user_con .uname").html();
            if (groupName == langgobale[42].string) {
                groupName = ""
            }
            document.onkeydown = function (event) {
                var e = event || window.event;
                var a = e.keyCode;
                if (a == 13 && event.ctrlKey) {
                    if (document.activeElement.id == "J_txt") {
                        $("#J_fastpublish").click()
                    }
                    if (document.activeElement.id == "editor") {
                        $("#J_reply").click()
                    }
                    if (document.activeElement.id == "J_scollReplytxt") {
                        $("#J_scollReply").click()
                    }
                }
            };
            var $o = $(".faster_reply").find(".headportrait");
            var vips = "";
            if ($o.attr("u-auth") == 1) {
                vips = '<i class="vip_icon vip_icon_s"></i>';
                if ($o.attr("u-vip") == 1) {
                    var n = $o.attr("u-level") > 0 ? $o.attr("u-level") : "v";
                    vips = '<i class="vip_icon vip_icon_s' + n + '"></i>'
                }
            }

            function publishcallback(value, pid, link, position) {
                var d = new Date, vYear = d.getFullYear(), vMon = d.getMonth() + 1, vDay = d.getDate(),
                    h = d.getHours(), m = d.getMinutes(), s = d.getSeconds(),
                    time = vYear + langgobale[156].string + vMon + langgobale[157].string + vDay + langgobale[158].string + h + ":" + m + ":" + s,
                    $ohead = $faster_reply.find(".headportrait"), orderby = $(".reply_nav").find(".current").index(),
                    img = $ohead.html(), name = $(".J_userInfo .user_name").html(), ulink = $ohead.attr("href"),
                    uid = $ohead.attr("u-id"),
                    postmanage = $ohead.attr("post-manage") == 1 ? '<input type="checkbox" />' : "",
                    postmanage2 = $ohead.attr("post-manage") == 1 ? '<span class="replay_btn supervisebtn">' + langgobale[75].string + "</span>" : "",
                    comment = $ohead.attr("post-comment") == 1 ? '<span class="replay_btn remark_btn">' + langgobale[48].string + "</span>" : "",
                    rate = $ohead.attr("post-rate") == 1 ? '<span class="replay_btn J_grade">' + langgobale[51].string + "</span>" : "",
                    s_num = "";
                switch (position) {
                    case 1:
                        s = "shafa";
                        s_num = langgobale[69].string;
                        break;
                    case 2:
                        s = "bandeng";
                        s_num = langgobale[70].string;
                        break;
                    case 3:
                        s = "diban";
                        s_num = langgobale[71].string;
                        break;
                    default:
                        s = "";
                        s_num = position + "#";
                        break
                }
                var str = '<li class="clearfix" post-id="' + pid + '" u-id="' + uid + '" ><div class="reply_list_img"><a href="' + ulink + '" target="_blank">' + img + "</a>" + postmanage + '</div><div class="reply_list_con"><div class="auth_msg clearfix"><a href="' + ulink + '" class="auth_name" target="_blank">' + name + "</a>" + vips + "<span>" + groupName + "</span><span>" + langgobale[72].string + "</span><span>" + time + '</span><span class="reply_list_float ' + s + '">' + s_num + '</span></div><div class="reply_txt">' + value + '</div><p class="replay_bu clearfix">' + postmanage2 + rate + '<a href="/post/edit/thread_id/' + title_id + "/post_id/" + pid + '" class="replay_btn">' + langgobale[73].string + '</a><a href="/post/reply/thread_id/' + title_id + "/post_id/" + pid + '" class="replay_btn">' + langgobale[74].string + "</a>" + comment + "</p></div></li>";
                if ($(".contain_right").find(".reply").length == 0) {
                    var string = '<div class="reply"><div class="reply_con"><div class="reply_title clearfix"><h3>' + langgobale[76].string + '</h3><span class="replay_num">0</span></div><ul class="reply_list">' + str + "</ul></div></div>";
                    $oReplyarea.before(string);
                    var postmanage = $faster_reply.find(".headportrait").attr("post-manage");
                    if (postmanage == 1 && $(".flotation").length == 0) {
                        var flotationstring = "<div class='flotation'><h4>" + langgobale[83].string + "<span class='themenum'>0</span>" + langgobale[78].string + "<span class='closebtn'></span><span class='allcheck_txt'>" + langgobale[79].string + "</span><input type='checkbox' name='allcheck'></h4><p><span id='J_reply_warn'>" + langgobale[80].string + "</span><span class='move_btn' id='J_reply_delete'>" + langgobale[159].string + "</span><span class='shield' id='J_reply_shield'>" + langgobale[81].string + "</span><span id='J_reply_stick'>" + langgobale[82].string + "</span></p></div>";
                        $(".reply_list").after(flotationstring);
                        var $oFlotation = $(".flotation");
                        $oFlotation.css({width: "200px"}).find("p").css({margin: "20px 0 15px 18px"})
                    }
                } else {
                    if (orderby == 1) {
                        $(".reply_title").siblings("ul").append(str)
                    } else {
                        $(".reply_title").siblings("ul").prepend(str)
                    }
                }
                var $oNum = $(".replay_num");
                var n = parseInt($oNum.html()) + 1;
                $oNum.html(n);
                $faster_reply.find("input").val("");
                $(".scollReplyWrap").find("input").val("");
                UE.getEditor("editor").setContent("");
                if ($(".hide_vb").length > 0) {
                    $(".hide_vb").html(langgobale[201].string)
                }
            }

            var time = 0;

            function publishBtnClick(value) {
                if (time == 3) {
                    _t.notieFun(langgobale[205].string);
                    return
                }
                if (value) {
                    if (_t.charCodeAtFun(value) < 5) {
                        _t.notieFun(langgobale[179].string);
                        return false
                    }
                    var v = value.replace(/<img [^>]*aid=['"]([^'"]+)[^>]*>/g, "[attachimg]" + "$1" + "[/attachimg]").replace(/<span[^>]* aid="([^'"]+)".*?>.*?<\/span><\/span>/g, "[attachment]" + "$1" + "[/attachment]");
                    if (_t.countInstances(v, "[attachimg]") > 30) {
                        _t.notieFun(langgobale[206].string);
                        return false
                    }
                    $.ajax({
                        url: "/post/add",
                        data: {tid: title_id, fid: fid, message: v, token: $("#token").val()},
                        type: "POST",
                        dataType: "json",
                        success: function (data) {
                            if (data.header.code == 4e5) {
                                publishcallback(value, data.body.data.post_id, "#", data.body.data.position);
                                _t.notieFun(data.header.desc);
                                time = 3;
                                setInterval(function () {
                                    time = 0
                                }, 3e3)
                            } else if (data.header.code == 600003) {
                                window.location.href = data.header.url
                            } else {
                                _t.notieFun(data.header.desc)
                            }
                        }
                    })
                } else {
                    _t.notieFun(langgobale[84].string)
                }
            }

            $("#J_fastpublish").on("click", function () {
                var value = $(this).prev().val();
                value = _t.escape(value);
                publishBtnClick(value)
            });
            $("#J_scollReply").on("click", function () {
                var value = $(this).prev().val();
                value = _t.escape(value);
                publishBtnClick(value)
            });
            $("#J_reply").on("click", function () {
                var value = UE.getEditor("editor").getContent();
                publishBtnClick(value);
                _msq.push(["trackEvent", "track_mul", "", "reply"])
            })
        }, attentionClick: function () {
            var _t = this;
            var $oplateinfor = $(".plateinfor");
            var $oNum = $oplateinfor.find(".num");
            var fid = $(".filtrate").attr("f-id");

            function ajax(obj, url, type) {
                $.ajax({
                    url: url,
                    data: {forum_id: fid, forum_token: forum_token},
                    type: "POST",
                    dataType: "json",
                    success: function (data) {
                        if (data.header.code == 9e5) {
                            var n = parseInt($oNum.html());
                            if (type == 0) {
                                $oNum.html(n + 1);
                                obj.html(langgobale[65].string).addClass("noattention").removeClass("attention")
                            } else {
                                $oNum.html(n - 1);
                                obj.html("+" + langgobale[66].string).addClass("attention").removeClass("noattention")
                            }
                        } else {
                            _t.notieFun(data.header.desc)
                        }
                    }
                })
            }

            $oplateinfor.delegate(".attention", "click", function () {
                ajax($(this), "/forum/focus", 0)
            }).delegate(".noattention", {
                click: function () {
                    ajax($(this), "/forum/CancelFocus ", 1)
                }, mouseenter: function () {
                    $(this).html(langgobale[67].string)
                }, mouseleave: function () {
                    $(this).html(langgobale[65].string)
                }
            })
        }, collectFun: function () {
            var _t = this;
            var tid = $(".filtrate").attr("date-id");

            function collectAjaxFun(url, type) {
                $.ajax({
                    url: url,
                    data: {id: tid, token: favorites_token},
                    type: "POST",
                    dataType: "json",
                    success: function (data) {
                        if (data.header.code == 1e5) {
                            if (type === 0) {
                                $(".J_collect").html("取消收藏").addClass("J_cancleCollect").removeClass("J_collect");
                                _t.notieFun("收藏成功")
                            } else {
                                $(".J_cancleCollect").html("收藏").addClass("J_collect").removeClass("J_cancleCollect");
                                _t.notieFun("取消收藏成功")
                            }
                        } else {
                            _t.notieFun(data.header.desc)
                        }
                    }
                })
            }

            $("body").delegate(".J_collect", "click", function () {
                collectAjaxFun("/favorites/add", 0)
            });
            $("body").delegate(".J_cancleCollect", "click", function () {
                collectAjaxFun("/favorites/delete", 1)
            })
        }, showExif: function () {
            var o = $(".invitation_content img");
            o.hover(function () {
                var parent = $(this).parent();
                parent.css({position: "relative"});
                if (parent.find(".exifwrap").length == 0) {
                    var h = o.height();
                    parent.append('<span class="exifwrap"> < span > 制造商: < /span> < span > 型号: < /span> < span > 拍摄时间: < /span> < span > 光圈: < /span> < span > 曝光时间: < /span> < span > ISO感光度: < /span> < span > 焦距: < /span> < /span>')
                } else {
                    parent.find(".exifwrap").show()
                }
            }, function () {
                o.siblings(".exifwrap").hide()
            })
        }, exifHover: function () {
            $(".invitation_content p,.reply_con p").hover(function () {
                if ($(this).find("span").eq(0).css("width") == "500px") {
                    $(this).find("a").css("color", "#ff7519")
                }
            }, function () {
                if ($(this).find("span").eq(0).css("width") == "500px") {
                    $(this).find("a").css("color", "#333")
                }
            })
        }, blockquoteFun: function () {
            var $oQuote = $(".reply_txt .quote");
            for (var i = 0; i < $oQuote.length; i++) {
                if ($oQuote.eq(i).parent("blockquote").length == 1) {
                    var parent = $oQuote.eq(i).parent("blockquote");
                    parent.css({margin: 0, padding: 0, background: "none", border: "none", lineHeight: "24px"});
                    parent.find("p").css({padding: 0, background: "none"})
                }
            }
        }, publishdraftFun: function () {
            var _t = this;
            var tid = $(".filtrate").attr("date-id"), fid = $(".filtrate").attr("f-id");
            $(".J_publish").on("click", function () {
                $.ajax({
                    url: "/thread/publishdraft",
                    data: {thread_id: tid, forum_id: fid},
                    type: "POST",
                    dataType: "json",
                    success: function (data) {
                        if (data.header.code == 5e5) {
                            var href = hosturl + "/t-" + data.body.tid;
                            window.scroll(0, 0);
                            var success = '<div class="sendSuccess"><div class="con"><p>' + langgobale[188].string + "</p>" + '<a href="' + href + '">' + "[" + langgobale[177].string + "]" + "</a>" + '<a href="' + href + '" class="link">' + langgobale[178].string + "</a>" + "</div></div>";
                            $(".main").append(success);
                            $(".sendSuccess").css({height: $(".main").height()});
                            setTimeout(function () {
                                window.location.href = href
                            }, 3e3)
                        } else {
                            _t.notieFun(data.header.desc)
                        }
                    }
                })
            })
        }, scollReplyFixFun: function () {
            var top = parseInt($(".contain_right").offset().top), o = $(".scollReplyWrap"), winh = $(window).height(),
                top1 = $(".faster_reply").offset().top, top2 = $(".reply_area").offset().top,
                height = $(".contain_left").height() + 70 - 160, htmlHeight = $("html").height(),
                scoll = $(window).scrollTop();
            o.css("top", winh - 60);
            if (top1 + 70 < winh || top2 + 70 < winh || scoll + winh > top1) {
                o.hide()
            } else {
                o.show()
            }
            if (scoll > height) {
                $(".sidebar").hide()
            }
            if (scoll < winh) {
                $(".return").hide()
            }
            $(window).scroll(function () {
                scoll = $(window).scrollTop();
                scollwinh = scoll + winh;
                top1 = $(".faster_reply").offset().top;
                top2 = $(".reply_area").offset().top;
                if ((scollwinh <= top1 + 60 || scoll < top1 + 60) && scollwinh > top1) {
                    o.hide()
                } else {
                    o.show()
                }
                if ((scollwinh <= top2 + 100 || scoll < top2 + 100) && scollwinh > top2 || scoll > top2) {
                    o.hide()
                }
                if (scoll > height - 80) {
                    $(".sidebar").hide()
                } else {
                    $(".sidebar").show()
                }
                if (scoll > 0) {
                    $(".return").show()
                } else {
                    $(".return").hide()
                }
            })
        }, coptFun: function () {
            var _t = this;
            var DEFAULT_VERSION = "8.0";
            var ua = navigator.userAgent.toLowerCase();
            var isIE = ua.indexOf("msie") > -1;
            var Version;
            var flagie8 = false;
            if (isIE) {
                Version = ua.match(/msie ([\d.]+)/)[1];
                if (Version <= DEFAULT_VERSION) {
                    flagie8 = true
                }
            }
            $("#copy_btn").on("click", function () {
                if (navigator.plugins["Shockwave Flash"] == undefined) {
                    _t.notieFun(langgobale[207].string)
                }
                if (flagie8) {
                    _t.notieFun("您的浏览器不支持一键复制功能")
                }
            });
            if (flagie8) {
                return false
            } else {
                var client = new ZeroClipboard(document.getElementById("copy_btn"))
            }
            var _href = "http://bbs.xiaomi.cn/t-" + $(".filtrate").attr("date-id");
            var href = $("h1 .name").text() + "\n" + _href + "\n" + "(" + langgobale[208].string + ")";
            client.on("ready", function () {
                $("#copy_btn").attr("data-clipboard-text", href);
                client.on("aftercopy", function (event) {
                    event.data["text/html"];
                    _t.notieFun(langgobale[202].string)
                })
            })
        }, lookPicFun: function () {
            $("body").delegate(".invitation_content img,.reply_con .reply_txt img", "click", function () {
                var picsrc = $(this).attr("src").split("?")[0];
                var modal_s1 = "<div class='pic_modelwrap'><div class='modal-backdrop'></div><div class='pic_modelcon'><span class='close'></span>",
                    modal_s2 = "</div></div>";
                $("body").append(modal_s1 + "<span class='loading'><img  src='http://c1.mifile.cn/f/i/bbs/forum/loading.gif' /></span><a target='_blank' href='" + picsrc + "'>查看原图</a>" + modal_s2);
                $(".pic_modelcon").css({"margin-top": -(300 + 32) / 2 + "px", "margin-left": -(300 + 32) / 2 + "px"});
                var img = new Image;
                img.src = picsrc;
                img.onload = function () {
                    var h = img.height, w = img.width;
                    var _size = switchMobile._isMobile ? 330 : 700;
                    if (w > _size) {
                        h = h / w * _size;
                        w = _size;
                        if (h > _size) {
                            w = w / h * _size;
                            h = _size
                        }
                    } else {
                        if (h > _size) {
                            w = w / h * _size;
                            h = _size
                        }
                    }
                    $(".pic_modelwrap .loading").remove();
                    $(".pic_modelwrap .close").after('<img src="' + picsrc + '"/>');
                    var o = $(".pic_modelwrap img");
                    o.css({height: h, width: w});
                    $(".pic_modelcon").css({"margin-top": -(h + 32) / 2 + "px", "margin-left": -(w + 32) / 2 + "px"})
                }
            });
            $("body").delegate(".pic_modelwrap .close", "click", function () {
                $(".pic_modelwrap").fadeOut("fast", function () {
                    $(this).remove()
                })
            })
        }, likeClick: function () {
            $(".like").on("click", function () {
                var s = parseInt($(this).next().text()) + 1;
                $(this).next().text(s + langgobale[61].string)
            });
            $(".no_like").on("click", function () {
                var s = parseInt($(this).next().text()) + 1;
                $(this).next().text(s + langgobale[62].string)
            })
        }, hideUeditorBtnFun: function (argument) {
            if ($("#editor").attr("isuploadattach") == 2) {
                setTimeout(function () {
                    $("#editor").find("#edui30,#edui35,#edui51").css({width: "0", height: "0", margin: "0"})
                }, 100)
            }
        }, showTwodimensionalcode: function (argument) {
            var oWatchmobile = $(".watchmobileThread"), oInfor = oWatchmobile.find(".infor"),
                oWatchmobile_picwrap = oWatchmobile.find(".watchmobileThread_picwrap");
            var timer = "";
            oWatchmobile.hover(function () {
                timer = setTimeout(function (argument) {
                    oInfor.addClass("active");
                    oWatchmobile_picwrap.slideDown()
                }, 100)
            }, function (argument) {
                clearTimeout(timer);
                oWatchmobile_picwrap.slideUp("normal", function (argument) {
                    oInfor.removeClass("active")
                })
            })
        }, lazyloadFun: function (argument) {
            $(".invitation_content img,.reply_txt img,.reply_list_img img").lazyload({effect: "fadeIn", threshold: 30})
        }, init: function () {
            var _t = this;
            _t.personLayer();
            _t.windowScoll();
            _t.extendClick();
            _t.fastpublishClick();
            _t.attentionClick();
            _t.collectFun();
            _t.exifHover();
            _t.publishdraftFun();
            _t.scollReplyFixFun();
            _t.coptFun();
            _t.hideUeditorBtnFun();
            _t.lookPicFun();
            _t.lazyloadFun();
            _t.showTwodimensionalcode();
            window.onresize = function (event) {
                _t.scollReplyFixFun()
            };
            $(".contain_right").delegate(".readstate", "click", function () {
                $(this).addClass("readstateover").removeClass("readstate")
            })
        }
    };
    if (switchMobile._isMobile) {
        var getPersonMobile = {
            $personLayer: $(".personLayer"),
            $userMsg: $(".user_msg_mobile"),
            getPerson: function () {
                this.$userMsg.append(this.$personLayer.find(".user_name").clone())
            },
            init: function () {
                if (switchMobile._isMobile) {
                    this.getPerson()
                }
            }
        };
        var _disableScollReplyFixFun = function () {
            return
        };
        $.extend(xmbbs, {scollReplyFixFun: _disableScollReplyFixFun});
        $.extend(xmbbsMobile, {getPersonMobile: getPersonMobile});
        xmbbsMobile.getPersonMobile.init()
    }
    xmbbs.init()
});*/