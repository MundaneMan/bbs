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
        print user
        if not user or user["password"] != \
                bcrypt.hashpw(str(password), str(user["password"])):
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


class UserLoginHandler(UserBaseHandler):
    operation = u"用户请求登录页面"

    def get(self):
        self.render('login.html', form_errors=None)

    def post(self):
        form_data = self._build_form_data()
        form_errors = self._validate_require_form_data(form_data)
        if form_errors:
            self._render(form_data, form_errors)
        if not self.do_login(form_data["email"], form_data["password"]):
            form_errors["form"] = "登录邮箱/密码不匹配"
            self._render(form_data, form_errors)
            return

        self.redirect('/')

    def _render(self, form_data=None, form_errors=None):
        self.render(
            "login.html", form_data=form_data, form_errors=form_errors
        )

    def _list_form_keys(self):
        return ["email", "password"]

    def _list_required_form_keys(self):
        return ["email", "password"]


class UserRegisterHandler(UserBaseHandler):
    operation = u"用户注册账号"

    def get(self, *args, **kwargs):
        self.render('register.html')

    def post(self, *args, **kwargs):
        form_data = self._build_form_data()
        form_errs = self._validate_register_form_data(form_data)
        print form_errs
        if form_errs:
            self.data["result"] = "failed"
            self.data["error_msg"] = form_errs
            self.write(self.data)
            self.redirect("/")
            return
        password = form_data["password"]
        hashed_password = bcrypt.hashpw(
            str(form_data["password"]), bcrypt.gensalt()
        )
        form_data["password"] = hashed_password
        form_data.pop("password2")
        form_data["status"] = "un_verify"
        form_data["role"] = "member"
        user_model.insert_user(form_data)
        self.do_login(form_data["email"], password)
        self.redirect("/")

    def _validate_register_form_data(self, form_data):
        form_errs = self._validate_require_form_data(form_data)
        if form_errs:
            return form_errs
        if form_data["password"] != form_data["password2"]:
            form_errs["password"] = u"两次密码不一致"
            self.data["err_msg"] = u"两次密码不一致"
            return form_errs
        if user_model.is_field_data_exist("email", form_data["email"]):
            form_errs["email"] = u"邮箱已经被注册"
            self.data["err_msg"] = u"邮箱已经被注册"
            return form_errs
        if user_model.is_field_data_exist("nick_name", form_data["nick_name"]):
            form_errs["nick_name"] = u"昵称已经存在"
            self.data["err_msg"] = u"昵称已经存在"
            return form_errs

    def _list_required_form_keys(self):
        return ["nick_name", "email", "password", "password2"]

    def _list_form_keys(self):
        return ["nick_name", "email", "password", "password2"]


class UserVerifyJsHandler(JsSiteBaseHandler):
    def post(self, *args, **kwargs):
        type = self.get_argument("type", "")
        if type == "email":
            self._verify_user_email()
        elif type == "nick_name":
            self._verify_user_nick_name()

    def _verify_user_email(self):
        email = self.get_argument("email", "")
        if email:
            if user_model.is_field_data_exist("email", email):
                self.data["result"] = "failed"
                self.data["message"] = u"该邮箱已经注册过"
                self.write(self.data)
                return
            else:
                self.data["result"] = "success"
                self.data["message"] = u"邮箱可用"
                self.write(self.data)
                return
        self.data["result"] = "failed"
        self.data["message"] = u"邮箱不能为空"
        self.write(self.data)
        return

    def _verify_user_nick_name(self):
        nick_name = self.get_argument("nick_name", "")
        if nick_name:
            if user_model.is_field_data_exist("nick_name", nick_name):
                self.data["result"] = "failed"
                self.data["message"] = u"昵称已存在"
                self.write(self.data)
                return
            else:
                self.data["result"] = "success"
                self.data["message"] = u"昵称可用"
                self.write(self.data)
                return
        self.data["result"] = "failed"
        self.data["message"] = u"昵称不能为空"
        self.write(self.data)
        return


class UserLogoutHandler(HomeBaseHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie(self.settings["cookie_key_sess"])
        self.redirect("/")

urls = [
    (r"/user/login/?", UserLoginHandler),
    (r"/user/logout/?", UserLogoutHandler),
    (r"/user/register/?", UserRegisterHandler),
    (r"/js/user/verify/?", UserVerifyJsHandler),
    ]
