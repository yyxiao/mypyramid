#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/14
"""

from ..models.product_model import CmsProductNav
from ..common.constant import NAV_TYPE_1, NAV_TYPE_2, NAV_TYPE_3, NAV_TYPE_4
from ..common.dateutils import date_now, get_predate_days, date_pattern1
from ..common.loguntil import HyLog


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
            nav_dict['navTime'] = nav.navTime if nav.navTime else ''
            nav_dict['hsnav'] = nav.hsnav if nav.hsnav else ''
            nav_dict['activeFlag'] = nav.activeFlag if nav.activeFlag else ''
            nav_dict['version'] = nav.version if nav.version else ''
            nav_list.append(nav_dict)
        return nav_list

