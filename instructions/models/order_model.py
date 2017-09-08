#!/usr/bin/env python
# -*- coding: utf-8 -*-



import re

import instructions.libs.geo as lib_geo
import instructions.libs.data as lib_data
import instructions.models.user_model as member_model

from instructions.models import build_obj_id
from config_web import db


SHOP_TYPES = ("bars", "massages", "saunas", "others")


def load_order_by_id(order_id):
    order_obj_id = build_obj_id(order_id)
    if not order_obj_id:
        return None
    return db.app_orders.find_one(
        {"_id": order_obj_id, "status":"normal"}
    )


def list_orders_by_conds(conds, field_type='list_normal', sort=None,
                         start=0, limit=30, is_count=False):
    if is_count:
        return db.app_orders.count(conds)
    sort_cond = None
    if not sort:
        sort_cond = [('_id', -1)]

    order_cursor = db.app_orders.find(conds, sort=sort_cond, skip=start, limit=limit)
    order_list = [o for o in order_cursor]

    # list prov and order member info
    if field_type in ('list_prov', 'list_order'):
        member_obj_ids = list()
        if field_type == 'list_prov':
            member_obj_ids = [o['prov_member_obj_id'] for o in order_list]
        if field_type == 'list_order':
            member_obj_ids = [o['order_member_obj_id'] for o in order_list]
        members = member_model.list_member_by_obj_ids(member_obj_ids)
        members_dict = {m['_id']: m for m in members}

        for order in order_list:
            member_obj = None
            if field_type == 'list_prov' and 'prov_member_obj_id' in order:
                member_obj = members_dict[order['prov_member_obj_id']]
            if field_type == 'list_order' and 'order_member_obj_id' in order:
                member_obj = members_dict[order['order_member_obj_id']]
            if not member_obj:
                continue
            order['member_id'] = str(member_obj['_id'])
            order['member_nickname'] = member_obj['nickname']
            order['member_avatar_id'] = member_obj['pic_id'] if 'pic_id' in member_obj else ''

    return order_list


def insert_order(order):
    return db.app_orders.insert(order)


def update_order(obj_id, order_data):
    db.app_orders.update({'_id': obj_id}, {'$set': order_data})


# --- pingpp event --- #

def insert_pingpp_event(event):
    return db.app_pingpp_events.insert(event)


def update_pingpp_event(obj_id, event_data):
    db.app_pingpp_events.update({'_id': obj_id}, {'$set': event_data})


def format_order(order_obj, loc=None, field_type="detail_normal"):
    key_dict = {'_id': 'id', 'prov_member_obj_id': 'prov_member_id',
                'order_member_obj_id': 'order_member_id', 'service_obj_id': 'service_id'}
    for key, val in key_dict.iteritems():
        if not key in order_obj:
            continue
        order_obj[val] = str(order_obj[key])
        order_obj.pop(key)

    if 'order_status' in order_obj:
        order_obj['order_status_name'] = lib_data.ORDER_STATUS_DICT[order_obj['order_status']]

    return order_obj


def increase_visit_count(shop_obj_id, visit_count=0):
    db.app_shops.update_one(
        {"_id": shop_obj_id}, {"$set": {"visit_count": visit_count + 1}}
    )
