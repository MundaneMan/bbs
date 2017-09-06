#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado


def real_remote_ip(handler):
    ip = handler.request.headers.get("X-Forwarded-For", handler.request.remote_ip)
    ip = ip.split(',')[-1].strip()
    ip = handler.request.headers.get("X-Real-Ip", ip)
    if tornado.netutil.is_valid_ip(ip):
        handler.remote_ip = ip
    # AWS uses X-Forwarded-Proto
    proto_header = handler.request.headers.get(
        "X-Scheme", handler.request.headers.get("X-Forwarded-Proto", handler.request.protocol)
    )
    if proto_header in ("http", "https"):
        handler.request.protocol = proto_header
    return ip
