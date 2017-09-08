#!/usr/bin/env python
# -*- coding: utf-8 -*-

from instructions.libs.handlers import HomeBaseHandler, JsSiteBaseHandler
import instructions.models.user_model as user_model
import bcrypt
import random
import time
import string

class UserBaseHandler(HomeBaseHandler):
    def do_login(self, email, password):
        """do login stuff"""
        user = user_model.load_user_by_email(email)
        if not user or user["hashed_password"] != \
                bcrypt.hashpw(str(password), str(user["hashed_password"])):
            return False

        # insert session
        sessions = user["sessions"] if "sessions" in user \
                                       and isinstance(user["sessions"], list) else list()
        if len(sessions) > 4:
            sessions = sessions[-4:]

        sess_id = ''.join(
            random.choice(string.lowercase + string.digits) for i in range(10)
        )
        sessions.append({"id": sess_id, "time": int(time.time())})

        user_model.update_user_by_obj_id(
            user["_id"], {"sessions": sessions}
        )

        # set cookie
        cookie_val = ":".join([str(user["_id"]), sess_id])
        self.set_cookie(self.settings["cookie_key_sess"], cookie_val)

        return True


class UserLoginHandler(HomeBaseHandler):
    def get(self):
        self.render('login.html')


class UserRegisterHandler(HomeBaseHandler):
    def get(self, *args, **kwargs):
        self.render('register.html')


class UserRegisterJsHandler(JsSiteBaseHandler):
    def post(self, *args, **kwargs):
        form_data = self._build_form_data()
        form_errs = self._validate_register_from_data(form_data)
        if form_errs:
            self.data["result"] = "failed"
            self.data["error"] = form_errs
            self.write(self.data)
            return
        hashed_password = bcrypt.hashpw(
            str(form_data["password"]), bcrypt.gensalt()
        )
        form_data["password"] = hashed_password
        form_data.pop("password2")
        user_model.insert_user(form_data)
        self.data["result"] = "success"
        self.data["message"] = "register account success"

    def _validate_register_from_data(self, form_data):
        form_errs = self._validate_require_form_data()
        if form_errs:
            return form_errs
        if form_data["password"] != form_data["password2"]:
            form_errs["password"] = u"两次密码不一致"
            return form_errs
        if user_model.is_field_data_exist("email", form_data["email"]):
            form_errs["email"] = u"邮箱已经被注册"
            return form_errs
        if user_model.is_field_data_exist("nick_name", form_data["nick_name"]):
            form_data["nick_name"] = u"昵称已经存在"
            return form_errs

    def _list_required_form_keys(self):
        return ["username", "email", "password", "password2"]


urls = [
    (r"/user/login/?", UserLoginHandler),
    (r"/user/register/?", UserRegisterJsHandler),
    ]
