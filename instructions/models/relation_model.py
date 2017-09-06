#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fupin.models import build_obj_id
from config_web import db


def add_or_remove_relation(member_obj_id, target_member_obj_id, r_type="follow"):
    relation_data = {
        "member_obj_id": member_obj_id, "target_member_obj_id": target_member_obj_id,
        "r_type": r_type, "status": "normal"
    }
    relation_obj = db.app_relations.find_one(relation_data)
    if not relation_obj:
        db.app_relations.insert_one(relation_data)
    else:
        db.app_relations.update({"_id": relation_obj["_id"]}, {"$set":{"status":"deleted"}})


def list_relations_by_cond(cond, is_count=False):
    if is_count:
        return db.app_relations.count(cond)
    return db.app_relations.find(cond)


def list_follows_by_member_obj_id(member_obj_id):
    follows_cond = {
        {"$or": [{"member_obj_id": member_obj_id},
                 {"target_member_obj_id": member_obj_id}], "status": "normal"}
    }
    return list_relations_by_cond(follows_cond)


def list_followers_by_member_obj_id(member_obj_id, is_count=False):
    cond = {"target_member_obj_id": member_obj_id, "r_type": "follow", "status": "normal"}
    return list_relations_by_cond(cond, is_count=is_count)


def list_following_by_member_obj_id(member_obj_id, is_count=False):
    cond = {"member_obj_id": member_obj_id, "r_type": "follow", "status": "normal"}
    return list_relations_by_cond(cond, is_count=is_count)


def is_following(member_obj_id, target_member_obj_id):
    follow_cond = {
        "member_obj_id": member_obj_id, "target_member_obj_id": target_member_obj_id,
        "r_type": "follow", "status": 'normal'
    }
    if db.app_relations.find_one(follow_cond):
        return True
    return False



def format_relation(relation_id):
    pass
