#!/usr/bin/env python
# -*- coding: utf-8 -*-

from instructions.libs.handlers import HomeBaseHandler


class UserLoginHandler(HomeBaseHandler):
    def get(self):
        self._render('login.html')


urls = [
    (r"/user/login/?", UserLoginHandler),
    ]
