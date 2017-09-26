#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.log
import tornado.ioloop
import tornado.options

import config_web
from URLS import ui_modules, URLS

from tornado.options import define, options
import bbs.helpers.handler_helper as handler_helper


define("port", default=8008)
define("debug", default=True)


tornado.options.parse_command_line()
config_web.settings["ui_modules"] = ui_modules


class BaseApplication(tornado.web.Application):
    def log_request(self, handler):
        log_method = tornado.log.access_log.error
        if handler.get_status() < 400:
            log_method = tornado.log.access_log.info
        elif handler.get_status() < 500:
            log_method = tornado.log.access_log.warning

        request_time = 1000.0 * handler.request.request_time()
        remote_ip = handler_helper.real_remote_ip(handler)
        request_summary = "%s %s (%s)" % (handler.request.method, handler.request.uri,
                                          remote_ip)
        log_method("%d %s %.2fms", handler.get_status(),
                   request_summary, request_time)


app = BaseApplication(URLS, **config_web.settings)
# app.listen(9900, xheaders=True)
app.xheaders = True
# app.add_handlers(config_web.settings["api_domain"], API_URLS)
app.db = config_web.db


def main():
    app.listen(options.port, address="", xheaders=True)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
