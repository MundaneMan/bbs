#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from fupin.models import build_obj_id, filter_obj_ids, filter_obj_id
from config_web import db


def load_target_by_id(target_id):
    target_obj_id = build_obj_id(target_id)
    return load_target_by_obj_id(target_obj_id)


def load_target_by_obj_id(target_obj_id, status="normal"):
    if not target_obj_id:
        return None
    return db.app_fp_targets.find_one({"_id": target_obj_id, "status": status})


def load_target_by_person_id(person_id, status="normal"):
    conds = {"person_id": person_id}
    if status:
        conds["status"] = status
    return db.app_fp_targets.find_one(conds)


def load_target_by_id_number(id_number, status="normal"):
    conds = {"id_number": id_number}
    if status:
        conds["status"] = status
    return db.app_fp_targets.find_one(conds)


def load_target_by_third_id(data):
    if "id_number" in data:
        id_number = data["id_number"]
        if id_number not in ("", "-"):
            return load_target_by_id_number(id_number)

    elif "person_id" in data:
        person_id = data["person_id"]
        if person_id not in ("", "-"):
            return load_target_by_person_id(person_id)

    return None


def distinct_target_families(cond, _is_count=True):
    target_families = db.app_fp_targets.distinct("family_id", cond)
    if not _is_count:
        return target_families
    return len(target_families)


def list_fp_targets_by_cond(cond, sort=None, start=0, limit=30, _is_count=False):
    if _is_count:
        return db.app_fp_targets.find(cond).count()
    if limit is None:
        fp_target_cursor = db.app_fp_targets.find(cond)
    else:
        fp_target_cursor = db.app_fp_targets.find(
            cond, sort=sort, skip=start, limit=limit
        )
    return fp_target_cursor


def insert_fp_target(target_data):
    if "status" not in target_data:
        target_data["status"] = "normal"
    target_data['create_at'] = target_data['update_at'] = int(time.time())
    target_data['supporters'] = []
    db.app_fp_targets.insert(target_data)


def update_target_by_id(target_id, target_data):
    target_obj_id = build_obj_id(target_id)
    conds = {"_id": target_obj_id}
    target_data['update_at'] = int(time.time())
    target_data = fill_target_update_data(target_data)
    db.app_fp_targets.update(conds, {"$set": target_data})


def update_target_by_third_id(target_data, person_id=None, id_number=None):
    conds = {"id_number": id_number} if id_number else {"person_id": person_id}
    target_data['update_at'] = int(time.time())
    db.app_fp_targets.update(conds, {"$set": target_data})


def fill_target_update_data(target_data):
    """ 根据表单中的ID获取与之对应的值
    """

    import fupin.libs.data_lib as data_lib

    if "area_id" in target_data:
        target_data["county_name"], target_data["village_name"] = \
            data_lib.load_area_by_id(target_data["area_id"], target_data["county_id"])

    if "id_type_id" in target_data:
        target_data["id_type"] = \
            data_lib.load_id_type_by_id(target_data["id_type_id"])

    if "family_type_id" in target_data:
        target_data["family_type"] = \
            data_lib.load_family_type_by_id(target_data["family_type_id"])

    if "major_poverty_cause_id" in target_data:
            target_data["major_poverty_cause"] = \
            data_lib.load_major_poverty_cause_by_id(target_data["major_poverty_cause_id"])

    if "nationality_id" in target_data:
            target_data["nationality"] = \
            data_lib.load_nationality_by_id(target_data["nationality_id"])

    if "edu_history_id" in target_data:
            target_data["edu_history"] = \
            data_lib.load_edu_history_by_id(target_data["edu_history_id"])

    if "gender_id" in target_data:
            target_data["gender"] = \
            data_lib.load_gender_by_id(target_data["gender_id"])

    return target_data


def delete_target_by_id(target_id):
    update_target_by_id(target_id, {"status": "deleted"})


def distinct_target_field_count(field, cond=None, _is_count=False):
    if not cond:
        cond = dict()
    if "status" not in cond:
        cond["status"] = "normal"
    if field:
        if _is_count:
            return len(db.app_fp_targets.distinct(field, cond))
        return db.app_fp_targets.distinct(field, cond)
    return None


def format_fp_target(target_obj):
    try:
        target_obj["lon"], target_obj["lat"] = target_obj["gps"]["coordinates"]
    except:
        pass
    return target_obj


