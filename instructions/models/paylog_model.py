#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'matt'

import re

import fupin.libs.geo as lib_geo
import fupin.libs.data as lib_data
import fupin.models.member_model as member_model

from fupin.models import build_obj_id
from config_web import db


def insert_paylog(paylog):
    db.app_paylogs.insert(paylog)
