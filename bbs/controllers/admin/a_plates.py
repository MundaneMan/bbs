#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bbs.libs.handlers import AdminBaseHandler
import bbs.models.plate_model as plate_model
import json


class PlatesManageHandler(AdminBaseHandler):
    operation = u"贴吧版块管理"

    def get(self, *args, **kwargs):
        category_id = self.get_argument("category_id", "")
        root_categories = [plate_model.format_category(c)
                           for c in plate_model.list_categories_by_cond({"status": "normal",
                                                                         "category_parent": "0"})]
        if category_id != "add":
            cur_category = plate_model.load_category_by_id(category_id)
            if cur_category:
                self._get_one_level_sub_categories(cur_category)
            else:
                self.redirect("/admin/article_category?category_id=add")
                return
        else:
            cur_category = None

        self.render("a_m_plates.html", categories=root_categories,
                    json_categories=json.dumps(root_categories),
                    cur_category=cur_category)

    def post(self):
        category_id = self.get_argument("category_id", "")

        if category_id == "" or category_id == "add":
            new_main_category_name = self.get_argument("main_category_name", "")
            # 新分类的内容为空
            if not new_main_category_name:
                self.redirect("/admin/article_category")
                return
            else:
                # 添加新分类
                if "new_sub_categories" in self.request.arguments:
                    new_sub_categories = self.request.arguments["new_sub_categories"]
                else:
                    new_sub_categories = list()
                _id = plate_model.insert_category({"category_name": new_main_category_name,
                                                   "category_parent": "0"})
                if not _id:
                    self._message_page(u"<strong style='color:red'>添加分类出错，文章分类'{}'已存在.</strong>"
                                       .format(new_main_category_name),
                                       category_id='add', t_seconds=2)
                    return
                category_id = str(_id)
                for new_sub_category in new_sub_categories:
                    r = plate_model.insert_category({"category_name": new_sub_category,
                                                     "category_parent": str(_id)})
                    if not r:
                        self._message_page(u"<strong style='color:red'>添加分类出错，文章分类'{}'已存在.</strong>".format(new_sub_category.decode("utf-8")), category_id=category_id, t_seconds=2)
                        return
        else:
            cur_category = plate_model.load_category_by_id(category_id)
            # 修改已有分类
            if cur_category:
                # 删除所有分类
                main_category_name = self.get_argument("main_category_name", "")
                if not main_category_name:
                    plate_model.delete_category_by_id(category_id)
                    sub_categories = plate_model.list_categories_by_cond(
                        {"category_parent": category_id})
                    if len(list(sub_categories)) > 0:
                        for sc in sub_categories:
                            plate_model.delete_category_by_id(str(sc["_id"]))
                else:
                    r1 = plate_model.update_category_name_by_id(category_id, {"category_name": main_category_name})
                    if not r1:
                        self._message_page(u"<strong style='color:red'>修改分类出错，文章分类'{0}'已存在.</strong>"
                                           .format(main_category_name),
                                           category_id=category_id, t_seconds=2)
                        return
                    # 既有修改又有删除和添加的操作
                    new_sub_categories = list()
                    if "new_sub_categories" in self.request.arguments:
                        new_sub_categories = self.request.arguments["new_sub_categories"]

                    modify_sub_categories = list()
                    for arg_key, arg_value in self.request.arguments.items():
                        if str(arg_key).startswith("sub_"):
                            modify_sub_category = dict()
                            modify_sub_category["_id"] = arg_key.split("_")[1]
                            modify_sub_category["category_name"] = str(arg_value[0])
                            modify_sub_category["category_parent"] = category_id
                            modify_sub_categories.append(modify_sub_category)
                    sub_categories = plate_model.list_categories_by_cond(
                        {"category_parent": category_id, "status": "normal"})

                    for sub_category in sub_categories:
                        is_del = True
                        for modify_category in modify_sub_categories:
                            if str(sub_category['_id']) == modify_category['_id']:
                                is_del = False
                        if is_del:
                            plate_model.delete_category_by_id(str(sub_category['_id']))

                    for category_name in new_sub_categories:
                        res = plate_model.insert_category({"category_name": category_name,
                                                           "category_parent": category_id})
                        if not res:
                            self._message_page(u"<strong style='color:red'>添加分类出错，文章分类'{0}'已存在.</strong>"
                                               .format(category_name.decode("utf-8")),
                                               category_id=category_id, t_seconds=2)
                            return

                    for category in modify_sub_categories:
                        _id = category['_id']
                        category.pop('_id')
                        s = plate_model.update_category_name_by_id(_id, category)
                        if not s:
                            self._message_page(u"<strong style='color:red'>修改分类出错，文章分类'{0}'已存在.</strong>"
                                               .format(category["category_name"].decode("utf-8")),
                                               category_id=category_id, t_seconds=2)
                            return
            else:
                self.redirect("/admin/article_category")
                return

        self._message_page(u"文章分类修改已成功保存.", category_id=category_id)

    # 获得一级子分类
    def _get_one_level_sub_categories(self, category):
        sub_categories = [plate_model.format_category(c) for c in plate_model.list_categories_by_cond(
            {"status": "normal", "category_parent": str(category["_id"])})]
        if sub_categories:
            category["sub_categories"] = sub_categories

    def _message_page(self, message, category_id="add",t_seconds=1):
        self.write(u"<center>"+message+".</center><script type='text/javascript'>"
                   "function jumpPage(){window.location.href='/admin/article_category?category_id="+category_id+"';};"
                   "window.setTimeout('jumpPage();',"+str(t_seconds*1000)+");"
                   "</script>")

urls = [
    (r"/admin/plates/manage/?", PlatesManageHandler),
]