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


class ErrorPageHandler(AdminBaseHandler):
    def get(self):
        self.render('error.html')


urls = [
    (r"/admin/?", IndexHandler),
    (r"/admin/index/?", IndexHandler),
    (r"/admin/datatable/?", DataTableHandler),
    (r"/admin/error_page/?", ErrorPageHandler)
    ]


class AdminMenuModule(tornado.web.UIModule):
    def render(self, module_name="index", tpl="admin/left.html"):
        return self.render_string(tpl, module_name=module_name)

ui_modules = {
    "AdminMenuModule": AdminMenuModule
}
