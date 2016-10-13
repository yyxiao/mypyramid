#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/12
"""


import hashlib
import urllib.request
from ..common.constant import SEND_PWD, SEND_URL


def send_sms(phone, content):
    # 密钥
    data = {
        'Account': 3,
        'Password': md5_encode(SEND_PWD),
        'Phone': phone,
        'Content': content,
        'SubCode': '',
        'SendTime': '',
    }
    data = urllib.parse.urlencode(data).encode()
    with urllib.request.urlopen(SEND_URL, data) as f:
        crm_msg = f.read().decode()
        return crm_msg


def md5_encode(pwd):
    m = hashlib.md5()
    m.update(pwd.encode('ascii'))
    encode_str = m.hexdigest()
    return encode_str

# send_sms(15800786806, '尊敬的肖先生，您好，您网上交易重置登录密码验证码为457345，请在三分钟内输入该有效验证码')

