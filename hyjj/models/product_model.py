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
    TEXT,
    CHAR,
    DECIMAL
)

from .meta import Other


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


class CmsProduct(Other):
    __tablename__ = 'hy_cms_private_product'
    id = Column(INT, primary_key=True)  # id
    productNo = Column(VARCHAR(50))  # 产品编号
    fullName = Column(VARCHAR(50))  # 产品名称
    name = Column(VARCHAR(50))  # 产品简称
    type = Column(VARCHAR(8))  # 产品简称
    supplierId = Column(INT)  # 产品简称
    supplierName = Column(VARCHAR(64))  # 基金净值
    productScale = Column(VARCHAR(20))  # 累计净值
    riskYield = Column(VARCHAR(128))  # 分红
    invAdviser = Column(VARCHAR(128))  # 净值公布时间
    invDirection = Column(TEXT)  # 沪深300指数
    riskControlMode = Column(TEXT)  # 备注
    deadlineType = Column(CHAR(1))  # 备用1
    minDeadline = Column(VARCHAR(20))  # 备用2
    maxDeadline = Column(VARCHAR(20))  # 备用3
    deadlineDesc = Column(TEXT)  # 活动标记
    minAmount = Column(VARCHAR(20))  #
    addAmount = Column(VARCHAR(20))  #
    inComeType = Column(CHAR(1))  #
    minInCome = Column(VARCHAR(20))  #
    maxInCome = Column(VARCHAR(20))  #
    incomeDesc = Column(TEXT)  #
    maxSaleNum = Column(INT)  #
    publishStartDate = Column(DateTime)  #
    publishEndDate = Column(DateTime)  #
    productStartDate = Column(DateTime)  #
    productEndDateType = Column(VARCHAR(200))  #
    productEndDate = Column(VARCHAR(200))  #
    transType = Column(VARCHAR(200))  #
    transferDate = Column(VARCHAR(200))  #
    attachFile = Column(VARCHAR(300))  #
    infoDesc = Column(TEXT)  #
    auditUserId = Column(VARCHAR(20))  #
    auditDate = Column(DateTime)  #
    auditStat = Column(CHAR(1))  #
    useStat = Column(CHAR(1))  #
    productStat = Column(CHAR(1))  #
    runStat = Column(CHAR(1))  #
    interestDate = Column(TEXT)  #
    remark = Column(VARCHAR(500))  #
    commission = Column(TEXT)  #
    activeFlag = Column(CHAR(1))  #
    createBy = Column(VARCHAR(64))  # 创建人
    riskLv = Column(CHAR(1))  #
    transferTipDate = Column(VARCHAR(200))  #
    maxAmount = Column(DECIMAL(20))  #
    createDate = Column(DateTime)  # 创建时间
    updateBy = Column(VARCHAR(64))  # 更新人
    updateDate = Column(DateTime)  # 更新时间
    version = Column(INT)  # '版本号'
    prdLevel = Column(CHAR(1))  #
    prdCharacter = Column(VARCHAR(64))  #
    incomeWay = Column(VARCHAR(64))  #
    manager = Column(VARCHAR(64))  #
    gp = Column(VARCHAR(64))  #
    custodian = Column(VARCHAR(64))  #
    hyComment = Column(VARCHAR(512))  #
    isDeleted = Column(CHAR(1))  #
    hotStatus = Column(CHAR(2))  #
    adImg = Column(VARCHAR(512))  #
    adImgUrl = Column(VARCHAR(256))  #
    platFormCode = Column(VARCHAR(50))  #
