#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bbs.controllers.home.index as home_index
import bbs.controllers.admin.index as admin_index
import bbs.controllers.home.user as user_controller
import bbs.controllers.common as common_handler
import bbs.controllers.home.article as article_controller


URLS = list()
URLS.extend(home_index.urls)
URLS.extend(admin_index.urls)
URLS.extend(user_controller.urls)
URLS.extend(common_handler.urls)
URLS.extend(article_controller.urls)


API_URLS = list()
# API_URLS.extend(bbs.handlers.api.api_account.URLS)

ui_modules = dict()
ui_modules.update(home_index.ui_modules)
ui_modules.update(admin_index.ui_modules)
