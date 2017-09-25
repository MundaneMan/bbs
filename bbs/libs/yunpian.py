#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests

import config_web


SMS_SEND_API_URL = "https://sms.yunpian.com/v2/sms/single_send.json"


def send_verify_sms(mobilephone, code):
    sms_dict = {
        "apikey": config_web.settings["yunpian_apikey"],
        "mobile": mobilephone,
        "text": "【ins酒吧】您的验证码是%s。如非本人操作，请忽略本短信" % code,
        # "callback_url": ""
    }
    r = requests.post(SMS_SEND_API_URL, data=sms_dict)
    r_dict = r.json()
    if r_dict and "code" in r_dict and r_dict["code"] == 0:
        return True
    
    logging.warn("SMS SEND ERROR: %s" % r_dict["msg"])
    return False
