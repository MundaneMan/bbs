#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bbs.libs.handlers import AdminBaseHandler, JsSiteBaseHandler
import bbs.models.user_model as user_model


class UsersManageHandler(AdminBaseHandler):
    operation = "用户后台管理页面"

    def get(self):
        base_url = u"/admin/user?"
        count = user_model.list_users_by_cond({"status": "normal"}, _is_count=True)

        users = [user_model.format_user(a) for a in
                 user_model.list_users_by_cond({"status": "normal"}, start=self.start, limit=self.limit)]
        self._render(users=users, base_url=base_url, start=self.start,
                     count=count, per_page=self.limit)

    def _render(self, form_data=None, form_errors=None, **kwargs):
        self.render(
            "a_users.html", form_data=form_data, form_errors=form_errors, **kwargs
        )


class UsersDeleteHandler(JsSiteBaseHandler):
    operation = "删除用户"

    def post(self, *args, **kwargs):
        pass

urls = [
    (r"/admin/users/?", UsersManageHandler),
    (r"/admin/users/delete/?", UsersDeleteHandler),
]