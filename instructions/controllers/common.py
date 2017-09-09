#!/usr/bin/env python
# -*- coding: utf-8 -*-

from instructions.libs.captcha import Captcha
from instructions.libs.handlers import BaseHandler
from cStringIO import StringIO


class VerifyCodeHandler(BaseHandler):
    operation = u"用户请求验证码"

    def get(self, *args, **kwargs):
        self.set_header("Content-Type", "image/png")
        img, chars = Captcha.get(self)
        buf = StringIO()
        img.save(buf, 'PNG', quality=70)
        self.write(buf.getvalue())


urls = [
    (r"/verify_code\.png/?", VerifyCodeHandler),
    ]