def add_supporter(supporter_id, target_id):
    supporter_obj_id = build_obj_id(supporter_id)
    target_obj_id = build_obj_id(target_id)
    target = load_target_by_obj_id(target_obj_id)

    if "supporters" in target:
        if supporter_obj_id in target["supporters"]:
            return
    return db.app_fp_targets.update_one(
        {"_id": target_obj_id}, {
            "$push": {"supporters": supporter_obj_id},
            "$set": {"update_at": int(time.time())}})


def disconnect_supporter(supporter_id, target_id):
    supporter_obj_id = build_obj_id(supporter_id)
    target_obj_id = build_obj_id(target_id)
    target = load_target_by_obj_id(target_obj_id)

    if "supporters" in target:
        if supporter_obj_id in target["supporters"]:
            return db.app_fp_targets.update_one(
                {"_id": target_obj_id}, {
                    "$pull": {"supporters": supporter_obj_id},
                    "$set": {"update_at": int(time.time())}})


def filter_target_data(target_data, _is_update=False):
    import fupin.libs.data_lib as data_lib

    heath_keys = [k for k in data_lib.HUAMINGCE_COL_KEYS if k]
    target_keys = [k for k in data_lib.POVERTY_TARGET_COL_KEYS if k]
    other_keys = ['address']
    all_keys = heath_keys + target_keys + other_keys

    # raw_dict用于插入数据, target_data用于更新数据
    if not _is_update:
        raw_dict = dict.fromkeys(all_keys, '')

    # 过滤键值对, 获取各个可选项id
    target_data = {k: v for k, v in target_data.items() if k in all_keys}

    county_name, village_name = target_data.get("county_name"), target_data.get("village_name")
    id_type = target_data.get("id_type")
    family_type = target_data.get("family_type")
    major_poverty_cause = target_data.get("major_poverty_cause")

    target_data["area_id"] = data_lib.load_area_id_by_name(county_name, village_name)
    target_data["county_id"] = target_data["area_id"].split("_")[0]
    target_data["id_type_id"] = data_lib.load_id_type_id_by_name(id_type)
    target_data["family_type_id"] = data_lib.load_family_type_id_by_name(family_type)
    target_data["major_poverty_cause_id"] = data_lib.load_major_poverty_cause_id_by_name(
        major_poverty_cause)

    if _is_update:
        return target_data

    raw_dict.update(target_data)
    return raw_dict


def check_and_edit(target_data):
    """ 检查用户是否在target表中, 存在则更新, 反之插入
    :param target_info: 待更新或插入的信息, 需要包含个人编码或身份证号
    :return: True(存在)/False(不存在)
    """

    id_number = target_data.get('id_number', None)
    person_id = target_data.get('person_id', None)

    if person_id is not None:
        t = load_target_by_person_id(person_id)
    elif id_number is not None:
        t = load_target_by_id_number(id_number)
    else:
        raise Exception('target_info should be contain person_id or id_number')

    # 筛选数据, 符合字段的数据才能被更新或插入
    if t:
        target_data = filter_target_data(target_data, _is_update=True)
        update_target_by_third_id(target_data, person_id=person_id, id_number=id_number)
        return False

    target_data = filter_target_data(target_data)
    insert_fp_target(target_data)
    return True


# target_housing_model
def load_target_housing_by_id(target_housing_id):
    target_housing_obj_id = build_obj_id(target_housing_id)
    return load_target_housing_by_obj_id(target_housing_obj_id)


def load_target_housing_by_obj_id(target_housing_obj_id, status="normal"):
    if not target_housing_obj_id:
        return None
    return db.app_fp_target_housing.find_one(
        {"_id": target_housing_obj_id, "status": status})


def load_target_housing_by_id_number(id_number, status="normal"):
    conds = {"id_number": id_number}
    if status:
        conds["status"] = status
    return db.app_fp_target_housing.find_one(conds)


def update_target_housing_by_id_number(id_number, target_housiing_data):
    conds = {"id_number": id_number}
    target_housiing_data['update_at'] = int(time.time())
    db.app_fp_targets_housing.update(conds, {"$set": target_housiing_data})


def list_fp_targets_housing_by_cond(cond, sort=None, start=0, limit=30, _is_count=False):
    if _is_count:
        return db.app_fp_target_housing.find(cond).count()
    fp_target_house_cursor = db.app_fp_target_housing.find(
        cond, sort=sort, skip=start, limit=limit
    )

    return fp_target_house_cursor


def insert_fp_target_housing(target_house_data):
    if not "status" in target_house_data:
        target_house_data["status"] = "normal"
    target_house_data['create_at'] = int(time.time())
    db.app_fp_target_housing.insert(target_house_data)


def format_fp_target_housing(target_house_obj):
    return target_house_obj


