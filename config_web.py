#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""config for web app"""

import os
import pymongo


SITE_NAME = "企业说明书管理系统"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# search index path
INDEX_PATH = os.path.join(BASE_DIR, "..", "index_data")


settings_common = {
    "app_base_path": BASE_DIR,
    "site_name": SITE_NAME,
    "static_version": "1.0.1",
    "cookie_key_sess": "fpc1",

    "static_path": os.path.join(BASE_DIR, "assets"),
    "template_path": os.path.join(BASE_DIR, "instructions", "templates"),
    "login_url": "/login",

    # "xsrf_cookies": True,
    "cookie_secret": "11oETkKXQAGaYdkL5gEmGeJkFuYh7EQnp2XdTP1o/Vo=",
    "gzip": True,
}

settings_debug = {
    "debug": True,
    "api_domain": "api-local.instructions.com",
    "admin_domain": "local-instructions.com",
    "static_url": "http://local-instructions.com/",
    "static_path": "/Users/matt/Projects/backup/instructions/static/",
}

settings_production = {
    "api_domain": "api-local.instructions.com",
    "admin_domain": "admin-instructions.com",
    "static_url": "http://s-local.instructions.com:8080/",
    "static_path": "/Users/matt/Projects/backup/instructions/static/",
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
db = client["web"]


# search server
search_url = "http://localhost:8000/SEARCH_RPC"


# icon url
icon_url_debug = "http://s-local.isntructions.com/icons/"
icon_url_production = "http://s.instructions.com/icons/"


