#!/usr/bin/env python
# -*- coding: utf-8 -*-

from instructions.models import build_obj_id, filter_obj_id
from config_web import db


def insert_feedback(fb_data):
    if not "status" in fb_data:
        fb_data["status"] = "normal"
    db.app_feedbacks.insert_one(fb_data)
