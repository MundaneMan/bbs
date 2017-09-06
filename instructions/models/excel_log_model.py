#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from instructions.models import build_obj_id
from config_web import db


def load_excel_log_by_id(excel_log_id):
    excel_log_obj_id = build_obj_id(excel_log_id)
    return load_excel_log_by_obj_id(excel_log_obj_id)


def load_excel_log_by_obj_id(excel_log_obj_id, status="normal"):
    if not excel_log_obj_id:
        return None
    return db.app_fp_excel_log.find_one({"_id": excel_log_obj_id, "status": status})


def list_excel_log_by_cond(cond, sort=None, start=0, limit=30, _is_count=False):
    if _is_count:
        return db.app_fp_excel_log.find(cond).count()

    fp_excel_log_cursor = db.app_fp_excel_log.find(
        cond, sort=sort, skip=start, limit=limit
    )
    return fp_excel_log_cursor


def insert_excel_log(excel_log_data):
    excel_log_data["create_at"] = int(time.time())
    return db.app_fp_excel_log.insert_one(excel_log_data)


def update_excel_log_error_by_obj_id(excel_log_obj_id, error_msg):
    db.app_fp_excel_log.update_one({"_id": excel_log_obj_id},
                                   {"$set": {"error_msg": error_msg}})


def format_excel_log(excel_log_data):
    excel_log_data["create_at"] = \
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(excel_log_data["create_at"]))

    excel_log_data["data_type"] = {
        "poverty_target": u"贫困户",
        "education": u"教育",
        "health": u"卫计",
        "housing": u"住建",
        "finance": u"财政",
        "medical": u"医疗",
    }.get(excel_log_data["data_type"], u"其他")

    return excel_log_data
