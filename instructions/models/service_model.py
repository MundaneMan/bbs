#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Skill Model Class"""

__author__ = 'matt'

import re

import fupin.libs.geo as lib_geo
import fupin.libs.data as lib_data
import fupin.models.member_model as member_model

from fupin.models import build_obj_id
from config_web import db


SHOP_TYPES = ("bars", "massages", "saunas", "others")


def load_service_by_id(service_id):
    service_obj_id = build_obj_id(service_id)
    if not service_obj_id:
        return None
    return load_service_by_obj_id(service_obj_id)


def load_service_by_obj_id(service_obj_id):
    return db.app_services.find_one(
        {"_id": service_obj_id, "status":"normal"}
    )


def list_services_by_conds(conds, loc=None, field_type="list_normal",
                           sort=None, start=0, limit=30, is_count=False):
    if 'member_id' in conds:
        conds['member_obj_id'] = build_obj_id(conds['member_id'])
        conds.pop('member_id')
    if 'is_same_member' in conds:
        # TODO: here
        conds.pop('is_same_member')
    if is_count:
        return db.app_services.count(conds)

    sort_conds = None
    if sort == 'location' and loc:
        conds['loc'] = {
            "$nearSphere": {"$geometry": {
                "type": "Point", "coordinates": [loc[0], loc[1]]}},
        }
    elif sort == 'ratings':
        sort_conds = [('avg_score', -1)]

    service_cursor = db.app_services.find(conds, sort=sort_conds, skip=start, limit=limit)
    service_list = [s for s in service_cursor]

    if field_type == 'list_home':
        # for home vc
        member_obj_ids = [s['member_obj_id'] for s in service_list]
        members = member_model.list_member_by_obj_ids(member_obj_ids)
        members_dict = {m['_id']: m for m in members}

        for service in service_list:
            if not 'member_obj_id' in service:
                continue
            member = members_dict[service['member_obj_id']]

            service['member_id'] = str(member['_id'])
            # print service['member_id']
            service['member_nickname'] = member['nickname']
            service['member_avatar_id'] = member['pic_id'] if 'pic_id' in member else ''
            service['member_gender'] = member['gender'] if 'gender' in member else 'F'
            service['member_age'] = member_model.calc_age(member['birthday'])

            if not loc or not 'last_loc' in member:
                continue
            coord = member['last_loc']['coordinates']
            service['distance'] = lib_geo.calc_distance(
                float(loc[0]), float(loc[1]), coord[0], coord[1]
            )

    if not sort or sort == 'default':
        max_distance = min_distance = -1
        max_v_count = -1
        for service_obj in service_list:
            # print shop_obj["distance"]
            if "distance" in service_obj and \
                    (float(service_obj["distance"]) > max_distance or max_distance == -1):
                max_distance = float(service_obj["distance"])

    return service_list


def insert_service(service_data):
    if not service_data.has_key("status"):
        service_data["status"] = "normal"
    return db.app_services.insert(service_data)

def update_service(service_obj_id, service_data):
    db.app_services.update({"_id":service_obj_id}, {"$set":service_data})

def update_shop_raw(shop_obj_id, shop_data_raw):
    db.app_shops.update({"_id":shop_obj_id}, shop_data_raw)


def format_service(service_obj, loc=None, field_type="detail_normal"):
    if '_id' in service_obj:
        service_obj["id"] = str(service_obj["_id"])
        service_obj.pop("_id")
    if 'member_obj_id' in service_obj:
        service_obj['member_id'] = str(service_obj['member_obj_id'])
        service_obj.pop('member_obj_id')
    if 'city_obj_id' in service_obj:
        service_obj["city_id"] = str(service_obj["city_obj_id"])
        service_obj.pop("city_obj_id")
    if 'skill_type_name' not in service_obj:
        service_obj['skill_type_name'] = _get_skill_type_name_by_id(service_obj['skill_type_id'])

    return service_obj

def _get_skill_type_name_by_id(skill_type_id):
    for skill_type in lib_data.SKILL_TYPES:
        for skill in skill_type['skills']:
            if skill['id'] == skill_type_id:
                return skill['name']


def _calc_service_distances(service_list, loc=None):
    member_obj_ids = [s['member_obj_id'] for s in service_list]
    members = member_model.list_member_by_obj_ids(member_obj_ids)

    members_dict = {m['_id']: m for m in members}

    for service in service_list:
        if not 'member_obj_id' in service:
            continue
        member = members_dict[service['member_obj_id']]
        if not 'last_loc' in member:
            continue
        coord = member['last_loc']['coordinates']
        service['distance'] = lib_geo.calc_distance(
            float(loc[0]), float(loc[1]), coord[0], coord[1]
        )


def increase_visit_count(shop_obj_id, visit_count=0):
    db.app_shops.update_one(
        {"_id": shop_obj_id}, {"$set": {"visit_count": visit_count + 1}}
    )
