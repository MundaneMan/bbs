#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from instructions.models import build_obj_id
from config_web import db


def load_operation_log_by_id(str_id, status="normal"):
    obj_id = build_obj_id(str_id)
    return db.app_fp_operation_logs.find_one({"_id": obj_id, "status": status})


def list_operation_log_by_cond(cond, sort=None, start=0, limit=30, _is_count=False):
    if _is_count:
        return db.app_fp_operation_logs.find(cond).count()

    operation_log_cursor = db.app_fp_operation_logs.find(
        cond, sort=sort, skip=start, limit=limit
    )
    return operation_log_cursor


def insert_operation_log(operation_log_data):
    operation_log_data["create_at"] = int(time.time())
    operation_log_data["status"] = "normal"
    return db.app_fp_operation_logs.insert_one(operation_log_data)
