#!/usr/bin/env python
# -*- coding: utf-8 -*-


member_roles = ("admin", "member")
member_roles_names = {"admin": u"管理员", "member": u"用户"}

member_permissions = {
    "admin": ("", ),
    "member": {"", }
}

ORDER_STATUS_DICT = {
    'new': '待支付',

    'wait_pay': '待支付',
    'paid': '已付款',
    'servicing': '服务中',
    'finished': '已完成',
}

ORDER_PAY_METHODS = [
    {'id': 'wxpay', 'name': '微信支付', 'pingpp_id': 'wx'},
    {'id': 'alipay', 'name': '支付宝', 'pingpp_id': 'alipay'},
]