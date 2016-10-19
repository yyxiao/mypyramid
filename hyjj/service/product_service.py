#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/14
"""

from ..models.product_model import CmsProductNav
from ..common.constant import STATE_INVALID, STATE_VALID
from ..common.dateutils import date_now
from ..common.loguntil import HyLog


class ProductService:

    @staticmethod
    def search_navs(dbs, wechat_id, pro_id, nav_type):
        nav_list = []
        navs = dbs.query(CmsProductNav).filter(CmsProductNav.productId == pro_id)
        if nav_type == 1:
            navs = navs.filter(CmsProductNav.navTime == pro_id)
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

