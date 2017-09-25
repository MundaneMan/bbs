#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from bbs.models import build_obj_id, build_id_time_str
from config_web import db


# --- article --- #

def load_article_by_id(article_id):
    article_obj_id = build_obj_id(article_id)
    return load_article_by_obj_id(article_obj_id)


def load_article_by_obj_id(article_obj_id):
    return db.articles.find_one({"_id": article_obj_id, "status": "normal"})


def list_article_by_obj_ids(obj_ids):
    r_obj_ids = list(set(obj_ids))
    articles = db.articles.find({"_id": {"$in": r_obj_ids}})
    return articles


def list_articles_by_cond(m_cond, sort=None, start=0, limit=30, is_count=False):
    if is_count:
        return db.articles.count(m_cond)

    return db.articles.find(m_cond, sort=sort, skip=start, limit=limit)


def insert_article(article_data):
    if "status" not in article_data:
        article_data["status"] = "normal"
    article_data["created_at"] = int(time.time())
    result = db.articles.insert_one(article_data)
    return result.inserted_id


def update_article_by_obj_id(obj_id, article_data):
    db.articles.update({"_id": obj_id}, {"$set": article_data})


def is_field_data_exist(field, data):
    cond = {field: data}
    print cond
    count = db.articles.find(cond).count()
    if count > 0:
        return True
    return False


def format_article(article_obj, ftype=""):
    if "_id" in article_obj:
        article_obj["article_id"] = str(article_obj["_id"])

    return article_obj

