#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bbs.libs.handlers import AdminBaseHandler, JsSiteBaseHandler
import bbs.models.article_model as article_model
import bbs.libs.photo as photo_tools


class ArticleManageHandler(AdminBaseHandler):
    operation = "帖子后台管理页面"

    def get(self):
        base_url = u"/admin/articles?"
        per_page = int(self.get_argument('perpage', "30"))
        count = article_model.list_articles_by_cond({"status": "normal"}, _is_count=True)
        if per_page <= 0:
            per_page = 30
        articles = [article_model.format_article(a) for a in
                    article_model.list_articles_by_cond({"status": "normal"}, start=self.start, limit=per_page)]
        self._render("w_articles/w_articles.html", articles=articles, base_url=base_url, start=self.start,
                     count=count, per_page=per_page)

    def _render(self, form_data=None, form_errors=None, **kwargs):
        self.render(
            "manage_posts.html", form_data=form_data, form_errors=form_errors, **kwargs
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