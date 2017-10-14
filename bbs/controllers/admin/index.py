#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bbs.libs.handlers import AdminBaseHandler
import tornado


class IndexHandler(AdminBaseHandler):
    def get(self):
        self.render('index.html')


class DataTableHandler(AdminBaseHandler):
    def get(self):
        self.render('datatable.html')


urls = [
    (r"/admin/?", IndexHandler),
    (r"/admin/index/?", IndexHandler),
    (r"/admin/datatable/?", DataTableHandler)
    ]


class AdminMenuModule(tornado.web.UIModule):
    def render(self, module_name="index", tpl="admin/left.html"):
        return self.render_string(tpl, module_name=module_name)


class AdminPageModule(tornado.web.UIModule):
    def render(self, baseurl, start, count, perpage, tpl="admin/a_m_page.html"):
        return self.render_string(tpl, baseurl=baseurl, start=start, count=count, perpage=perpage)

ui_modules = {
    "AdminMenuModule": AdminMenuModule,
    "AdminPageModule": AdminPageModule,
}