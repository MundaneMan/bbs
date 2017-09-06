#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from fupin.models import build_obj_id, filter_obj_ids, filter_obj_id
from config_web import db


# ****************************************************************************************
# 帮扶人
# ****************************************************************************************
def load_supporter_by_id(supporter_id):
    supporter_obj_id = build_obj_id(supporter_id)
    return load_supporter_by_obj_id(supporter_obj_id)


def load_supporter_by_obj_id(supporter_obj_id, status="normal"):
    if not supporter_obj_id:
        return None
    return db.app_supporters.find_one({"_id": supporter_obj_id, "status": status})


def list_supporters_by_cond(cond, sort=None, start=0, limit=30, _is_count=False):
    if _is_count:
        return db.app_supporters.find(cond).count()

    if limit is None:
        return db.app_supporters.find(cond, sort=sort)

    supporter_cursor = db.app_supporters.find(
        cond, sort=sort, skip=start, limit=limit
    )
    return supporter_cursor


def load_supporter_by_phone_number(phone_number):
    return db.app_supporters.find_one({"telephone": phone_number, "status": "normal"})


def insert_supporter(supporter_data):
    if not "status" in supporter_data:
        supporter_data["status"] = "normal"
    supporter_data["targets"] = []
    supporter_data["create_at"] = supporter_data["update_at"] = int(time.time())
    db.app_supporters.insert(supporter_data)


def update_supporter_by_id(supporter_id, update_date):
    supporter_obj_id = build_obj_id(supporter_id)
    update_date["update_at"] = int(time.time())
    return db.app_supporters.update_one({"_id": supporter_obj_id}, {"$set": update_date})


def delete_supporter_by_id(supporter_id):
    return update_supporter_by_id(supporter_id, {"status": "deleted"})


def format_supporter(supporter_obj):
    return supporter_obj


def add_target(supporter_id, target_id):
    supporter_obj_id = build_obj_id(supporter_id)
    target_obj_id = build_obj_id(target_id)
    supporter = load_supporter_by_obj_id(supporter_obj_id)

    if "targets" in supporter:
        if target_obj_id in supporter["targets"]:
            return
    return db.app_supporters.update_one({"_id": supporter_obj_id},
                                        {"$push": {"targets": target_obj_id},
                                         "$set": {"update_at": int(time.time())}})


def disconnect_target(supporter_id, target_id):
    supporter_obj_id = build_obj_id(supporter_id)
    target_obj_id = build_obj_id(target_id)
    supporter = load_supporter_by_obj_id(supporter_obj_id)

    if "targets" in supporter:
        if target_obj_id in supporter["targets"]:
            return db.app_supporters.update_one(
                {"_id": supporter_obj_id},
                {"$pull": {"targets": target_obj_id},
                 "$set": {"update_at": int(time.time())}})


def supporter_add_support_organization(organization_id, supporter_id):
    update_supporter_by_id(supporter_id, {"organization_id": organization_id})


# ****************************************************************************************
# 帮扶单位
# ****************************************************************************************
def load_support_organization_by_id(str_id, status="normal"):
    obj_id = build_obj_id(str_id)
    return db.app_support_organizations.find_one({"_id": obj_id, "status": status})


def load_support_organization_by_area_id(area_id, status="normal"):
    return db.app_support_organizations.find_one({"area_id": area_id, "status": status})


def list_support_organizations_by_cond(cond, sort=None, start=0, limit=30, _is_count=False):
    if _is_count:
        return db.app_support_organizations.find(cond).count()

    support_organizations_cursor = db.app_support_organizations.find(
        cond, sort=sort, skip=start, limit=limit
    )
    return support_organizations_cursor


def insert_support_organization(data):
    if not "status" in data:
        data["status"] = "normal"
    data["supporters"] = []
    data["create_at"] = data["update_at"] = int(time.time())
    db.app_support_organizations.insert(data)


def organization_remove_supporter(support_organization_id, supporter_id):
    supporter_obj_id = build_obj_id(supporter_id)
    organization_obj_id = build_obj_id(support_organization_id)
    organization = load_support_organization_by_id(support_organization_id)

    if "supporters" in organization:
        if supporter_obj_id in organization["supporters"]:
            return db.app_support_organizations.update_one(
                {"_id": organization_obj_id},
                {"$pull": {"supporters": supporter_obj_id},
                 "$set": {"update_at": int(time.time())}})


def organization_add_supporter(support_organization_id, supporter_id):
    supporter_obj_id = build_obj_id(supporter_id)
    organization_obj_id = build_obj_id(support_organization_id)
    organization = load_support_organization_by_id(support_organization_id)

    if "supporters" in organization:
        if supporter_obj_id in organization["supporters"]:
            return db.app_support_organizations.update_one(
                {"_id": organization_obj_id},
                {"$push": {"supporters": supporter_obj_id},
                 "$set": {"update_at": int(time.time())}})


def update_support_organization_by_id(str_id, data):
    obj_id = build_obj_id(str_id)
    data["update_at"] = int(time.time())
    return db.app_support_organizations.update_one({"_id": obj_id}, {"$set": data})


def format_support_organization(organization):
    import fupin.libs.data_lib as data_lib

    organization["county_name"], organization["village_name"] = \
        data_lib.load_area_by_id(organization["area_id"], organization["county_id"])

    return organization


def support_organization_add_supporter(organization_id, supporter_id):
    supporter_obj_id = build_obj_id(supporter_id)
    organization_obj_id = build_obj_id(organization_id)
    organization = load_support_organization_by_id(organization_id)

    if "supporters" in organization:
        if supporter_obj_id in organization["supporters"]:
            return
    return db.app_support_organizations.update_one({"_id": organization_obj_id},
                                        {"$push": {"supporters": supporter_obj_id},
                                         "$set": {"update_at": int(time.time())}})


def support_organization_disconnect_supporter(organization_id, supporter_id):
    supporter_obj_id = build_obj_id(supporter_id)
    organization_obj_id = build_obj_id(organization_id)
    organization = load_support_organization_by_id(organization_id)

    if "supporters" in organization:
        if supporter_obj_id in organization["supporters"]:
            return db.app_support_organizations.update_one(
                {"_id": organization_obj_id}, {
                    "$pull": {"supporters": supporter_obj_id},
                    "$set": {"update_at": int(time.time())}})
