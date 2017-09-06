#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from fupin.models import build_obj_id
from config_web import db


# ****************************************************************************************
# 教育数据
# ****************************************************************************************
def load_edu_student_funding_by_id(str_id, status="normal"):
    obj_id = build_obj_id(str_id)
    return db.app_fp_edu_student_fundings.find_one({"_id": obj_id, "status": status})


def list_edu_student_fundings_by_cond(cond, sort=None, start=0, limit=30,
                                      _is_count=False):
    if _is_count:
        return db.app_fp_edu_student_fundings.find(cond).count()

    return db.app_fp_edu_student_fundings.find(cond, sort=sort, skip=start, limit=limit)


def insert_edu_student_funding(data):
    if "status" not in data:
        data["status"] = "normal"
    data['create_at'] = data['update_at'] = int(time.time())
    db.app_fp_edu_student_fundings.insert(data)


# ****************************************************************************************
# 雨露计划
# ****************************************************************************************
def load_rain_prj_by_id(str_id, status="normal"):
    obj_id = build_obj_id(str_id)
    return db.app_fp_rain_prjs.find_one({"_id": obj_id, "status": status})


def load_rain_prj_by_cond(cond, status="normal"):
    cond['status'] = status
    return db.app_fp_rain_prjs.find_one(cond)


def list_rain_prjs_by_cond(cond, sort=None, start=0, limit=30, _is_count=False):
    if _is_count:
        return db.app_fp_rain_prjs.find(cond).count()

    return db.app_fp_rain_prjs.find(cond, sort=sort, skip=start, limit=limit)


def insert_rain_prj(data):
    if "status" not in data:
        data["status"] = "normal"
    data['create_at'] = data['update_at'] = int(time.time())
    db.app_fp_rain_prjs.insert(data)


def update_rain_prj_by_cond(cond, data):
    db.app_fp_rain_prjs.update_one(cond, {"$set": data})


def insert_or_update_rain_prj(data):
    if 'id_number' in data and data['id_number']:
        cond = {'id_number': data['id_number'], 'year': data['year']}
        if 'card_number' in data and data['card_number']:
            cond['card_number'] = data['card_number']
        exist = load_rain_prj_by_cond(cond)
        if exist:
            return update_rain_prj_by_cond(cond, data)

    return insert_rain_prj(data)
