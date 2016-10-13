#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/13
"""

from ..models.model import CustomerSms
from ..common.constant import STATE_INVALID, STATE_VALID


class sendSmsService:
    @staticmethod
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
