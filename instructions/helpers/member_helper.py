#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config_web


def build_avatar_url(avatar_id, pic_type="icon"):
    if avatar_id:
        return "".join([config_web.settings["static_url"], "avatars",
            "/", pic_type, "/", avatar_id, ".jpg"])



