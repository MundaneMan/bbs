#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from bbs.models import build_obj_id, build_id_time_str
from config_web import db


def load_article_by_id(article_id):
    article_obj_id = build_obj_id(article_id)
    return load_article_by_obj_id(article_obj_id)


def load_article_by_obj_id(article_obj_id, status="normal"):
    if not article_obj_id:
        return None
    return db.articles.find_one({"_id": article_obj_id, "status": status})


def load_article_by_cond(cond):
    if "status" not in cond:
        cond['status'] = 'normal'
    return db.articles.find_one(cond)


def distinct_article_id(cond=None, is_obj_id=False):
    if cond and not isinstance(cond, dict):
        raise ValueError('cond should be dict')
    c = cond or {}
    if 'status' not in c:
        c['status'] = 'normal'

    obj_id_list = db.articles.distinct('_id', c)
    if is_obj_id:
        return obj_id_list
    return [str(i) for i in obj_id_list]


def list_articles_by_cond(cond, sort=[('create_at', -1)], start=0, limit=30, _is_count=False):
    if ('status' not in cond) and isinstance(cond, dict):
        cond['status'] = 'normal'
    if _is_count:
        return db.articles.find(cond).count()
    if limit is None:
        fp_article_cursor = db.articles.find(cond)
    else:
        fp_article_cursor = db.articles.find(
            cond, sort=sort, skip=start, limit=limit
        )
    return fp_article_cursor


def insert_article(article_data):
    if "status" not in article_data:
        article_data["status"] = "normal"
    article_data['create_at'] = article_data['update_at'] = int(time.time())
    result = db.articles.insert_one(article_data)
    return result.inserted_id


def update_article_by_id(article_id, article_data):
    article_obj_id = build_obj_id(article_id)
    conds = {"_id": article_obj_id}
    article_data['update_at'] = int(time.time())
    db.articles.update(conds, {"$set": article_data})


def delete_article_by_id(article_id):
    update_article_by_id(article_id, {"status": "deleted"})


def distinct_article_field(field, cond=None, _is_count=False):
    if not cond:
        cond = dict()
    if "status" not in cond:
        cond["status"] = "normal"
    if field:
        if _is_count:
            return len(db.articles.distinct(field, cond))
        return db.articles.distinct(field, cond)
    return None


def format_article(_obj, t_format='%Y-%m-%d %H:%M:%S'):
    if "created_at" in _obj:
        _obj["created_at"] = time.strftime(t_format,
                                          time.localtime(_obj["created_at"]))
    if "_id" in _obj:
        _obj["_id"] = str(_obj["_id"])

    return _obj