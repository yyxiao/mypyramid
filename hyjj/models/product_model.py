#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/18
"""

from sqlalchemy import (
    Column,
    INT,
    VARCHAR,
    Sequence,
    DateTime,
    TEXT
)

from .meta import Other


# class City(Other):
#     __tablename__ = 'city'                                                              # 测试多数据源多表
#     code = Column(VARCHAR(5), primary_key=True)                   # code
#     name = Column(VARCHAR(20))                  # name


class CmsProductNav(Other):
    __tablename__ = 'hy_cms_product_nav'
    id = Column(INT, primary_key=True)                   # id
    productId = Column(INT)                     # '产品ID'
    nav = Column(VARCHAR(16))                   # 基金净值
    accnav = Column(VARCHAR(16))                   # 累计净值
    shareBonus = Column(VARCHAR(16))                   # 分红
    navTime = Column(VARCHAR(16))                   # 净值公布时间
    hsnav = Column(VARCHAR(16))                   # 沪深300指数
    remarks = Column(VARCHAR(512))                   # 备注
    remark1 = Column(VARCHAR(256))                   # 备用1
    remark2 = Column(VARCHAR(256))                   # 备用2
    remark3 = Column(VARCHAR(256))                   # 备用3
    activeFlag = Column(VARCHAR(1))                   # 活动标记
    version = Column(INT)  # '版本号'
    createDate = Column(DateTime)  # 创建时间
    createBy = Column(VARCHAR(64))  # 创建人
    updateDate = Column(DateTime)  # 更新时间
    updateBy = Column(VARCHAR(64))  # 更新人
