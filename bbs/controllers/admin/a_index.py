#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bbs.libs.handlers import AdminBaseHandler
import tornado


class IndexHandler(AdminBaseHandler):
    def get(self):
        self.render('index.html')


class ErrorPageHandler(AdminBaseHandler):
    def get(self):
        self.render('error.html')


class FormPageHandler(AdminBaseHandler):
    def get(self):
        self.render('form.html')


class ImageListHandler(AdminBaseHandler):
    def get(self):
        self.render('imglist.html')


class SelfDefHandler(AdminBaseHandler):
    def get(self):
        self.render('self_def.html')


class ToolsHandler(AdminBaseHandler):
    def get(self):
        self.render('tools.html')


class FilesHandler(AdminBaseHandler):
    def get(self):
        self.render('filelist.html')


class TabHandler(AdminBaseHandler):
    def get(self):
        self.render('tab.html')


class WorkbenchHandler(AdminBaseHandler):
    def get(self):
        self.render('default.html')


class ComputerHandler(AdminBaseHandler):
    def get(self):
        self.render('computer.html')

urls = [
    (r"/admin/?", IndexHandler),
    (r"/admin/index/?", IndexHandler),
    (r"/admin/error_page/?", ErrorPageHandler),
    (r"/admin/form/?", FormPageHandler),
    (r"/admin/imagelist/?", ImageListHandler),
    (r"/admin/self_def/?", SelfDefHandler),
    (r"/admin/tools/?", ToolsHandler),
    (r"/admin/files/?", FilesHandler),
    (r"/admin/tab/?", TabHandler),
    (r"/admin/workbench/?", WorkbenchHandler),
    (r"/admin/computer/?", ComputerHandler)
    ]


class AdminMenuModule(tornado.web.UIModule):
    def render(self, module_name="index", tpl="admin/a_m_left.html"):
        return self.render_string(tpl, module_name=module_name)

ui_modules = {
    "AdminMenuModule": AdminMenuModule
}
