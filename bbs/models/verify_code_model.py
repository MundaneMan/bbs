#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Common module
"""

from config_web import db
import time



# --- verify_code --- #

def load_code_by_code(code, code_type):
    return db.app_codes.find_one(
        {"verify_code": code, "code_type": code_type, "status": "normal"},
        sort=[("_id", -1)]
    )


def update_code_by_obj_id(code_obj_id, code_data):
    db.app_codes.update({"_id": code_obj_id}, {"$set": code_data})


def insert_code(code_data):
    if not code_data.has_key("status"):
        code_data["status"] = "normal"
    code_data["create_at"] = int(time.time())
    db.app_codes.insert_one(code_data)
