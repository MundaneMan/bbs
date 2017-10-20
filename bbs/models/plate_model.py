#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from bbs.models import build_obj_id, build_id_time_str
from config_web import db


# 贴吧版块管理
def load_category_by_id(category_id):
    category_obj_id = build_obj_id(category_id)
    return load_category_by_obj_id(category_obj_id)


def load_category_by_obj_id(category_obj_id, status="normal"):
    if not category_obj_id:
        return None
    return db.plates.find_one({"_id": category_obj_id, "status": status})


def load_category_by_cond(cond):
    cond['status'] = 'normal'
    return db.plates.find_one(cond)


def list_categories_by_cond(cond, sort=None, start=0, limit=None, _is_count=False):
    if ('status' not in cond) and isinstance(cond, dict):
        cond['status'] = 'normal'
    if _is_count:
        return db.plates.find(cond).count()
    if limit is None:
        fp_category_cursor = db.plates.find(cond)
    else:
        fp_category_cursor = db.plates.find(
            cond, sort=sort, skip=start, limit=limit
        )
    return list(fp_category_cursor)


def insert_category(category_data):
    # 判断是否已经存在相同分类名
    c = load_category_by_cond({"status": "normal", "category_name": category_data["category_name"]})
    if c:
        return False
    if "status" not in category_data:
        category_data["status"] = "normal"
    category_data['create_at'] = int(time.time())
    result = db.plates.insert_one(category_data)
    return result.inserted_id

def update_category_by_id(category_id, category_data):
    category_obj_id = build_obj_id(category_id)
    conds = {"_id": category_obj_id}
    category_data['update_at'] = int(time.time())
    db.plates.update(conds, {"$set": category_data})


def update_category_name_by_id(category_id, category_data):
    # 判断是否已经存在相同分类名
    c = load_category_by_cond({"status": "normal", "category_name": category_data["category_name"]})
    if c and (str(c['_id']) != category_id):
        return False
    category_obj_id = build_obj_id(category_id)
    conds = {"_id": category_obj_id}
    category_data['update_at'] = int(time.time())
    db.plates.update(conds, {"$set": category_data})
    return True


def save_category(category):
    category['_id'] = build_obj_id(category['_id'])
    category['update_at'] = int(time.time())
    db.plates.save(category)


def delete_category_by_id(category_id):
    category_data = {"status": "deleted"}
    category_obj_id = build_obj_id(category_id)
    conds = {"_id": category_obj_id}
    category_data['update_at'] = int(time.time())
    db.plates.update(conds, {"$set": category_data})


def distinct_category_field(field, cond=None, _is_count=False):
    if not cond:
        cond = dict()
    if "status" not in cond:
        cond["status"] = "normal"
    if field:
        if _is_count:
            return len(db.plates.distinct(field, cond))
        return db.plates.distinct(field, cond)
    return None


def list_sub_categories_by_name(category_name, count):
    cond = dict()
    cond["category_name"] = category_name
    cond['status'] = 'normal'
    category = db.plates.find_one(cond)
    if category:
        return list_categories_by_cond({"status": "normal", "category_parent": str(category["_id"])}, limit=count)


def list_all_sub_categories_by_name():
    pass


def format_category(_obj):
    if "create_at" in _obj:
        _obj["create_at"] = time.strftime('%Y-%m-%d %H:%M:%S',
                                          time.localtime(_obj["create_at"]))
    if "_id" in _obj:
        _obj["_id"] = str(_obj["_id"])
    return _obj
