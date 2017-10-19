#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bbs.libs.handlers import AdminBaseHandler, JsSiteBaseHandler
import bbs.models.article_model as article_model
import bbs.libs.photo as photo_tools


class ArticleManageHandler(AdminBaseHandler):
    operation = "帖子后台管理页面"

    def get(self):
        self._render()

    def _render(self, form_data=None, form_errors=None):
        self.render(
            "manage_posts.html", form_data=form_data, form_errors=form_errors
        )


class ArticleDeletehHandler(JsSiteBaseHandler):
    operation = "删除帖子"

    def post(self, *args, **kwargs):
        pass

    def _render(self, form_data=None, form_errors=None):
        self.render(
            "edit.html", form_data=form_data, form_errors=form_errors
        )

urls = [
    (r"/admin/manage/posts/?", ArticleManageHandler),
    (r"/admin/posts/delete/?", ArticleDeletehHandler),

]