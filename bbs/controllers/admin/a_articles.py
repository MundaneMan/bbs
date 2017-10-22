#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bbs.libs.handlers import AdminBaseHandler, JsSiteBaseHandler
import bbs.models.article_model as article_model
import bbs.libs.photo as photo_tools


class ArticleManageHandler(AdminBaseHandler):
    operation = "帖子后台管理页面"

    def get(self):
        base_url = u"/admin/articles?"
        count = article_model.list_articles_by_cond({"status": "normal"}, _is_count=True)

        articles = [article_model.format_article(a) for a in
                    article_model.list_articles_by_cond({"status": "normal"}, start=self.start, limit=self.limit)]
        self._render(articles=articles, base_url=base_url, start=self.start,
                     count=count, per_page=self.limit)

    def _render(self, form_data=None, form_errors=None, **kwargs):
        self.render(
            "a_posts.html", form_data=form_data, form_errors=form_errors, **kwargs
        )


class ArticleDeleteHandler(JsSiteBaseHandler):
    operation = "删除帖子"

    def post(self, *args, **kwargs):
        pass

urls = [
    (r"/admin/posts/?", ArticleManageHandler),
    (r"/admin/posts/delete/?", ArticleDeleteHandler),
]