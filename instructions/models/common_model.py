#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Common module
"""

from instructions.models import build_obj_id, filter_obj_id
from config_web import db


# --- photo --- #

def load_photo_by_id(photo_id):
    if not photo_id:
        return None
    return db.app_photos.find_one({"photo_id":photo_id})

def update_photo(photo_id, photo_data):
    db.app_photos.update({"photo_id":photo_id}, {"$set":photo_data})

def insert_photo_info(photo_data, photo_type, member_obj_id):
    """insert photo info"""
    photo_dict = {
        "photo_id":photo_data["id"], "width":photo_data["width"], "height":photo_data["height"],
        "type":photo_type, "member_obj_id":member_obj_id, "status":"new"
    }
    db.app_photos.insert_one(photo_dict)

def list_photos_by_city_obj_id(city_obj_id, start=0, limit=30):
    photos = db.app_photos.find(
        {"city_obj_id":city_obj_id, "status":"normal"}, sort=[("_id", -1)],
        skip=start, limit=limit
    )
    return photos

def format_photo(photo_obj):
    photo_obj = filter_obj_id(photo_obj)
    if photo_obj.has_key("city_obj_id"):
        photo_obj.pop('city_obj_id')
    if photo_obj.has_key("member_obj_id"):
        photo_obj.pop('member_obj_id')
    return photo_obj


# --- code --- #

def load_code_by_code(code, code_type):
    return db.app_codes.find_one(
        {"verify_code":code, "code_type":code_type, "status":"normal"},
        sort=[("_id", -1)]
    )


def update_code_by_obj_id(code_obj_id, code_data):
    db.app_codes.update({"_id":code_obj_id}, {"$set":code_data})


def insert_code(code_data):
    if not code_data.has_key("status"):
        code_data["status"] = "normal"
    db.app_codes.insert_one(code_data)


# --- feedback --- #

def insert_feedback(feedback_text):
    """insert feedback"""
    feedback_obj = {"content": feedback_text}
    db.app_feedbacks.insert_one(feedback_obj)
