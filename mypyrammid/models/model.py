#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
from sqlalchemy import (
    Column,
    INT,
    VARCHAR,
    Sequence,
    DateTime,
    TEXT
)

from .meta import Base, mypyramid_SCHEMA, Other
from datetime import datetime


class RiskQuestion(Base):
    __tablename__ = 'risk_question'                                                              # 问题表
    id = Column(INT, Sequence('risk_question_id_seq', schema=mypyramid_SCHEMA), primary_key=True)    # 主键ID
    question_type = Column(VARCHAR(1))                   # 类型
    question_name = Column(VARCHAR(300))                # 问题描述
    create_user = Column(VARCHAR(20))                   # 创建人
    create_time = Column(DateTime)                      # 创建时间
    state = Column(VARCHAR(1))                  # 是否有效


class RiskAnswers(Base):
    __tablename__ = 'risk_answers'                                                              # 答案表
    id = Column(INT, Sequence('risk_answers_id_seq', schema=mypyramid_SCHEMA), primary_key=True)    # 主键ID
    question_id = Column(INT)                           # 问题id
    answer_name = Column(VARCHAR(100))                  # 答案描述
    selection_no = Column(VARCHAR(2))                      # 选项编号
    create_user = Column(VARCHAR(20))                   # 创建人
    create_time = Column(DateTime)                      # 创建时间
    score = Column(INT)                      # 分数


class CustomerRisk(Base):
    __tablename__ = 'customer_risk'                                                             # 客户答卷表
    id = Column(INT, Sequence('customer_risk_id_seq', schema=mypyramid_SCHEMA), primary_key=True)    # 主键ID
    cust_id = Column(VARCHAR(20))                       # 客户id
    evaluating_time = Column(DateTime)                  # 评测时间
    cust_answers = Column(VARCHAR(200))                  # 风险题目答案
    score = Column(INT)                                 # 答卷得分
    risk_level = Column(VARCHAR(6))                        # 风险等级
    remark = Column(VARCHAR(100))                       # 备注
    create_user = Column(VARCHAR(20))                   # 创建人
    create_time = Column(DateTime)                      # 创建时间
    update_user = Column(VARCHAR(20))                   # 更新人
    update_time = Column(DateTime)                      # 更新时间
    state = Column(VARCHAR(1))                          # 是否有效


class CustomerInfo(Base):
    __tablename__ = 'customer_info'                                                             # 客户答卷表
    id = Column(INT, Sequence('customer_info_id_seq', schema=mypyramid_SCHEMA), primary_key=True)    # 主键ID
    cust_id = Column(VARCHAR(20))                       # 客户id
    indiinst_flag = Column(VARCHAR(1))                     # 对私对公标志
    openid = Column(VARCHAR(20))                        # 微信OPENID
    cust_name = Column(VARCHAR(20))                     # 真实姓名
    phone = Column(VARCHAR(11))                         # 手机号码
    risk_level = Column(VARCHAR(6))                        # 客户风险等级
    risk_expi_date = Column(DateTime)                   # 风险评估失效日期
    version = Column(VARCHAR(1))                        # 版本号
    create_user = Column(VARCHAR(20))                   # 创建人
    create_time = Column(DateTime)                      # 创建时间
    update_user = Column(VARCHAR(20))                   # 更新人
    update_time = Column(DateTime)                      # 更新时间
    state = Column(VARCHAR(1))                          # 是否有效


class CustomerCollProd(Base):
    __tablename__ = 'customer_coll_prod'                # 客户收藏产品表
    id = Column(INT, Sequence('customer_coll_prod_id_seq', schema=mypyramid_SCHEMA), primary_key=True)    # 主键ID
    cust_id = Column(VARCHAR(20))                       # 客户id
    prod_id = Column(VARCHAR(20))                       # 产品id
    version = Column(VARCHAR(1))                        # 版本号
    create_user = Column(VARCHAR(20))                   # 创建人
    create_time = Column(DateTime)                      # 创建时间
    update_user = Column(VARCHAR(20))                   # 更新人
    update_time = Column(DateTime)                      # 更新时间
    state = Column(VARCHAR(1))                          # 是否有效


class CustomerOrderSeq(Base):
    __tablename__ = 'customer_order_seq'                # 客户预约流水表
    id = Column(INT, Sequence('customer_order_seq_id_seq', schema=mypyramid_SCHEMA), primary_key=True)  # 主键ID
    cust_id = Column(VARCHAR(20))                       # 客户id
    prod_id = Column(VARCHAR(20))                       # 产品id
    phone = Column(VARCHAR(20))                         # 预约电话
    version = Column(VARCHAR(1))                        # 版本号
    create_user = Column(VARCHAR(20))                   # 创建人
    create_time = Column(DateTime)                      # 创建时间
    update_user = Column(VARCHAR(20))                   # 更新人
    update_time = Column(DateTime)                      # 更新时间
    state = Column(VARCHAR(1))                          # 是否有效


class CustomerSms(Base):
    __tablename__ = 'customer_sms'                                                              # 发送短信表
    id = Column(INT, Sequence('customer_sms_id_seq', schema=mypyramid_SCHEMA), primary_key=True)    # 主键ID
    sms_content = Column(VARCHAR(300))                  # 问题描述
    phone = Column(VARCHAR(11))                         # 手机号码
    create_user = Column(VARCHAR(20))                   # 创建人
    create_time = Column(DateTime)                      # 创建时间
    state = Column(VARCHAR(1))                  # 是否有效
