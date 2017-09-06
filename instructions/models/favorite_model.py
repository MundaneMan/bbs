#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'matt'

from fupin.models import build_obj_id, filter_obj_ids, filter_obj_id
from config_web import db

import fupin.libs.geo as lib_geo


# def load_favorite_
def check_if_favorited(member_obj_id, target_obj_id):
    fav_obj = db.app_favorites.find_one(
        {"member_obj_id":member_obj_id, "target_obj_id":target_obj_id}
    )
    # if fav_obj and fav_obj[""]

    pass