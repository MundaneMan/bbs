#!/usr/bin/env python
# -*- coding: utf-8 -*-

from instructions.libs.handlers import HomeBaseHandler, JsSiteBaseHandler
from instructions.libs.captcha import Captcha
import instructions.models.article_model as article_model
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
        form_errors = self._validate_require_form_data(form_data)
        if form_errors:
            self._render(form_data,form_errors)
            return
        article_model.insert_article(form_data)

    def _render(self,form_data=None, form_errors=None):
        self.render(
            "edit_article.html", form_data=form_data, form_errors=form_errors
        )

    def _list_form_keys(self):
        return ["title", "content"]

    def _list_required_form_keys(self):
        return ["title", "content"]

urls = [
    (r"/article/edit/?", ArticlePublishHandler),
    ]