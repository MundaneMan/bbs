#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bson
import datetime


def build_obj_id(id):
    try:
        return bson.objectid.ObjectId(id)
    except bson.errors.InvalidId:
        return None


def filter_obj_ids(obj_list):
    return [filter_obj_id(obj) for obj in obj_list]


def filter_obj_id(obj):
    if "_id" in obj:
        obj["id"] = str(obj["_id"])
        obj.pop("_id", None)
    return obj


def build_id_time_str(obj_id):
    china_tz = ChinaTimeZone()
    local_datetime = obj_id.generation_time.replace(tzinfo=china_tz)
    return local_datetime.strftime("%Y-%m-%d %H:%M:%S")


class ChinaTimeZone(datetime.tzinfo):
    def utcoffset(self, date_time):
        return datetime.timedelta(hours=8) + self.dst(date_time)

    def dst(self, date_time):
        return datetime.timedelta(0)
