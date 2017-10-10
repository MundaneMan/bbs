#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""config for web app"""

import os
import pymongo


SITE_NAME = u"AI头条网"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# search index path
INDEX_PATH = os.path.join(BASE_DIR, "..", "index_data")


settings_common = {
    "app_base_path": BASE_DIR,
    "site_name": SITE_NAME,
    "static_version": "1.0.1",
    "cookie_key_sess": "fpc1",

    "static_path": os.path.join(BASE_DIR, "assets"),
    "template_path": os.path.join(BASE_DIR, "bbs", "templates"),
    "login_url": "/user/login",

    # "xsrf_cookies": True,
    "cookie_secret": "11oETkKXQAGaYdkL5gEmGeJkFuYh7EQnp2XdTP1o/Vo=",
    "gzip": True,
    "redis": {"db": 1, "host": "localhost", "port": 6379}

}

settings_debug = {
    "debug": True,
    "api_domain": "www-local.bbs.com",
    "admin_domain": "www-local.bbs.com",
    "static_url": "http://www-local.bbs.com/static/",
    "static_path": "/Users/data/website/bbs/static/",
}

settings_production = {
    "api_domain": "www-local.bbs.com",
    "admin_domain": "www-local.bbs.com",
    "static_url": "http://www-local.bbs.com/static/",
    "static_path": "/Users/data/website/bbs/static/",
}

settings_testing = {

}


RUNNING_STATUS = os.getenv("RUNNING_STATUS", "debug")
if RUNNING_STATUS == "debug":
    settings_common.update(settings_debug)
elif RUNNING_STATUS == "testing":
    settings_common.update(settings_testing)
elif RUNNING_STATUS == "production":
    settings_common.update(settings_production)
settings = settings_common


# db
mongo_host = os.getenv("MONGO_HOST", "mongodb")
client = pymongo.MongoClient(mongo_host, 27017)
db = client["bbs"]


# search server
search_url = "http://localhost:8000/SEARCH_RPC"


# icon url
icon_url_debug = "http://s-local.isntructions.com/icons/"
icon_url_production = "http://s.bbs.com/icons/"


