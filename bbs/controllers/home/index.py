#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from bbs.libs.handlers import HomeBaseHandler


class IndexHandler(HomeBaseHandler):
    def get(self):
        self.render('index.html')


class ContactHandler(HomeBaseHandler):
    def get(self):
        self.render('contact.html')


class Error404Handler(HomeBaseHandler):
    def get(self):
        self.render('error_404.html')


urls = [
    (r"/", IndexHandler),
    (r"/index/?", IndexHandler),
    (r"/contact/?", ContactHandler),
    (r"/error/404/?", Error404Handler),
    ]


class HomePageModule(tornado.web.UIModule):
    def render(self, baseurl, start, count, perpage, tpl="admin/paged.html"):
        return self.render_string(tpl, baseurl=baseurl, start=start, count=count, perpage=perpage)

ui_modules = {
    "HomePageModule": HomePageModule
}
