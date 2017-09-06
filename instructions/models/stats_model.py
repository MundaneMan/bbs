#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from instructions.models import build_obj_id
from config_web import db


def load_stats_by_id(stats_id):
    stats_obj_id = build_obj_id(stats_id)
    return load_stats_by_obj_id(stats_obj_id)


def load_stats_by_obj_id(stats_obj_id, status="normal"):
    if not stats_obj_id:
        return None
    return db.app_fp_statss.find_one({"_id": stats_obj_id, "status": status})


def load_latest_stats():
    cond = {"status": "normal"}
    sort = [("create_at", -1)]
    stats_cursor = db.app_fp_stats.find(cond, sort=sort, limit=1)
    if stats_cursor.count() > 0:
        return stats_cursor[0]


def insert_stats(stats_obj):
    if "status" not in stats_obj:
        stats_obj['status'] = "normal"
    stats_obj['create_at'] = int(time.time())
    db.app_fp_stats.insert(stats_obj)




