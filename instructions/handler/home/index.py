#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from instructions.libs.handlers import HomeBaseHandler


class IndexHandler(HomeBaseHandler):
    def get(self):
        self._render('index.html')


urls = [
    (r"/?", IndexHandler),
    (r"/index/?", IndexHandler),
    ]


class AdminNavModule(tornado.web.UIModule):
    def render(self, tpl="admin/a_m_nav.html"):
        return self.render_string(tpl)


class AdminPageModule(tornado.web.UIModule):
    def render(self, baseurl, start, count, perpage, tpl="admin/a_m_page.html"):
        return self.render_string(tpl, baseurl=baseurl, start=start, count=count, perpage=perpage)

ui_modules = {
    "AdminNavModule": AdminNavModule,
    "AdminPageModule": AdminPageModule,
}