#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime

import fupin.libs.data as lib_data

from fupin.models import build_obj_id, build_id_time_str
from config_web import db


# --- member --- #

def load_member_by_id(member_id):
    member_obj_id = build_obj_id(member_id)
    return load_member_by_obj_id(member_obj_id)


def load_member_by_obj_id(member_obj_id):
    return db.app_members.find_one({"_id": member_obj_id, "status": "normal"})


def load_member_by_mobilephone(mobilephone, country_code, status="normal"):
    cond = {"mobilephone": mobilephone, "country_code": country_code}
    if status:
        cond["status"] = status
    return db.app_members.find_one(cond)


def load_member_by_email(email):
    return db.app_members.find_one({"email": email, "status": "normal"})


def list_member_by_obj_ids(obj_ids):
    r_obj_ids = list(set(obj_ids))
    members = db.app_members.find({"_id": {"$in": r_obj_ids}})
    return members


def list_members_by_cond(m_cond, sort=None, start=0, limit=30, is_count=False):
    if is_count:
        return db.app_members.count(m_cond)

    return db.app_members.find(m_cond, sort=sort, skip=start, limit=limit)


def insert_member(member_data):
    if "status" in member_data:
        member_data["status"] = "normal"
    result = db.app_members.insert_one(member_data)
    return result.inserted_id


def update_member_location(obj_id, loc):
    member_dict = {'visited_at': int(time.time())}
    if loc and len(loc) == 2:
        member_dict['last_loc'] = {'type': 'Point', 'coordinates': [float(loc[0]), float(loc[1])]}
    db.app_members.update({'_id': obj_id}, {'$set': member_dict})


def update_member_by_obj_id(obj_id, member_data):
    db.app_members.update({"_id": obj_id}, {"$set": member_data})


def format_member(member_obj, ftype=""):
    if "_id" in member_obj:
        member_obj["member_id"] = str(member_obj["_id"])

    if ftype == "admin_normal":
        member_obj["created_at"] = build_id_time_str(member_obj["_id"])

    for key in ("_id", "hashed_password", 'coordinates', "favorite_shops", "sessions"):
        member_obj.pop(key, None)

    return member_obj


# --- favorites -- #

def is_shop_favorited(member_obj_id, shop_obj_id):
    member = load_member_by_obj_id(member_obj_id)
    if member and "favorite_shops" in member and \
            shop_obj_id in member["favorite_shops"]:
        return True
    return False


def do_favorite_shop(member_obj_id, shop_obj_id, status):
    is_faved = is_shop_favorited(member_obj_id, shop_obj_id)

    if status == "add" and not is_faved:
        db.app_members.update_one({"_id": member_obj_id},
                                  {"$addToSet": {"favorite_shops": shop_obj_id}})
    if status == "remove" and is_faved:
        db.app_members.update_one({"_id": member_obj_id},
                                  {"$pull": {"favorite_shops": shop_obj_id}})


# --- calc --- #

def calc_age(birthday):
    bdate = datetime.datetime.strptime(birthday, '%Y-%m-%d')
    today = datetime.datetime.today()
    return today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))

# --- account --- #


# --- report --- #

def insert_member_report(report_data):
    if not 'status' in report_data:
        report_data['status'] = 'normal'
    if not 'report_status' in report_data:
        report_data['report_status'] = 'new'
    if not 'report_type' in report_data:
        report_data['report_type'] = 'member'

    db.app_reports.insert(report_data)
