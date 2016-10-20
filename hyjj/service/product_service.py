#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/14
"""

from ..models.product_model import CmsProductNav, CmsProduct
from ..common.constant import NAV_TYPE_1, NAV_TYPE_2, NAV_TYPE_3, NAV_TYPE_4, PAGE_SIZE
from ..common.dateutils import date_now, get_predate_days, date_pattern1, date_pattern2
from ..common.loguntil import HyLog
import datetime


class ProductService:

    @staticmethod
    def search_navs(dbs, wechat_id, pro_id, nav_type):
        nav_list = []
        navs = dbs.query(CmsProductNav.id, CmsProductNav.productId, CmsProductNav.nav, CmsProductNav.accnav,
                         CmsProductNav.navTime, CmsProductNav.hsnav, CmsProductNav.activeFlag, CmsProductNav.version)\
            .filter(CmsProductNav.productId == pro_id)
        if nav_type == NAV_TYPE_1:
            navs = navs.filter(CmsProductNav.navTime > get_predate_days(date_now(date_pattern1), -90))
        elif nav_type == NAV_TYPE_2:
            navs = navs.filter(CmsProductNav.navTime > get_predate_days(date_now(date_pattern1), -180))
        elif nav_type == NAV_TYPE_3:
            navs = navs.filter(CmsProductNav.navTime > get_predate_days(date_now(date_pattern1), -365))
        elif nav_type == NAV_TYPE_4:
            start_year = date_now()[0:4] + '/01/01'
            navs = navs.filter(CmsProductNav.navTime > start_year)
        navs = navs.all()
        for nav in navs:
            nav_dict = dict()
            nav_dict['id'] = nav.id if nav.id else ''
            nav_dict['productId'] = nav.productId if nav.productId else ''
            nav_dict['nav'] = nav.nav if nav.nav else ''
            nav_dict['accnav'] = nav.accnav if nav.accnav else ''
            nav_dict['navTime'] = datetime.datetime.strptime(nav.navTime, date_pattern2).strftime(date_pattern1) \
                if nav.navTime else ''
            nav_dict['hsnav'] = nav.hsnav if nav.hsnav else ''
            nav_dict['activeFlag'] = nav.activeFlag if nav.activeFlag else ''
            nav_dict['version'] = nav.version if nav.version else ''
            nav_list.append(nav_dict)
        HyLog.log_info("[search_navs]:" + nav_list)
        return nav_list

    @staticmethod
    def search_products(dbs, wechat_id, page_no):
        page_offset = int(page_no) * 10
        pro_list = []
        nav1 = dbs.query(CmsProductNav.productId, CmsProductNav.nav, CmsProductNav.navTime, CmsProductNav.accnav)\
            .order_by(CmsProductNav.productId.desc(), CmsProductNav.navTime.desc()).subquery()
        nav_all = dbs.query(nav1).group_by(nav1.c.productId).subquery()
        pros = dbs.query(CmsProduct.id, CmsProduct.productNo, CmsProduct.fullName, CmsProduct.name,
                         CmsProduct.type, CmsProduct.minDeadline, CmsProduct.maxDeadline, CmsProduct.supplierId,
                         CmsProduct.supplierName, CmsProduct.productScale, CmsProduct.productStat, CmsProduct.hyComment,
                         CmsProduct.productStartDate, CmsProduct.deadlineType,
                         nav_all.c.nav, nav_all.c.navTime, nav_all.c.accnav)\
            .outerjoin(nav_all, CmsProduct.id == nav_all.c.productId)\
            .filter(CmsProduct.useStat == '1').filter(CmsProduct.isDeleted == '0')\
            .order_by(CmsProduct.id.desc()).offset(page_offset).limit(PAGE_SIZE)
        for pro in pros:
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
            pro_list.append(nav_dict)
        HyLog.log_info("[search_products]:" + str(pro_list))
        return pro_list

    @staticmethod
    def search_product_info(dbs, wechat_id, product_id):
        pro = dbs.query(CmsProduct.id, CmsProduct.productNo, CmsProduct.fullName, CmsProduct.name,
                         CmsProduct.type, CmsProduct.minDeadline, CmsProduct.maxDeadline, CmsProduct.supplierId,
                         CmsProduct.supplierName, CmsProduct.productScale, CmsProduct.productStat, CmsProduct.hyComment,
                         CmsProduct.productStartDate, CmsProduct.deadlineType)\
            .filter(CmsProduct.id == product_id).filter(CmsProduct.isDeleted == '0').first()
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
        nav_dict['isCollect'] = '0'
        HyLog.log_info("[search_product_info]:" + str(nav_dict))
        return nav_dict
