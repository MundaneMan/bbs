#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Skill Model Class"""



import re

import instructions.libs.geo as lib_geo
import instructions.models.member_model as member_model

from instructions.models import build_obj_id
from config_web import db


SHOP_TYPES = ("bars", "massages", "saunas", "others")


def load_shop_by_id(shop_id):
    shop_obj_id = build_obj_id(shop_id)
    if not shop_obj_id:
        return None
    return db.app_shops.find_one(
        {"_id": shop_obj_id, "status":"normal"}
    )


def list_shops_by_cond(cond, loc=None, filed_type="list_normal", sort=None, start=0,
        limit=30, is_count=False):
    if is_count:
        return db.app_shops.count(cond)
    sort_cond = None
    if sort == "location" and loc:
        cond["loc"] = {
            "$nearSphere": {"$geometry": {
                "type": "Point", "coordinates": [loc[0], loc[1]]}
            },
        }
    elif sort == "visited":
        sort_cond = [("visit_count", -1)]
    elif sort == "ratings":
        sort_cond = [("avg_score", -1)]

    shop_cursor = db.app_shops.find(cond, sort=sort_cond, skip=start, limit=limit)
    shop_list = [calc_shop_distance(shop, loc) for shop in shop_cursor]

    if not sort or sort == "default":
        max_distance = min_distance = -1
        max_v_count = -1
        for shop_obj in shop_list:
            # print shop_obj["distance"]
            if "distance" in shop_obj and \
                    (float(shop_obj["distance"]) > max_distance or max_distance == -1):
                max_distance = float(shop_obj["distance"])
            if "visit_count" in shop_obj and \
                    (shop_obj["visit_count"] > max_v_count or max_v_count == -1):
                max_v_count = shop_obj["visit_count"]

        distance_diff = max_distance - min_distance
        max_v_count = max_v_count if max_v_count > 0 else 100
        for shop_obj in shop_list:
            distance_score = rating_score = 0
            if "distance" in shop_obj and shop_obj["distance"] > 0 and distance_diff > 0:
                distance_score = (1.0 - (shop_obj["distance"] / max_distance)) * 0.3
            if "avg_score" in shop_obj:
                rating_score = (shop_obj["avg_score"] / 10.0) * 0.4
            visit_count = shop_obj["visit_count"] if "visit_count" in shop_obj else 0
            visit_score = visit_count * 1.0 / max_v_count * 0.3

            # print shop_obj["name_en"], shop_obj["distance"],
            # distance_score, rating_score, visit_score

            shop_obj["sort_score"] = distance_score + rating_score + visit_score

        shop_list = sorted(shop_list, key=lambda k: k["sort_score"], reverse=True)

    return shop_list


def list_shops_by_city_id(city_id, start=0, limit=30, status="normal"):
    city_obj_id = build_obj_id(city_id)
    return list_shops_by_city_obj_id(
            city_obj_id, start=start, limit=limit, status=status
    )


def list_shops_by_city_obj_id(city_obj_id, shop_type=None, start=0, limit=30,
        status="normal", is_count=False):
    cond = {"city_obj_id": city_obj_id}
    if status:
        cond["status"] = status

    if is_count:
        return list_shops_by_cond(cond, is_count=True)

    if shop_type:
        cond["type"] = shop_type
    return list_shops_by_cond(cond, start=start, limit=limit)


def list_shop_reports():
    return db.app_feedbacks.find({"status":"normal"})


def list_favorited_shops(member_obj_id):
    member = member_model.load_member_by_obj_id(member_obj_id)
    if not member or "favorite_shops" not in member:
        return []

    shops = list_shops_by_cond({"_id": {"$in": member["favorite_shops"]}})
    return shops


def list_shop_by_keyword(keyword, status="normal"):
    s_regex = {"$regex": re.compile(keyword, re.IGNORECASE)}
    search_dict = {"$or": [{"name_en": s_regex}, {"name_cn": s_regex}, {"name_local": s_regex}]}
    cond = search_dict if status is None else {"$and": [{"status": status}, search_dict]}

    return list_shops_by_cond(cond)


def insert_skill(skill_data):
    if not skill_data.has_key("status"):
        skill_data["status"] = "normal"
    return db.app_skills.insert(skill_data)

def update_shop(shop_obj_id, shop_data):
    db.app_shops.update({"_id":shop_obj_id}, {"$set":shop_data})

def update_shop_raw(shop_obj_id, shop_data_raw):
    db.app_shops.update({"_id":shop_obj_id}, shop_data_raw)


def calc_shop_distance(shop_obj, loc=None):
    if loc and len(loc) == 2 and "loc" in shop_obj:
        lat = float(loc[1])
        lon = float(loc[0])
        coord = shop_obj["loc"]["coordinates"]
        shop_obj["distance"] = lib_geo.calc_distance(lon, lat, coord[0], coord[1])

    return shop_obj


def format_shop(shop_obj, loc=None, field_type="detail_normal"):
    if shop_obj.has_key("_id"):
        shop_obj["id"] = str(shop_obj["_id"])
        del(shop_obj["_id"])
    if shop_obj.has_key("city_obj_id"):
        shop_obj["city_id"] = str(shop_obj["city_obj_id"])
        del(shop_obj["city_obj_id"])

    # long, lat
    if "loc" in shop_obj and "coordinates" in shop_obj["loc"]:
        shop_obj["loc_lat"] = str(shop_obj["loc"]["coordinates"][1])
        shop_obj["loc_long"] = str(shop_obj["loc"]["coordinates"][0])
        shop_obj.pop("loc", None)

    return shop_obj


def increase_visit_count(shop_obj_id, visit_count=0):
    db.app_shops.update_one(
            {"_id": shop_obj_id}, {"$set": {"visit_count": visit_count + 1}}
    )
