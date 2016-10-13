#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/13
"""

import redis
import random
import string
from ..models.model import CustomerSms
from ..common.constant import STATE_INVALID, STATE_VALID, TIMEOUT_CODE


def add_sms(dbs, sms_content, phone, create_user):
    msg = ''
    try:
        sms = CustomerSms()
        sms.sms_content = sms_content
        sms.phone = phone
        sms.create_user = create_user
        sms.state = STATE_VALID
        dbs.add(sms)
    except Exception as e:
        msg = '新增短信发送记录失败，请核对后重试'
    return msg


def add_code_redis(phone, code, redis_host):
    pool = redis.ConnectionPool(host=redis_host, port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    r.set(phone, code)
    # 设置过期失效时间
    r.expire(phone, TIMEOUT_CODE)


def make_random(length):
    rand_list = [random.choice(string.digits) for i in range(length)]
    random_code = ''.join([i for i in rand_list])
    return random_code
