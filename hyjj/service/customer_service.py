#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/14
"""

import datetime
import json
import urllib.request
from ..models.model import CustomerInfo, CustomerCollProd
from ..common.constant import STATE_INVALID, STATE_VALID, PAGE_SIZE, URL_COUNT_BIND, AUTH_KEY, URL_PROD_OFFER
from ..common.dateutils import date_now, date_pattern1, date_pattern2
from ..common.loguntil import HyLog
from ..service.product_service import ProductService


class CustomerService:

    @staticmethod
    def add_customer(dbs, cust_id, indiinst_flag, cust_name, phone, risk_level, create_user='xyy'):
        msg = ''
        try:
            customer = dbs.query(CustomerInfo).filter(CustomerInfo.phone == phone).first()
            if not customer:
                customer = CustomerInfo()
                customer.create_time = date_now()
            customer.cust_id = cust_id
            customer.indiinst_flag = indiinst_flag
            # customer.openid = openid
            customer.cust_name = cust_name
            customer.phone = phone
            customer.risk_level = risk_level
            customer.risk_expi_date = date_now()
            customer.create_user = create_user
            customer.state = STATE_VALID
            dbs.add(customer)
            dbs.flush()
        except Exception as e:
            msg = '新增用户关联记录失败，请核对后重试'
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

    @staticmethod
    def book_product_by_id(wechat_id, product_name, phone, create_user='xyy'):
        # 调用CRM产品预约接口
        data = {
            'authKey': AUTH_KEY,
            'custid': wechat_id,
            'fundname': product_name,
            'phone': phone
        }
        data = urllib.parse.urlencode(data).encode()
        with urllib.request.urlopen(URL_PROD_OFFER, data) as f:
            crm_msg = f.read().decode()
        # crm = json.loads(crm_msg)
        # return ''

    @staticmethod
    def search_coll_product(dbs, dbms, wechat_id, page_no):
        """
        查找收藏产品
        :param dbs:
        :param dbms:
        :param wechat_id:
        :param page_no:
        :return:
        """
        page_offset = int(page_no) * 10
        coll_prod_list = []
        coll_prods = dbs.query(CustomerCollProd)\
            .filter(CustomerCollProd.cust_id == wechat_id)\
            .order_by(CustomerCollProd.create_time.desc()).offset(page_offset).limit(PAGE_SIZE)
        if coll_prods:
            for coll_prod in coll_prods:
                pro = ProductService.search_col_product(dbms, coll_prod.prod_id)
                if pro:
                    nav_dict = dict()
                    nav_dict['id'] = pro[0] if pro[0] else ''
                    nav_dict['productNo'] = pro[1] if pro[1] else ''
                    nav_dict['fullName'] = pro[2] if pro[2] else ''
                    nav_dict['name'] = pro[3] if pro[3] else ''
                    nav_dict['type'] = pro[4] if pro[4] else ''
                    nav_dict['minDeadline'] = pro[5] if pro[5] else ''
                    nav_dict['maxDeadline'] = pro[6] if pro[6] else ''
                    nav_dict['supplierId'] = pro[7] if pro[7] else ''
                    nav_dict['supplierName'] = pro[8] if pro[8] else ''
                    nav_dict['productScale'] = pro[9] if pro[9] else ''
                    nav_dict['productStat'] = pro[10] if pro[10] else ''
                    nav_dict['hyComment'] = pro[11] if pro[11] else ''
                    nav_dict['productStartDate'] = str(pro[12]) if pro[12] else ''
                    nav_dict['deadlineType'] = pro[13] if pro[13] else ''
                    nav_dict['nav'] = pro[14] if pro[14] else ''
                    nav_dict['navTime'] = datetime.datetime.strptime(pro[15], date_pattern2).strftime(date_pattern1) \
                        if pro[15] else ''
                    nav_dict['accnav'] = pro[16] if pro[16] else ''
                    nav_dict['hotStatus'] = pro[17] if pro[17] else ''
                    coll_prod_list.append(nav_dict)
        return coll_prod_list

    @staticmethod
    def count_bind(phone, realname):
        data = {
            'authKey': AUTH_KEY,
            'phone': phone,
            'realname': realname
        }
        data = urllib.parse.urlencode(data).encode()
        with urllib.request.urlopen(URL_COUNT_BIND, data) as f:
            crm_msg = f.read().decode()
        crm = json.loads(crm_msg)
        return crm
