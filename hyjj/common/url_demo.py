#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/25
"""
import urllib.request
import json


def request_crm():
    # 密钥
    data = {
        'authKey': 'E10ADC3949BA59ABBE56E057F20F883E',
        'phone': 15120074584,
        'realname': 'sdf'
    }
    data = urllib.parse.urlencode(data).encode()
    with urllib.request.urlopen('http://10.11.11.27:8080/hycrm/wechat/countBind', data) as f:
        crm_msg = f.read().decode()
    crm = json.loads(crm_msg)
    print('数据获取结果：{0}'.format(crm_msg))
    print('数据获取结果：{0}' + crm['code'])
    print('数据获取结果：{10}' + crm["objects"]["indiinstflag"])


if __name__ == '__main__':
    request_crm()