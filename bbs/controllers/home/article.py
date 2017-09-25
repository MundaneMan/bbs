#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bbs.libs.handlers import HomeBaseHandler, JsSiteBaseHandler
from bbs.libs.captcha import Captcha
import bbs.models.article_model as article_model
import time
import string


class ArticleBaseHandler(HomeBaseHandler):
    def render(self, template_name, **kwargs):
        super(ArticleBaseHandler, self).render("article/"+template_name, **kwargs)


class ArticlePublishHandler(ArticleBaseHandler):
    def get(self, *args, **kwargs):
        self._render()

    def post(self, *args, **kwargs):
        form_data = self._build_form_data()
        print form_data
        form_errors = self._validate_require_form_data(form_data)
        if form_errors:
            self._render(form_data, form_errors)
            return
        article_id = article_model.insert_article(form_data)
        self.redirect("/article/view/{}/".format(str(article_id)))

    def _render(self, form_data=None, form_errors=None):
        self.render(
            "article_edit.html", form_data=form_data, form_errors=form_errors
        )

    def _list_form_keys(self):
        return ["title", "content"]

    def _list_required_form_keys(self):
        return ["title", "content"]


class ArticleViewHandler(ArticleBaseHandler):
    def get(self, article_id):
        print article_id
        article = article_model.load_article_by_id(article_id)
        print article
        if article:
            self.render("article_view.html", article=article)
        else:
            self.redirect("/")


urls = [
    (r"/article/edit/?", ArticlePublishHandler),
    (r"/article/view/(\w+)/?", ArticleViewHandler),
    ]