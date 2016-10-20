#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/12
"""
PAGE_SIZE = 10

# 证件类型
CARD_TYPE = {'身份证': '01', '护照': '02', '港澳台证件': '03', '军官证': '04'}

SEND_URL = 'http://10.0.130.11:8080/ema/http/SendSms'
SEND_PWD = 'abc123'

STATE_VALID = 1  # 有效
STATE_INVALID = 0   # 无效

CODE_SUCCESS = '00'
CODE_ERROR = '01'
CODE_WRONG = '02'

TIMEOUT_CODE = 180

SMS_DESC = '尊敬的%s先生，您好，您网上交易重置登录密码验证码为%s，请在三分钟内输入该有效验证码'

NAV_TYPE_1 = '1'  # 三个月
NAV_TYPE_2 = '2'  # 六个月
NAV_TYPE_3 = '3'  # 一年
NAV_TYPE_4 = '4'  # 今年
