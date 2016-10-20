#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/14
"""

from ..models.model import CustomerInfo, CustomerCollProd
from ..common.constant import STATE_INVALID, STATE_VALID
from ..common.dateutils import date_now
from ..common.loguntil import HyLog


class CustomerService:

    @staticmethod
    def add_customer(dbs, cust_id, indiinst_flag, openid, cust_name, phone, risk_level, create_user='xyy'):
        msg = ''
        try:
            customer = dbs.query(CustomerInfo).filter(CustomerInfo.phone == phone).first()
            if not customer:
                customer = CustomerInfo()
            customer.cust_id = cust_id
            customer.indiinst_flag = indiinst_flag
            customer.openid = openid
            customer.cust_name = cust_name
            customer.phone = phone
            customer.risk_level = risk_level
            customer.risk_expi_date = date_now()
            customer.create_user = create_user
            customer.create_time = date_now()
            customer.state = STATE_VALID
            dbs.add(customer)
            dbs.flush()
        except Exception as e:
            msg = '新增短信发送记录失败，请核对后重试'
            HyLog.log_error(e)
        return msg

    @staticmethod
    def collect_product_by_id(dbs, wechat_id, product_id, create_user='xyy'):
        try:
            cus_coll = dbs.query(CustomerCollProd)\
                .filter(CustomerCollProd.prod_id == product_id).filter(CustomerCollProd.cust_id == wechat_id).first()
            if not cus_coll:
                cus_coll = CustomerCollProd()
                cus_coll.cust_id = wechat_id
                cus_coll.prod_id = product_id
                cus_coll.create_user = create_user
                cus_coll.create_time = date_now()
                cus_coll.state = STATE_VALID
            else:
                cus_coll.state = STATE_INVALID if cus_coll.state == STATE_VALID else STATE_VALID
                cus_coll.update_user = create_user
                cus_coll.update_time = date_now()
            dbs.merge(cus_coll)
            dbs.flush()
            HyLog.log_info("[search_product_info]:" + str(cus_coll))
            return cus_coll.state
        except Exception as e:
            HyLog.log_error(e)
            return ''
