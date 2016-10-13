#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/13
"""

from ..models.model import CustomerSms


class sendSmsService:

    def add_sms(self, sms_content, phone, create_user):
        try:
            sms = CustomerSms()
            sms.sms_content = sms_content
            sms.phone = phone
            sms.create_user = create_user
            self.add(sms)
            msg = '新增短信发送记录成功'
        except Exception as e:
            msg = '新增短信发送记录失败，请核对后重试'
        return msg