# target_finance_model
def load_target_finance_by_id(target_finance_id):
    target_finance_obj_id = build_obj_id(target_finance_id)
    return load_target_finance_by_obj_id(target_finance_obj_id)


def load_target_finance_by_obj_id(target_finance_obj_id, status="normal"):
    if not target_finance_obj_id:
        return None
    return db.app_fp_target_finance.find_one(
        {"_id": target_finance_obj_id, "status": status})


def load_target_finance_by_id_number_and_subsidy_type(id_number, subsidy_type,
                                                      status="normal"):
    conds = {"id_number": id_number, "subsidy_type": subsidy_type}
    if status:
        conds["status"] = status
    return db.app_fp_target_finance.find_one(conds)


def update_target_finance_by_id_number_and_subsidy_type(id_number, subsidy_type,
                                                        target_finance_data):
    conds = {"id_number": id_number, "subsidy_type": subsidy_type}
    target_finance_data['update_at'] = int(time.time())
    db.app_fp_targets_finance.update(conds, {"$set": target_finance_data})


def list_fp_targets_finance_by_cond(cond, sort=None, start=0, limit=30, _is_count=False):
    if _is_count:
        return db.app_fp_target_finance.find(cond).count()
    fp_target_finance_cursor = db.app_fp_target_finance.find(
        cond, sort=sort, skip=start, limit=limit
    )

    return fp_target_finance_cursor


def insert_fp_target_finance(target_finance_data):
    if not "status" in target_finance_data:
        target_finance_data["status"] = "normal"
        target_finance_data['create_at'] = int(time.time())
    db.app_fp_target_finance.insert(target_finance_data)


def format_fp_target_finance(target_finance_obj):
    return target_finance_obj


# target_medical_serious_illness_model
def load_target_medical_serious_illness_by_id(str_id):
    obj_id = build_obj_id(str_id)
    return load_target_medical_serious_illness_by_obj_id(obj_id)


def load_target_medical_serious_illness_by_obj_id(obj_id, status="normal"):
    if not obj_id:
        return None
    return db.app_fp_target_medical_serious_illness.find_one(
        {"_id": obj_id, "status": status})


def list_fp_targets_medical_serious_illness_by_cond(
    cond, sort=None, start=0, limit=30, _is_count=False):
    if _is_count:
        return db.app_fp_target_medical_serious_illness.find(cond).count()
    
    cursor = db.app_fp_target_medical_serious_illness.find(
        cond, sort=sort, skip=start, limit=limit)
    return cursor


def insert_or_update_fp_target_medical_serious_illness(data):
    conds = {"medical_id_number": data["medical_id_number"],
             "year": data["year"]}
    old_record = db.app_fp_target_medical_serious_illness.find_one(conds)

    data["is_notice"] = False
    if old_record:
        for k in data:
            if data[k] == old_record[k]:
                data["update_at"] = int(time.time())
                db.app_fp_target_medical_serious_illness.update_one(conds, {"$set": data})
                return
        else:
            return
    else:
        data["create_at"] = data["update_at"] = int(time.time())
        data["status"] = "normal"

    db.app_fp_target_medical_serious_illness.insert_one(data)


def format_fp_target_medical_serious_illness(mongo_obj):
    return mongo_obj


# target_medical_addition_hospitalization_model
def load_target_medical_addition_hospitalization_by_id(str_id, status="normal"):
    obj_id = build_obj_id(str_id)
    return db.app_fp_target_medical_addition_hospitalization.find_one({
        "_id": obj_id, "status": status})


def list_fp_targets_medical_addition_hospitalization_by_cond(
    cond, sort=None, start=0, limit=30, _is_count=False):
    if _is_count:
        return db.app_fp_target_medical_addition_hospitalization.find(cond).count()

    cursor = db.app_fp_target_medical_addition_hospitalization.find(
        cond, sort=sort, skip=start, limit=limit)
    return cursor


def insert_or_update_fp_target_medical_addition_hospitalization(data):
    conds = {"id_number": data["id_number"],
             "year": data["year"]}
    old_record = db.app_fp_target_medical_addition_hospitalization.find_one(conds)

    data["is_notice"] = False
    if old_record:
        for k in data:
            if data[k] == old_record[k]:
                data["update_at"] = int(time.time())
                db.app_fp_target_medical_addition_hospitalization.update_one(
                    conds, {"$set": data})
                return
        else:
            return
    else:
        data["create_at"] = data["update_at"] = int(time.time())
        data["status"] = "normal"

    db.app_fp_target_medical_addition_hospitalization.insert_one(data)


def format_fp_target_medical_addition_hospitalization(mongo_obj):
    return mongo_obj
