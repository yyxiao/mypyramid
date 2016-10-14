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

        customer_mod = importlib.import_module('service.{0}'.format('customer_service'))
        self.customerService = getattr(customer_mod, 'CustomerService')()
