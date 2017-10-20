#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bbs.libs.handlers import AdminBaseHandler, JsSiteBaseHandler
import bbs.models.images_model as images_model


class ImagesManageHandler(AdminBaseHandler):
    operation = "帖子后台管理页面"

    def get(self):
        base_url = u"/admin/images/manage?"
        count = images_model.list_images_by_cond({"status": "normal"}, _is_count=True)

        images = [images_model.format_Images(a) for a in
                  images_model.list_images_by_cond({"status": "normal"}, start=self.start, limit=self.limit)]
        self._render(images=images, base_url=base_url, start=self.start,
                     count=count, per_page=self.limit)

    def _render(self, form_data=None, form_errors=None, **kwargs):
        self.render(
            "images_manage.html", form_data=form_data, form_errors=form_errors, **kwargs
        )


class ImagesDeletehHandler(JsSiteBaseHandler):
    operation = "删除图片"

    def post(self, *args, **kwargs):
        pass

urls = [
    (r"/admin/images/manage/?", ImagesManageHandler),
    (r"/admin/images/delete/?", ImagesDeletehHandler),
]