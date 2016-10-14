#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/14
"""

from ..models.model import CustomerInfo
from ..common.constant import STATE_INVALID, STATE_VALID


class CustomerService:

    def add_customer(self, dbs, cust_id, indiinst_flag, openid, cust_name, phone, risk_level, risk_expi_date, create_user='xyy'):
        msg = ''
        try:
            customer = CustomerInfo()
            customer.cust_id = cust_id
            customer.indiinst_flag = indiinst_flag
            customer.openid = openid
            customer.cust_name = cust_name
            customer.phone = phone
            customer.risk_level = risk_level
            customer.risk_expi_date = risk_expi_date
            customer.create_user = create_user
            customer.state = STATE_VALID
            dbs.add(customer)
            self.HyLog.log_info('新增短信发送记录失败，请核对后重试')
        except Exception as e:
            msg = '新增短信发送记录失败，请核对后重试'
            self.HyLog.log_error(e + msg)
        return msg
