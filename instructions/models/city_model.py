#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bson
import pymongo

from fupin.models import build_obj_id, filter_obj_ids, filter_obj_id
from config_web import db


field_dict = {
    # city list normal
    "city_ln": ("id", "name", "country_name", "name_en", "home_pic_id", "sort_index",
                "is_hot", "is_dest"),
    # city detail normal
    "city_dn": ("id", "name", "country_name", "name_en", "home_pic_id", "intro"),
    # city switch list
    "city_sl": ("id", "name", "country_name", "name_en", "name_abbr", "is_hot", "is_dest"),

    # trip list normal
    "trip_ln": ("id", "title", "title_pic_id", "city_id"),
    "trip_dn": ("id", "title", "title_pic_id", "city_id", "details")
}


# --- city --- #

def load_city_by_id(city_id):
    city_obj_id = build_obj_id(city_id)
    return load_city_by_obj_id(city_obj_id)

def load_city_by_obj_id(city_obj_id, status="normal"):
    if not city_obj_id:
        return None
    return db.app_cities.find_one({"_id":city_obj_id, "status":status})


def load_city_by_name(city_name, status="normal"):
    return db.app_cities.find_one({"name": city_name, "status": status})


def list_cities_by_cond(cond, field_type="city_ln", sort=None, start=0, limit=30):
    fields = field_dict[field_type] if field_type in field_dict else None

    cities = db.app_cities.find(
        cond, projection=fields, sort=sort, skip=start, limit=limit
    )

    return cities

def insert_city(city_data):
    if not city_data.has_key("status"):
        city_data["status"] = "normal"
    db.app_cities.insert(city_data)


def update_city_by_id(city_id, city_data):
    obj_id = build_obj_id(city_id)
    update_city_by_obj_id(obj_id, city_data=city_data)

def update_city_by_obj_id(obj_id, city_data):
    db.app_cities.update({"_id":obj_id}, {"$set":city_data})


def format_city(city_obj, is_api=False):
    new_city_obj = filter_obj_id(city_obj)

    if "created_by" in city_obj:
        city_obj["created_by"] = str(city_obj["created_by"])

    return new_city_obj


# --- trip --- #

def load_trip_by_id(trip_id):
    trip_obj_id = build_obj_id(trip_id)
    return db.app_trips.find_one({"_id":trip_obj_id, "status":"normal"})

def list_trips_by_city_obj_id(city_obj_id, start=0, limit=30, status="normal"):
    cond = {"city_obj_id":city_obj_id}
    if status:
        cond["status"] = status
    orderby = [("_id", -1)]

    return db.app_trips.find(cond, sort=orderby, skip=start, limit=limit)


def list_trips_by_cond(cond, field_type="list_normal", sort=None, start=0,
        limit=30, is_count=False):
    if is_count:
        return db.app_trips.count(cond)
    if sort is None:
        sort = [("_id", -1)]
    return db.app_trips.find(cond, sort=sort, skip=start, limit=limit)

def insert_trip(trip_data):
    if not trip_data.has_key("status"):
        trip_data["status"] = "normal"

    trip_obj_id = db.app_trips.insert(trip_data)

    # TODO: update photo status
    if trip_data.has_key("details"):
        pic_ids = [d["data"] for d in trip_data["details"] \
            if d.has_key("type") and d["type"] == "photo"]

def update_trip_by_obj_id(obj_id, trip_data):
    db.app_trips.update({"_id":obj_id}, {"$set":trip_data})

def format_trip(trip_obj, field_type="detail_normal"):
    fields = None
    if field_type == "list_normal":
        fields = field_dict["trip_ln"]
    else:
        fields = field_dict["trip_dn"]

    if trip_obj.has_key("city_obj_id"):
        trip_obj["city_id"] = str(trip_obj["city_obj_id"])
        del(trip_obj["city_obj_id"])

    t_trip_obj = filter_obj_id(trip_obj)
    t_trip_obj = dict((k, v) for (k, v) in t_trip_obj.iteritems() \
        if k in fields) if fields else None

    if field_type == "list_normal":
        for detail in trip_obj["details"]:
            if detail["type"] == "text":
                t_trip_obj["detail_intro"] = detail["data"]
                break

    return t_trip_obj
