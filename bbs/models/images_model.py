#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bbs.models import build_obj_id, build_id_time_str
from config_web import db
import time

def load_image_by_id(image_id):
    image_obj_id = build_obj_id(image_id)
    return load_image_by_obj_id(image_obj_id)


def load_image_by_obj_id(image_obj_id):
    return db.images.find_one({"_id": image_obj_id, "status": "normal"})


def list_image_by_obj_ids(obj_ids):
    r_obj_ids = list(set(obj_ids))
    images = db.images.find({"_id": {"$in": r_obj_ids}})
    return images


def list_images_by_cond(m_cond, sort=[('create_at', -1)], start=0, limit=30, _is_count=False):
    if _is_count:
        return db.images.count(m_cond)

    return list(db.images.find(m_cond, sort=sort, skip=start, limit=limit))


def insert_image(image_data):
    if "status" not in image_data:
        image_data["status"] = "normal"
    image_data["created_at"] = int(time.time())
    result = db.images.insert_one(image_data)
    return result.inserted_id


def update_image_by_obj_id(obj_id, image_data):
    db.images.update({"_id": obj_id}, {"$set": image_data})


def is_field_data_exist(field, data):
    cond = {field: data}
    print cond
    count = db.images.find(cond).count()
    if count > 0:
        return True
    return False


def format_image(_obj, t_format='%Y-%m-%d %H:%M:%S'):
    if "create_at" in _obj:
        _obj["create_at"] = time.strftime(t_format, time.localtime(_obj["create_at"]))
    if "_id" in _obj:
        _obj["_id"] = str(_obj["_id"])

    return _obj