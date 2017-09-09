#!/usr/bin/env python
# -*- coding: utf-8 -*-

import instructions.controllers.home.index as home_index
import instructions.controllers.admin.index as admin_index
import instructions.controllers.home.user as user_controller
import instructions.controllers.common as common_handler
import instructions.controllers.home.article as article_controller


URLS = list()
URLS.extend(home_index.urls)
URLS.extend(admin_index.urls)
URLS.extend(user_controller.urls)
URLS.extend(common_handler.urls)
URLS.extend(article_controller.urls)


API_URLS = list()
# API_URLS.extend(instructions.handlers.api.api_account.URLS)

ui_modules = dict()
ui_modules.update(home_index.ui_modules)
ui_modules.update(admin_index.ui_modules)
