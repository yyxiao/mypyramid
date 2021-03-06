#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/14
"""

from sqlalchemy import or_, func
from ..models.product_model import CmsProductNav, CmsProduct
from ..models.model import CustomerCollProd
from ..common.constant import NAV_TYPE_1, NAV_TYPE_2, NAV_TYPE_3, NAV_TYPE_4, PAGE_SIZE, \
    RISK_FIRST, RISK_SECOND, RISK_THIRD
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
            navs = navs.filter(CmsProductNav.navTime >= start_year)
        navs = navs.order_by(CmsProductNav.navTime).all()
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
        return nav_list

    @staticmethod
    def search_products(dbs, wechat_id, page_no, search_key, risk_level):
        page_offset = int(page_no) * 10
        pro_list = []
        # create sqlalchemy sub query
        nav1 = dbs.query(CmsProductNav.productId, CmsProductNav.nav, CmsProductNav.navTime, CmsProductNav.accnav)\
            .order_by(CmsProductNav.productId.desc(), CmsProductNav.navTime.desc()).subquery()
        nav_all = dbs.query(nav1).group_by(nav1.c.productId).subquery()
        pros = dbs.query(CmsProduct.id, CmsProduct.productNo, CmsProduct.fullName, CmsProduct.name,
                         CmsProduct.type, CmsProduct.minDeadline, CmsProduct.maxDeadline, CmsProduct.supplierId,
                         CmsProduct.supplierName, CmsProduct.productScale, CmsProduct.productStat, CmsProduct.hyComment,
                         CmsProduct.productStartDate, CmsProduct.deadlineType,
                         nav_all.c.nav, nav_all.c.navTime, nav_all.c.accnav, CmsProduct.hotStatus)\
            .outerjoin(nav_all, CmsProduct.id == nav_all.c.productId)\
            .filter(CmsProduct.useStat == '1').filter(CmsProduct.isDeleted == '0')\
            .filter(CmsProduct.platFormCode.like('%FUND%'))
        # count pros_num and filter_num from cmsProduct
        count_pros = dbs.query(func.count(CmsProduct.id))\
            .outerjoin(nav_all, CmsProduct.id == nav_all.c.productId)\
            .filter(CmsProduct.useStat == '1').filter(CmsProduct.isDeleted == '0')\
            .filter(CmsProduct.platFormCode.like('%FUND%')).scalar()
        count_user_pros = dbs.query(func.count(CmsProduct.id)) \
            .outerjoin(nav_all, CmsProduct.id == nav_all.c.productId) \
            .filter(CmsProduct.useStat == '1').filter(CmsProduct.isDeleted == '0')\
            .filter(CmsProduct.platFormCode.like('%FUND%'))
        if risk_level == RISK_FIRST:
            pros = pros.filter(CmsProduct.riskLv == '1')
            count_user_pros = count_user_pros.filter(CmsProduct.riskLv == '1')
        elif risk_level == RISK_SECOND:
            pros = pros.filter(CmsProduct.riskLv <= '3')
            count_user_pros = count_user_pros.filter(CmsProduct.riskLv <= '3')
        if search_key:
            pros = pros.filter(or_(CmsProduct.fullName.like('%' + search_key + '%'),
                                   CmsProduct.name.like('%' + search_key + '%')))
            count_user_pros = count_user_pros.filter(or_(CmsProduct.fullName.like('%' + search_key + '%'),
                                                         CmsProduct.name.like('%' + search_key + '%')))
        pros = pros.order_by(CmsProduct.id.desc()).offset(page_offset).limit(PAGE_SIZE)
        count_user_pros = count_user_pros.scalar()
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
            nav_dict['hotStatus'] = pro[17] if pro[17] else ''
            pro_list.append(nav_dict)
        # HyLog.log_info(pro_list)
        return pro_list, count_pros, count_user_pros

    @staticmethod
    def search_product_info(dbs, dbms, wechat_id, product_id):
        nav1 = dbs.query(CmsProductNav.productId, CmsProductNav.nav, CmsProductNav.navTime, CmsProductNav.accnav) \
            .order_by(CmsProductNav.productId.desc(), CmsProductNav.navTime.desc()).subquery()
        nav_all = dbs.query(nav1).group_by(nav1.c.productId).subquery()
        pro = dbms.query(CmsProduct.id, CmsProduct.productNo, CmsProduct.fullName, CmsProduct.name,
                         CmsProduct.type, CmsProduct.minDeadline, CmsProduct.maxDeadline, CmsProduct.supplierId,
                         CmsProduct.supplierName, CmsProduct.productScale, CmsProduct.productStat, CmsProduct.hyComment,
                         CmsProduct.productStartDate, CmsProduct.deadlineType, CmsProduct.manager, CmsProduct.riskLv,
                         CmsProduct.hotStatus, CmsProduct.publishStartDate,
                         nav_all.c.nav, nav_all.c.navTime, nav_all.c.accnav, CmsProduct.deadlineDesc)\
            .outerjoin(nav_all, CmsProduct.id == nav_all.c.productId)\
            .filter(CmsProduct.id == product_id).filter(CmsProduct.isDeleted == '0').first()
        cust_pro = dbs.query(CustomerCollProd)\
            .filter(CustomerCollProd.prod_id == product_id).filter(CustomerCollProd.cust_id == wechat_id).first()
        nav_dict = dict()
        if pro:
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
            nav_dict['manager'] = pro[14] if pro[14] else ''
            nav_dict['riskLv'] = pro[15] if pro[15] else ''
            nav_dict['hotStatus'] = pro[16] if pro[16] else ''
            nav_dict['publishStartDate'] = str(pro[17]) if pro[17] else ''
            nav_dict['isCollect'] = cust_pro.state if cust_pro else '0'
            nav_dict['nav'] = pro[18] if pro[18] else ''
            nav_dict['navTime'] = datetime.datetime.strptime(pro[19], date_pattern2).strftime(date_pattern1) \
                if pro[19] else ''
            nav_dict['accnav'] = pro[20] if pro[20] else ''
            nav_dict['deadlineDesc'] = pro[21] if pro[21] else ''
        HyLog.log_info("[search_product_info]:" + str(nav_dict))
        return nav_dict

    @staticmethod
    def search_col_product(dbms, prod_id):
        nav1 = dbms.query(CmsProductNav.productId, CmsProductNav.nav, CmsProductNav.navTime, CmsProductNav.accnav) \
            .order_by(CmsProductNav.productId.desc(), CmsProductNav.navTime.desc()).subquery()
        nav_all = dbms.query(nav1).group_by(nav1.c.productId).subquery()
        product = dbms.query(CmsProduct.id, CmsProduct.productNo, CmsProduct.fullName, CmsProduct.name,
                             CmsProduct.type, CmsProduct.minDeadline, CmsProduct.maxDeadline, CmsProduct.supplierId,
                             CmsProduct.supplierName, CmsProduct.productScale, CmsProduct.productStat,
                             CmsProduct.hyComment, CmsProduct.productStartDate, CmsProduct.deadlineType,
                             nav_all.c.nav, nav_all.c.navTime, nav_all.c.accnav, CmsProduct.hotStatus) \
            .outerjoin(nav_all, CmsProduct.id == nav_all.c.productId) \
            .filter(CmsProduct.useStat == '1')\
            .filter(CmsProduct.isDeleted == '0')\
            .filter(CmsProduct.id == prod_id)
        product = product.order_by(CmsProduct.id.desc()).first()
        return product
