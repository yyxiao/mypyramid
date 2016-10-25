#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/13
"""

import random
import string
import time
from ..models.model import CustomerSms
from ..common.constant import STATE_INVALID, STATE_VALID, TIMEOUT_CODE
from ..common.redisutil import create_redis
from ..common.loguntil import HyLog
from ..common.dateutils import date_now


class SendSmsService:

    @staticmethod
    def add_sms(dbs, sms_content, phone, create_user='xyy'):
        msg = ''
        try:
            sms = CustomerSms()
            sms.sms_content = sms_content
            sms.phone = phone
            sms.create_user = create_user
            sms.create_time = date_now()
            sms.state = STATE_VALID
            dbs.add(sms)
        except Exception as e:
            msg = '新增短信发送记录失败，请核对后重试'
            HyLog.log_error(e + msg)
        return msg

    @staticmethod
    def add_code_redis(phone, code, redis_host):
        r = create_redis(redis_host)
        r.set(phone, code)
        r.expire(phone, TIMEOUT_CODE)

    @staticmethod
    def add_ip_no_redis(ip, num, redis_host):
        r = create_redis(redis_host)
        r.set(ip, num)
        r.expireat(ip, int(time.mktime(time.strptime(date_now('%Y-%m-%d 23:59:50'), '%Y-%m-%d %H:%M:%S'))))

    @staticmethod
    def make_random(length):
        rand_list = [random.choice(string.digits) for i in range(length)]
        random_code = ''.join([i for i in rand_list])
        return random_code
