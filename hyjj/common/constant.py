#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/12
"""
PAGE_SIZE = 10

# 证件类型
CARD_TYPE = {'身份证': '01', '护照': '02', '港澳台证件': '03', '军官证': '04'}

SEND_URL = 'http://10.0.130.11:8080/ema/http/SendSms'
SEND_PWD = 'abc123'

STATE_VALID = '1'  # 有效
STATE_INVALID = '0'   # 无效

QUESTION_USER = '0'     # 个人
QUESTION_ORG = '1'      # 机构

CODE_SUCCESS = '00'
CODE_ERROR = '01'
CODE_WRONG = '02'
CODE_NO_RISK = '04'

TIMEOUT_CODE = 180

SMS_DESC = '尊敬的%s先生，您好，您账号绑定验证码为%s，请在三分钟内输入该有效验证码'

NAV_TYPE_1 = '1'  # 三个月
NAV_TYPE_2 = '2'  # 六个月
NAV_TYPE_3 = '3'  # 一年
NAV_TYPE_4 = '4'  # 今年

# 评测类型
RISK_FIRST = '01'
RISK_SECOND = '02'
RISK_THIRD = '03'
RISK_MSG = {'00': '保守型:您的投资目标是寻求资本的保值，其次为资本的缓和升值，可承受的风险较低。',
            '01': '稳健性:您的投资目标是资本缓和升值，其次为资本保值，可承担中等风险。',
            '02': '积极型:您的投资目标是增值财富，您可承受一定风险，并了解高收益总是与高风险相伴。'}
RISK_TYPE_LEVEL = {'00': '低风险',
                   '01': '中风险,低风险',
                   '02': '高风险,中风险,低风险'}

AUTH_KEY = 'E10ADC3949BA59ABBE56E057F20F883E'

URL_COUNT_BIND = 'http://10.12.5.42:8080/hycrm/wechat/countBind'
URL_RISK_EVAL = 'http://10.12.5.42:8080/hycrm/wechat/riskEval'
URL_PROD_OFFER = 'http://10.12.5.42:8080/hycrm/wechat/prodOffer'

