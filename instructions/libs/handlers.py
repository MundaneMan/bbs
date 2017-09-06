#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""base handlers"""

import datetime
import traceback

import tornado.web
import tornado.netutil

import config_web
import fupin.libs.data as lib_data
import fupin.libs.template as lib_template

import fupin.helpers.member_helper as member_helper
import fupin.models.member_model as member_model
import fupin.models.target_model as target_model
import fupin.models.operation_log_model as operation_log_model
import fupin.libs.data as lib_data
import fupin.libs.data_lib as data_lib


class BaseHandler(tornado.web.RequestHandler):
    operation = u"未标记操作"

    def initialize(self):
        self.prepare_remote_ip()

    def set_default_handlers(self):
        self.set_header("Server", "ghs/1.0.1")

    @property
    def start(self):
        start = self.get_argument("start", "0")
        start = int(start) if start.isdigit() else 0
        if start < 0:
            start = 0
        return start

    def prepare_remote_ip(self):
        raw_ip = self.request.headers.get("X-Forwarded-For", self.request.remote_ip)
        raw_ip = raw_ip.split(',')[-1].strip()
        raw_ip = self.request.headers.get("X-Real-Ip", raw_ip)
        if tornado.netutil.is_valid_ip(raw_ip):
            self.remote_ip = raw_ip
        # AWS uses X-Forwarded-Proto
        proto_header = self.request.headers.get(
            "X-Scheme", self.request.headers.get("X-Forwarded-Proto",
                                                 self.request.protocol))
        if proto_header in ("http", "https"):
            self.request.protocol = proto_header

    def get_template_namespace(self):
        namespace = super(BaseHandler, self).get_template_namespace()
        namespace["set_checkbox_value"] = lib_template.set_checkbox_value
        namespace["build_checkbox"] = lib_template.build_checkbox
        namespace["build_radiobox"] = lib_template.build_radiobox
        namespace["build_form_text"] = lib_template.build_form_text
        namespace["build_form_select"] = lib_template.build_form_select
        return namespace

    def _list_form_keys(self):
        raise NotImplementedError

    def _list_required_form_keys(self):
        return list()

    def _validate_form_data(self, form_data):
        form_errors = dict()
        for key in self._list_form_keys():
            if key in self._list_required_form_keys() and not form_data[key]:
                form_errors[key] = "不能为空"

        return form_errors

    def build_photo_url(self, photo_id, pic_type="photo"):
        if photo_id:
            return "".join(
                [self.settings["static_url"], "photos", "/", pic_type, "/", photo_id, ".jpg"]
            )
        else:
            return "".join(["/images/", "pic_none_", pic_type, ".png"])

    def build_icon_url(self, icon_id, pic_type="icon"):
        return member_helper.build_avatar_url(icon_id, pic_type=pic_type)

    @property
    def base_handler_type(self):
        return "base"

    @property
    def unlog_operations(self):
        return ("signup", )

    def prepare(self):
        self._operation_log_init()

    def on_finish(self):
        self._operation_log_finish()

    def _operation_log_init(self):
        self.operation_data = {
            "operate_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def _operation_log_finish(self):
        member = self.current_user
        request = self.request

        # 没登录, 登录不成功的操作不记录
        if self.current_user is None:
            # 登录操作, POST后302认为登录成功
            if request.uri == "/signin" and request.method == "POST" and \
                    self.get_status() == 302:
                email = self.get_argument("email", None)
                member = member_model.load_member_by_email(email)
            else:
                return

        # 不记录日志的操作, 操作名出现在路由中则不记录
        for operation in self.unlog_operations:
            if operation in request.uri:
                return

        # 本次操作结果(fail/失败, success/成功, unknow/未知, miss/未知路由类)
        # 状态码4xx 5xx 认为是失败
        result = "fail"
        if (self.get_status() // 100) < 4:
            # ajax 请求通过判断 self.data 中的 result 或 err_code 判断
            if self.base_handler_type == "js_site_base":
                data = self.data
                # err_code == 0 或 result == "success" 认为操作成功
                if "result" in data:
                    if data["result"] in ("success", ):
                        result = "success"
                elif "err_code" in data:
                    if data["err_code"] in (0, ):
                        result = "success"
                else:
                    result = "unknow"

            # api 请求通过判断 self.data 中的 result 判断
            elif self.base_handler_type == "api_base":
                data = self.data
                # result == "success" 认为操作成功
                if "result" in data:
                    if data["result"] in ("success", ):
                        result = "success"
                else:
                    result = "unknow"

            # site_base 请求
            elif self.base_handler_type == "site_base":
                result = "success"

            # 未知路由类
            else:
                result = "miss"

        # 记录文件名
        # 格式: {"key": "a.jpg; b.jpg", "key": "c.jpg"}, 同一键下含多个值的以"; "(分号加空格)间隔
        files_dict = dict()
        for file_key in request.files:
            tmp = "; ".join([f["filename"] for f in request.files[file_key]])
            files_dict[file_key] = tmp

        # 记录表单参数
        # 格式: {"key": "a; b", "key": "c"}, 同一键下含多个值的以"; "(分号加空格)间隔
        args_dict = dict()
        for arg_key in request.arguments:
            tmp = "; ".join([v for v in request.arguments[arg_key]])
            args_dict[arg_key] = tmp

        # 其他(请求头, self.data, 异常等)
        data = self.data if "data" in self.__dict__ else {}
        other = {
            "request_headers": dict(self.request.headers),
            "data": data,
            "exception": traceback.format_exc()
        }

        # 获取操作名
        operation = self.operation

        self.operation_data["result"] = result
        self.operation_data["member_id"] = str(member["_id"])
        self.operation_data["member_name"] = member["nickname"]
        self.operation_data["handler_type"] = self.base_handler_type
        self.operation_data["method"] = request.method
        self.operation_data["request_files"] = files_dict
        self.operation_data["request_arguments"] = args_dict
        self.operation_data["request_time"] = "%.2fms" % (1000.0 * request.request_time())
        self.operation_data["status_code"] = str(self.get_status())
        self.operation_data["route"] = request.uri.split("?")[0]
        self.operation_data["ip"] = self.remote_ip
        self.operation_data["operation"] = operation
        self.operation_data["other"] = other

        operation_log_model.insert_operation_log(self.operation_data)


class SiteBaseHandler(BaseHandler):
    @property
    def base_handler_type(self):
        return "site_base"

    @property
    def site_name(self):
        return self.settings["site_name"]

    @property
    def next_url(self):
        next_url = self.get_argument("next", None)
        return next_url or "/"

    def _build_form_data(self, encode_str=False):
        form_data = dict()
        for key in self._list_form_keys():
            form_data[key] = self.get_argument("f_"+key, "")

        if encode_str:
            for k, v in form_data.items():
                if v and type(v) is unicode:
                    form_data[k] = v.encode("utf-8")

        return form_data

    def get_current_user(self):
        cookie_data = self.get_cookie(self.settings["cookie_key_sess"])
        if not cookie_data:
            return None

        try:
            member_id, session_id = cookie_data.split(":")
        except:
            return None

        member = member_model.load_member_by_id(member_id)
        if not member.has_key("sessions") or \
                not isinstance(member["sessions"], list):
            return None

        for session in member["sessions"]:
            if session["id"] == session_id:
                return member

        self.clear_cookie(self.settings["cookie_key_sess"])
        return None

    def has_permission(self, permission):
        if not (self.current_user and 'role' in self.current_user):
            return False
        return self.current_user["role"] == "admin" or permission in \
            lib_data.member_permissions[self.current_user["role"]]


class JsSiteBaseHandler(SiteBaseHandler):
    @property
    def base_handler_type(self):
        return "js_site_base"

    def initialize(self):
        super(SiteBaseHandler, self).initialize()
        self.data = {"err_code": 1, "err_msg": "unknow_error", "result": "fail"}


# api base handler
class ApiBaseHandler(BaseHandler):
    @property
    def base_handler_type(self):
        return "api_base"

    def initialize(self):
        super(ApiBaseHandler, self).initialize()
        self.data = {
            "result": "failure", "message": "unknow_error"
        }

    def _build_form_data(self):
        form_data = dict()
        for key in self._list_form_keys():
            form_data[key] = self.get_argument(key, "")

        return form_data

    def get_current_user(self):
        auth_token = self.request.headers.get("Authorization")
        if not auth_token:
            return None
        token_keys = auth_token.split(":")
        if not len(token_keys) == 2:
            return None
        member_id = token_keys[0]
        session_id = token_keys[1]

        member = member_model.load_member_by_id(member_id)
        if not member or not "sessions" in member or \
                not isinstance(member["sessions"], list):
            return None

        for session in member["sessions"]:
            if session["id"] == session_id:
                return member


