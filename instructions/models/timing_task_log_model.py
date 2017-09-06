#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from fupin.models import build_obj_id, build_id_time_str
from config_web import db


def load_timing_task_log_by_id(str_id, status="normal"):
    obj_id = build_obj_id(str_id)
    return db.app_fp_stats.find_one({"_id": obj_id, "status": status})


def list_timing_task_logs_by_cond(cond, sort=None, start=0, limit=30, _is_count=False):
    if _is_count:
        return db.app_fp_stats.find(cond).count()

    timing_log_cursor = db.app_fp_stats.find(
        cond, sort=sort, skip=start, limit=limit
    )
    return timing_log_cursor


def insert_timing_task_log(timing_log_data):
    timing_log_data["create_at"] = int(time.time())
    timing_log_data["status"] = "normal"
    return db.app_fp_stats.insert_one(timing_log_data)


def format_timing_log(timing_log):
    if "_id" in timing_log:
        timing_log["member_id"] = str(timing_log["_id"])

    if "create_at" in timing_log:
        timing_log["create_at"] = \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timing_log["create_at"]))

    return timing_log
