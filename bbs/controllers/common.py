#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bbs.libs.captcha import Captcha
from bbs.libs.handlers import BaseHandler
from cStringIO import StringIO
import tornado.web


class VerifyCodeHandler(BaseHandler):
    operation = u"用户请求验证码"

    def get(self, *args, **kwargs):
        self.set_header("Content-Type", "image/png")
        img, chars = Captcha.get(self)
        buf = StringIO()
        img.save(buf, 'PNG', quality=70)
        self.write(buf.getvalue())


urls = [
    (r"/verify_code.png/?", VerifyCodeHandler),
    ]


class CommonPageModule(tornado.web.UIModule):
    def render(self, base_url, start, count, per_page, tpl="m_page.html"):
        return self.render_string(tpl, baseurl=base_url, start=start, count=count, perpage=per_page)

ui_modules = {
    "CommonPageModule": CommonPageModule
}
