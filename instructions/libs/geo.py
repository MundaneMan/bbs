# -*- coding: utf-8 -*-
#!/usr/bin/env python

import math
import json
import requests

from fupin.libs.shapes import Point, Rect


def calc_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    earth_r = 6372.8
    return c * earth_r


def get_city_name_by_loc(loc):
    # TODO: should we check and get location from google?
    if is_loc_in_china(loc):
        # print "IN CHINA !!!"
        pass
    url = "http://api.map.baidu.com/geocoder/v2/?ak=" + "duFxrIijbRfete3QpK4C5IvV" + \
        "&output=json&pois=1&location=" + str(loc[1]) + "," + str(loc[0])
    r = requests.get(url)

    try:
        json_obj = json.loads(r.text)
    except:
        print "json decode error..."
        return

    if not "status" in json_obj or json_obj["status"] != 0:
        return

    result_dict = json_obj["result"]
    formatted_address = result_dict["formatted_address"]
    address_dict = result_dict["addressComponent"]
    city_name = address_dict["city"]
    country = address_dict["country"]
    district = address_dict["district"]
    province = address_dict["province"]
    street = address_dict["street"]
    country_code = address_dict["country_code"]

    if city_name.endswith(u'市'):
        city_name = city_name[:-1]

    # TODO: save address?
    # TODO: 国外怎么办
    # print "city_name:", city_name
    return city_name


def is_loc_in_china(loc):
    region_rects = (GeoRect(49.220400, 79.446200, 42.889900, 96.330000),
                    GeoRect(54.141500, 109.687200, 39.374200, 135.000200),
                    GeoRect(42.889900, 73.124600, 29.529700, 124.143255),
                    GeoRect(29.529700, 82.968400, 26.718600, 97.035200),
                    GeoRect(29.529700, 97.025300, 20.414096, 124.367395),
                    GeoRect(20.414096, 107.975793, 17.871542, 111.744104))
    exclude_rects = (GeoRect(25.398623, 119.921265, 21.785006, 122.497559),
                     GeoRect(22.284000, 101.865200, 20.098800, 106.665000),
                     GeoRect(21.542200, 106.452500, 20.487800, 108.051000),
                     GeoRect(55.817500, 109.032300, 50.325700, 119.127000),
                     GeoRect(55.817500, 127.456800, 49.557400, 137.022700),
                     GeoRect(44.892200, 131.266200, 42.569200, 137.022700))

    # in mongo db, long goes first
    lat, lon = float(loc[1]), float(loc[0])
    for r_rect in region_rects:
        if r_rect.contains(lat, lon):
            for e_rect in exclude_rects:
                if e_rect.contains(lat, lon):
                    return False
            return True
    return False


class GeoRect(object):
    def __init__(self, lat1, lon1, lat2, lon2):
        self.west = min(lon1, lon2)
        self.north = max(lat1, lat2)
        self.east = max(lon1, lon2)
        self.south = min(lat1, lat2)

    def contains(self, lat, lon):
        return self.west <= lon and self.east >= lon and self.north >= lat and self.south <= lat
