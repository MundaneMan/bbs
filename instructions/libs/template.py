#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.escape import xhtml_escape


def set_checkbox_value(key, form_data=None, obj=None):
    check_text = " checked=\"checked\""
    if form_data and key in form_data and form_data[key]:
        return check_text
    if obj and key in obj and obj[key]:
        return check_text

    return ""


def build_checkbox(key, val, form_data=None, obj=None, fid=""):
    check_html = ""
    if (form_data and key in form_data and val in form_data[key]) or \
            (obj and key in obj and val in obj[key]):
        check_html = ' checked="checked"'

    html = '<input type="checkbox" id="{}" name="f_{}" value="{}"{}/>'
    return html.format(fid, key, val, check_html)


def build_radiobox(key, val, form_data=None, obj=None):
    check_html = ""
    if (form_data and key in form_data and form_data[key] == val) or \
            (obj and key in obj and obj[key] == val):
        check_html = ' checked="checked"'

    return '<input type="radio" name="f_{}" value="{}"{}/>'.format(key, val, check_html)


def build_form_text(key, form_data=None, obj=None, fclass="form-control", fplaceholder=""):
    html = '<input type="text" name="f_%s" value="%s" class="%s" placeholder="%s"/>'
    fval = ""
    if obj and key in obj:
        fval = unicode(obj[key])
        if ("start_time" in key or "close_time" in key) and len(fval) < 4:
            fval = "0" + fval
    if form_data and key in form_data:
        fval = form_data[key]

    return html % (key, xhtml_escape(fval), fclass, fplaceholder)


def build_form_select(key, form_data=None, obj=None, fvalues=None, fclass="form-control"):
    if not fvalues:
        return ""
    html = '<select name="f_%s" class="%s">%s</select>'
    option_list = list()
    option_str = '<option value="%s"%s>%s</option>'
    sel_str = ' selected="selected"'

    option_list.append(option_str % ("", "", u"-- 请选择 --"))

    if isinstance(fvalues, dict):
        for fval, ftext in fvalues.iteritems():
            if form_data and key in form_data and form_data[key] == fval:
                option_list.append(option_str % (fval, sel_str, ftext))
            elif obj and key in obj and obj[key] == fval:
                option_list.append(option_str % (fval, sel_str, ftext))
            else:
                option_list.append(option_str % (fval, "", ftext))
    else:
        for fdict in fvalues:
            if form_data and key in form_data and form_data[key] == fdict['name']:
                option_list.append(option_str % (fdict['id'], sel_str, fdict['name']))
            elif obj and key in obj and obj[key] == fdict['id']:
                option_list.append(option_str % (fdict['id'], sel_str, fdict['name']))
            else:
                option_list.append(option_str % (fdict['id'], "", fdict['name']))

    return html % (key, fclass, "".join(option_list))
