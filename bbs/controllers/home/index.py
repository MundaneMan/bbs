#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from bbs.libs.handlers import HomeBaseHandler
import bbs.models.article_model as article_model


class IndexHandler(HomeBaseHandler):
    def get(self):
        articles = article_model.list_articles_by_cond({"status": "normal"}, limit=10)
        self.render('index.html', articles=articles)


class ContactHandler(HomeBaseHandler):
    def get(self):
        self.render('contact.html')


class Error404Handler(HomeBaseHandler):
    def get(self):
        self.render('error_404.html')


class InformationHandler(HomeBaseHandler):
    operation = "请求资讯页面"

    def get(self):
        self.render('information.html')


urls = [
    (r"/", IndexHandler),
    (r"/index/?", IndexHandler),
    (r"/contact/?", ContactHandler),
    (r"/error/404/?", Error404Handler),
    (r"/information/?", InformationHandler),
    ]


class HomePageModule(tornado.web.UIModule):
    def render(self, baseurl, start, count, perpage, tpl="admin/paged.html"):
        return self.render_string(tpl, baseurl=baseurl, start=start, count=count, perpage=perpage)

ui_modules = {
    "HomePageModule": HomePageModule
}
