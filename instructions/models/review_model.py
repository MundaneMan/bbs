#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'matt'

import datetime
import calendar

from fupin.models import build_obj_id, filter_obj_ids, filter_obj_id
from config_web import db


def list_reviews_by_cond(cond, order="id_desc", start=0, limit=30,
        is_count=False):
    if is_count:
        return db.app_reviews.count(cond)

    order_by = None
    if order == "id_desc":
        order_by = [("_id", -1)]

    reviews = [r for r in db.app_reviews.find(cond, sort=order_by, skip=start,
        limit=limit)]
    return reviews


def update_review(review_obj_id, review_data):
    db.app_reviews.update({"_id":review_obj_id}, {"$set":review_data})

def update_shop_raw(shop_obj_id, shop_data_raw):
    db.app_shops.update({"_id":shop_obj_id}, shop_data_raw)


def insert_review(review_data):
    if not review_data.has_key("status"):
        review_data["status"] = "normal"
    db.app_reviews.insert(review_data)


def format_review(review_obj):
    date_obj = review_obj["_id"].generation_time
    # review_obj["created_at"] = time.mktime(date_obj.timetuple())
    review_obj["created_at"] = calendar.timegm(date_obj.timetuple())

    review_obj = filter_obj_id(review_obj)

    review_obj["target_id"] = str(review_obj["target_obj_id"])
    review_obj.pop("target_obj_id", None)

    if review_obj.has_key("author_obj_id"):
        review_obj["author_id"] = str(review_obj["author_obj_id"])
        del(review_obj["author_obj_id"])

    return review_obj


def calc_avg_review_score(target_obj_id):
    # db.command("aggregate")
    piplines = [
        {"$match":{"target_obj_id":target_obj_id}},
        {"$group":{"_id":"$target_obj_id", "avg_score":{"$avg":"$score"}}}
    ]
    result = db.app_reviews.aggregate(piplines)
    for r in result:
        return r["avg_score"] * 2

    return 0
