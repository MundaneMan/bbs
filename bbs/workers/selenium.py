#!/usr/bin/env python
# -*- coding: utf-8 -*-


from selenium import webdriver
driver = webdriver.Chrome()
driver.get("//www.baidu.com")
driver.find_element_by_id("kw").send_keys("我爱python")