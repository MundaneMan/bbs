#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bbs.libs.handlers import HomeBaseHandler, JsSiteBaseHandler
import bbs.models.article_model as article_model
import bbs.models.image_model as images_model
import bbs.libs.photo as photo_tools


class ArticlePublishHandler(HomeBaseHandler):
    def get(self, *args, **kwargs):
        self._render()

    def post(self, *args, **kwargs):
        form_data = self._build_form_data()
        print form_data
        form_errors = self._validate_require_form_data(form_data)
        if form_errors:
            self._render(form_data, form_errors)
            return
        if "main_pic" in self.request.files:
            main_pic = self.request.files["main_pic"][0]
            main_pic_info_dict = photo_tools.save_upload_photo(main_pic["body"], self.settings["static_path"])
            form_data["main_pic"] = main_pic_info_dict["id"]
        article_id = article_model.insert_article(form_data)
        self.redirect("/article/view/{}/".format(str(article_id)))

    def _render(self, form_data=None, form_errors=None):
        self.render(
            "/article/edit.html", form_data=form_data, form_errors=form_errors
        )

    def _list_form_keys(self):
        return ["title", "content", "main_pic"]

    def _list_required_form_keys(self):
        return ["title", "content"]


class ArticleViewHandler(HomeBaseHandler):
    operation = u"查看一篇文章内容"

    def get(self, article_id):
        # print article_id
        article = article_model.load_article_by_id(article_id)
        if article:
            if "main_pic" in article and article["main_pic"]:
                article["main_pic"] = self.build_photo_url(article["main_pic"], "title")
            self.render("/article/view.html", article=article)
        else:
            self.send_error(404)


class ArticleUploadImgHandler(JsSiteBaseHandler):
    operation = u"保存文章中的图片"

    def post(self):
        if self.request.files and "upload" not in self.request.files.keys():
            self.data["success"] = False
            self.data["msg"] = u"没有找到文件 !"
            self.write(self.data)
            return
        callback = self.get_argument("CKEditorFuncNum")
        photo = self.request.files["upload"][0]
        photo_file_name = photo["filename"]
        if not (photo_file_name.endswith(".jpg") or photo_file_name.endswith(".png")):
            self.data["result"] = "failed"
            self.data["message"] = "Photo format error ,must be jpg or png images !"
            self.write(self.data)
            return
        photo_info_dict = photo_tools.save_upload_photo(photo["body"], self.settings["static_path"])
        file_name = self.build_photo_url(photo_info_dict["id"])

        res_txt = "<script type='text/javascript'> window.parent.CKEDITOR.tools.callFunction("\
                  + callback + ",'" + file_name + "'," + ");</script>"
        print res_txt
        self.write(res_txt)


urls = [
    (r"/article/edit/?", ArticlePublishHandler),
    (r"/article/view/(\w+)/?", ArticleViewHandler),
    (r"/article/upload_img/?", ArticleUploadImgHandler)
]