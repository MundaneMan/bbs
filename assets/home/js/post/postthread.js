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
        }, selectFormChange: function () {
            $(".dropdown_text_middle").on({
                mouseleave: function (e) {
                    $(this).children(".selectlist").hide()
                }
            }).find("span,i").on({
                click: function (e) {
                    $(this).siblings(".selectlist").toggle()
                }
            }).end().find(".selectlist").delegate("li", "click", function (e) {
                var s = $(this).html();
                var val = $(this).attr("value");
                $(this).parents(".dropdown_text_middle").children("span").html(s).attr("value", val);
                $(".selectlist").hide()
            })
        }, checkWrapChange: function () {
            $(".check_wrap").parent().on("click", function (e) {
                var $checkwrap_i = $(this).find("i"), $checkbox = $(this).children("input");
                if ($checkbox.attr("readonly")) {
                    return
                } else if ($checkwrap_i.hasClass("check_center")) {
                    $checkwrap_i.removeClass("check_center");
                    $checkbox.attr("checked", false)
                } else {
                    $checkwrap_i.addClass("check_center");
                    $checkbox.attr("checked", true)
                }
                return false
            })
        }, titleLiChange: function () {
            var $oTitleLi = $(".session2 .title li"), $oTitleUl = $(".session2 .title_select"),
                $oTitleSelectLi = $oTitleUl.children("li");
            $oTitleLi.on("click", function () {
                var i = $(this).index();
                $oTitleUl.show();
                $oTitleLi.removeClass("current").eq(i).addClass("current");
                $oTitleSelectLi.removeClass("current").eq(i).addClass("current")
            })
        }, listChange: function () {
            var _t = this, $selectPlate = $(".selectPlate"), $selectPlateSpan = $selectPlate.find("span").eq(0),
                $oselectPlatelist = $(".selectPlatelist"), $selectPlateLi = $oselectPlatelist.find("li"),
                $oSelect = $(".selectlist");
            $selectPlateSpan.on("click", function (e) {
                $oselectPlatelist.slideToggle("slow")
            });
            $oselectPlatelist.on("mouseleave", function (e) {
                $(this).slideUp("slow")
            });

            function ajaxFun(fid, liname) {
                $.ajax({
                    url: "/thread/type",
                    data: {forum_id: fid},
                    type: "POST",
                    dataType: "json",
                    success: function (data) {
                        if (data.header.code == 1e5) {
                            var val = data.body.list.data;
                            if (val.length != 0) {
                                var s = "";
                                for (var i = 0; i < val.length; i++) {
                                    s += "<li value='" + val[i].typeid + "'>" + val[i].name + "</li>"
                                }
                                $(".selectclassify ul").html(s).siblings("span").attr("value", val[0].typeid).html(val[0].name)
                            } else {
                                $(".selectclassify ul").html("").siblings("span").attr("value", 0).html(langgobale[42].string)
                            }
                            if (arguments.length == 3) {
                                $selectPlateSpan.attr("value", fid).html(liname)
                            }
                            $oselectPlatelist.fadeOut();
                            var selectgenre = $(".selectgenre span").attr("value");
                            var rights = data.body.rights;
                            var o = $(".selectgenre").find("ul");
                            if (rights.special == 2) {
                                o.html('<li value="1">普通</li>')
                            } else {
                                var snormal = '<li><span class="J_changetype_normal">普通</span></li>';
                                if (selectgenre == 1) {
                                    snormal = '<li value="1">普通</li>'
                                }
                                o.html(snormal);
                                if (rights.activity == 1) {
                                    var sactivity = '<li><span class="J_changetype_activity">活动</span></li>';
                                    if (selectgenre == 2) {
                                        sactivity = '<li value="2">活动</li>'
                                    }
                                    o.append(sactivity)
                                }
                                if (rights.poll == 1) {
                                    var svote = '<li><span class="J_changetype_vote">投票</span></li>';
                                    if (selectgenre == 4) {
                                        svote = '<li value="4">投票</li>'
                                    }
                                    o.append(svote)
                                }
                                if (rights.rush == 1) {
                                    var srush = '<li><span class="J_changetype_rush">抢楼</span></li>';
                                    if (selectgenre == 5) {
                                        srush = '<li value="5">抢楼</li>'
                                    }
                                    o.append(srush)
                                }
                            }
                        } else {
                            _t.notieFun(data.header.desc)
                        }
                    }
                })
            }

            var spanvalue = $selectPlateSpan.attr("value");
            if (spanvalue != 0) {
                ajaxFun(spanvalue)
            }
            $selectPlateLi.on("click", function () {
                var forum_id = $(this).attr("value");
                var name = $(this).html();
                ajaxFun(forum_id, name)
            });
            for (var i = 0, len = $selectPlateLi.length; i < len; i++) {
                if (i % 6 == 5) {
                    $selectPlateLi.eq(i).css({"border-right": "none"})
                }
            }
        }, changeTypeFun: function () {
            var fid = tid = "", type = $(".selectgenre ul").attr("type");

            function changeType(postType) {
                fid = $(".selectPlate").find("span").attr("value");
                tid = $(".selectclassify").find("span").attr("value");
                window.location.href = "/thread/" + postType + "/fid/" + fid + "/filter/" + tid + "/type/" + type
            }

            $("body").delegate(".J_changetype_normal", "click", function (event) {
                changeType("add")
            });
            $("body").delegate(".J_changetype_activity", "click", function (event) {
                changeType("activity")
            });
            $("body").delegate(".J_changetype_vote", "click", function (event) {
                changeType("poll")
            });
            $("body").delegate(".J_changetype_rush", "click", function (event) {
                changeType("rush")
            })
        }, hideUeditorBtnFun: function (argument) {
            if ($("#editor").attr("isuploadattach") == 2) {
                setTimeout(function () {
                    $("#editor").find("#edui30,#edui35,#edui51").css({width: "0", height: "0", margin: "0"})
                }, 100)
            }
        }, init: function () {
            var _t = this;
            _t.selectFormChange();
            _t.checkWrapChange();
            _t.titleLiChange();
            _t.listChange();
            _t.changeTypeFun();
            _t.hideUeditorBtnFun()
        }
    };
    xmbbs.init()
});