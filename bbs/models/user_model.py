#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from bbs.models import build_obj_id, build_id_time_str
from config_web import db


# --- user --- #

def load_user_by_id(user_id):
    user_obj_id = build_obj_id(user_id)
    return load_user_by_obj_id(user_obj_id)


def load_user_by_obj_id(user_obj_id):
    return db.users.find_one({"_id": user_obj_id, "status": "normal"})


def load_user_by_mobile_phone(mobile_phone, country_code, status="normal"):
    cond = {"mobilephone": mobile_phone, "country_code": country_code}
    if status:
        cond["status"] = status
    return db.users.find_one(cond)


def load_user_by_email(email):
    print email
    return db.users.find_one({"username": email})


def list_user_by_obj_ids(obj_ids):
    r_obj_ids = list(set(obj_ids))
    users = db.users.find({"_id": {"$in": r_obj_ids}})
    return users


def list_users_by_cond(m_cond, sort=None, start=0, limit=30, _is_count=False):
    if _is_count:
        return db.users.count(m_cond)

    return db.users.find(m_cond, sort=sort, skip=start, limit=limit)


def insert_user(user_data):
    if "status" in user_data:
        user_data["status"] = "normal"
    user_data["create_at"] = int(time.time())
    result = db.users.insert_one(user_data)
    return result.inserted_id


def update_user_location(obj_id, loc):
    user_dict = {'visited_at': int(time.time())}
    if loc and len(loc) == 2:
        user_dict['last_loc'] = {'type': 'Point', 'coordinates': [float(loc[0]), float(loc[1])]}
    db.users.update({'_id': obj_id}, {'$set': user_dict})


def update_user_by_obj_id(obj_id, user_data):
    db.users.update({"_id": obj_id}, {"$set": user_data})


def is_field_data_exist(field, data):
    cond = {field: data}
    print cond
    count = db.users.find(cond).count()
    if count > 0:
        return True
    return False


def format_user(user_obj, t_format='%Y-%m-%d %H:%M:%S'):
    if "_id" in user_obj:
        user_obj["user_id"] = str(user_obj["_id"])

    if "create_at" in user_obj:
        user_obj["create_at"] = time.strftime(t_format,
                                              time.localtime(user_obj["create_at"]))

    for key in ("password", 'coordinates', "favorite_shops", "sessions"):
        user_obj.pop(key, None)

    return user_obj

