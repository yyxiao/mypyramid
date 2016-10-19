#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/14
"""
import importlib


class BaseUtil:

    def __init__(self, request):
        self.request = request

        hy_log_mod = importlib.import_module('hyjj.common.{0}'.format('loguntil'))
        customer_mod = importlib.import_module('hyjj.service.{0}'.format('customer_service'))
        send_sms_mod = importlib.import_module('hyjj.service.{0}'.format('sendsms_service'))
        risk_mod = importlib.import_module('hyjj.service.{0}'.format('risk_service'))
        product_mod = importlib.import_module('hyjj.service.{0}'.format('product_service'))
        self.customerService = getattr(customer_mod, 'CustomerService')()
        self.sendSmsService = getattr(send_sms_mod, 'SendSmsService')()
        self.riskService = getattr(risk_mod, 'RiskService')()
        self.productService = getattr(product_mod, 'ProductService')()
        self.hyLog = getattr(hy_log_mod, 'HyLog')()
