# -*- coding: utf-8 -*-
#!/usr/bin/env python

import functools
import tornado.web

import bbs.libs.data as lib_data
import bbs.models.target_model as target_model


def admin_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not (self.current_user and self.current_user.has_key("role") \
                and self.current_user["role"] in lib_data.member_roles):
            # self.send_error(404)
            self.clear_cookie(self.settings["cookie_key_sess"])
            self.redirect("/signin")
            return

        return method(self, *args, **kwargs)
    return wrapper


def has_permission(permission):
    def check_permission(method):
        def wrapper(self, *args, **kwargs):
            if not (self.current_user and self.current_user.has_key("role")):
                raise tornado.web.HTTPError(403)
            if self.current_user["role"] != "admin" and not permission in \
                    lib_data.member_permissions[self.current_user["role"]]:
                raise tornado.web.HTTPError(403)

            return method(self, *args, **kwargs)

        return wrapper
    return check_permission


def api_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise tornado.web.HTTPError(403)

        return method(self, *args, **kwargs)
    return wrapper
