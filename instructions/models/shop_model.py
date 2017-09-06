#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fupin.models import build_obj_id
from config_web import db


def load_shop_by_id(shop_id):
    shop_obj_id = build_obj_id(shop_id)
    if not shop_obj_id:
        return None
    return db.app_shops.find_one(
        {"_id": shop_obj_id, "status":"normal"}
    )


def list_shops_by_cond(cond, loc=None, field_type="list_normal", sort=None, start=0, limit=30, is_count=False):
    sort_cond = None
    if sort == 'location' and loc:
        pass
    elif sort == 'ratings':
        sort_cond = [('avg_score', -1)]
    shop_cursor = db.app_shops.find(cond, sort=sort_cond, skip=start, limit=limit)
    shop_list = [format_shop(s) for s in shop_cursor]

    if field_type == 'list_home':
        pass

    return shop_list


def insert_shop(shop_data):
    if not shop_data.has_key("status"):
        shop_data["status"] = "normal"
    return db.app_shops.insert(shop_data)


def format_shop(shop_obj, field_type="detail_normal"):
    if "_id" in shop_obj:
        shop_obj["id"] = str(shop_obj["_id"])
        shop_obj.pop('_id')
    if "city_obj_id" in shop_obj:
        shop_obj["city_id"] = str(shop_obj["city_obj_id"])
        shop_obj.pop('city_obj_id')

    # long, lat
    if "loc" in shop_obj and "coordinates" in shop_obj["loc"]:
        shop_obj["loc_lat"] = str(shop_obj["loc"]["coordinates"][1])
        shop_obj["loc_long"] = str(shop_obj["loc"]["coordinates"][0])
        shop_obj.pop("loc", None)

    return shop_obj
