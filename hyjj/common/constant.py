#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/12
"""

# 证件类型
CARD_TYPE = {'身份证': '01', '护照': '02', '港澳台证件': '03', '军官证': '04'}

SEND_URL = 'http://10.0.130.11:8080/ema/http/SendSms'
SEND_PWD = 'abc123'

STATE_VALID = 'A'
STATE_INVALID = 'B'

CODE_SUCCESS = '0000000'
CODE_ERROR = '0000001'
CODE_WRONG = '0000002'
