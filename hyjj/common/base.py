#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/14
"""
import importlib
from ..service import sendsms_service


class BaseUtil:

    def __init__(self, request):
        self.request = request

        hy_log_mod = importlib.import_module('hyjj.common.{0}'.format('loguntil'))
        customer_mod = importlib.import_module('hyjj.service.{0}'.format('customer_service'))
        send_sms_mod = importlib.import_module('hyjj.service.{0}'.format('sendsms_service'))
        self.customerService = getattr(customer_mod, 'CustomerService')()
        self.sendSmsService = getattr(send_sms_mod, 'SendSmsService')()
        self.hyLog = getattr(hy_log_mod, 'HyLog')()
