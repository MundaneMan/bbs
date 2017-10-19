#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bbs.controllers.home.index as index
import bbs.controllers.admin.a_index as a_index
import bbs.controllers.home.user as user
import bbs.controllers.common as common
import bbs.controllers.home.article as article

import bbs.controllers.admin.a_article as a_article


URLS = list()
URLS.extend(index.urls)
URLS.extend(a_index.urls)
URLS.extend(user.urls)
URLS.extend(common.urls)
URLS.extend(article.urls)

URLS.extend(a_article.urls)


API_URLS = list()
# API_URLS.extend(bbs.handlers.api.api_account.URLS)

ui_modules = dict()
ui_modules.update(common.ui_modules)
ui_modules.update(a_index.ui_modules)
