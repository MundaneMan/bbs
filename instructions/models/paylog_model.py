#!/usr/bin/env python
# -*- coding: utf-8 -*-



import re

import instructions.libs.geo as lib_geo
import instructions.libs.data as lib_data
import instructions.models.member_model as member_model

from instructions.models import build_obj_id
from config_web import db


def insert_paylog(paylog):
    db.app_paylogs.insert(paylog)
