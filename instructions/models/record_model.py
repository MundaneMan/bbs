#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from fupin.models import build_obj_id
from config_web import db
import pymongo


def load_record_by_id(record_id):
    record_obj_id = build_obj_id(record_id)
    return load_record_by_obj_id(record_obj_id)


def load_record_by_obj_id(record_obj_id, status="normal"):
    if not record_obj_id:
        return None
    return db.app_fp_record.find_one({"_id": record_obj_id, "status": status})


def list_record_by_cond(cond, sort=None, start=0, limit=30, _is_count=False):
    if _is_count:
        return db.app_fp_record.find(cond).count()

    fp_record_cursor = db.app_fp_record.find(
        cond, sort=sort, skip=start, limit=limit
    )
    return fp_record_cursor


def insert_record(record_data):
    record_data["status"] = "normal"
    record_data["create_at"] = int(time.time())
    db.app_fp_record.insert_one(record_data)


def create_gps_index():
    index_dict = db.app_fp_record.index_information()
    if not "gps_data_2dsphere" in index_dict.keys():
        db.app_fp_record.create_index([("gps_data", pymongo.GEOSPHERE)])


def find_near(cond, distance=5000, start=0, limit=30, _is_count=False):
    cond['gps_data']['$near']['$maxDistance'] = distance
    if _is_count:
        return db.app_fp_record.find(cond).count()
    fp_record_cursor = db.app_fp_record.find(cond, skip=start, limit=limit)
    return fp_record_cursor


def format_record(record_data):

    return record_data
