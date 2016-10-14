#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/13
"""
import redis
import string
from pyramid.view import view_config
from datetime import datetime
from ..service.sendsms_service import *
from ..common.sendsms import send
from ..common import constant
from ..common.loguntil import HyLog
from ..common.jsonutils import other_response
from ..common.redisutil import create_redis
from ..common.base import BaseUtil


class MobileView(BaseUtil):

    @view_config(route_name='sendCode', renderer='json')
    def send_code(self):
        """
        设备初始化登录
        :param self:
        :return:
        """
        error_msg = ''
        dbs = self.request.dbsession
        user_phone = self.request.POST.get('phone', '')
        user_name = self.request.POST.get('name', '')
        if not user_phone:
            error_msg = '用户手机不能为空！'
        elif not user_name:
            error_msg = '用户姓名不能为空！'
        if not error_msg:
            code = make_random(6)
            content = constant.SMS_DESC % (user_name, code)
            redis_host = self.request.registry.settings['redis.sessions.host']
            r = create_redis(redis_host)
            num = r.get(self.request.client_addr)
            num = int(num) if num else 0
            if num <= 9:
                add_code_redis(user_phone, code, redis_host)
                add_ip_no_redis(self.request.client_addr, num + 1, redis_host)
                send(user_phone, content)
                error_msg = add_sms(dbs, sms_content=content, phone=user_phone)
        if error_msg:
            json_a = {
                'returnCode': constant.CODE_ERROR,
                'returnMsg': error_msg
            }
        else:
            json_a = {
                'returnCode': constant.CODE_SUCCESS,
                'returnMsg': ''
            }
        HyLog.log_in(self.request.client_addr, '', ('sendCode failed ' + error_msg if error_msg else 'sendCode success'),
                     'mobile')
        resp = other_response(json_a=json_a)
        return resp

    @view_config(route_name='accountBinding', renderer='json')
    def account_binding(self):
        """
        设备初始化登录
        :param self:
        :return:
        """
        error_msg = ''
        error_code = constant.CODE_ERROR
        dbs = self.request.dbsession
        user_phone = self.request.POST.get('phone', '')
        user_name = self.request.POST.get('name', '')
        verification_code = self.request.POST.get('verificationCode', '')
        wechat_id = self.request.POST.get('wechatId', '')
        is_risk = 0
        if not user_phone:
            error_msg = '用户手机不能为空！'
        elif not user_name:
            error_msg = '用户姓名不能为空！'
        elif not verification_code:
            error_msg = '验证码不能为空！'
        elif not wechat_id:
            error_msg = '客户ID不能为空！'
        if not error_msg:
            redis_host = self.request.registry.settings['redis.sessions.host']
            r = create_redis(redis_host)
            random_code = r.get(user_phone)
            random_code = int(random_code) if random_code else 0
            if random_code != int(verification_code):
                error_msg = '验证码有误请重新输入！'
                error_code = constant.CODE_WRONG
            else:
                self.customerService.add_customer(self, openid='231d')
        if error_msg:
            json_a = {
                'returnCode': error_code,
                'returnMsg': error_msg,
                'isRiskAssess': is_risk
            }
        else:
            json_a = {
                'returnCode': constant.CODE_SUCCESS,
                'returnMsg': '',
                'isRiskAssess': is_risk
            }
        HyLog.log_in(self.request.client_addr, '', ('accountBinding failed ' + error_msg if error_msg
                                               else 'sendCode success'), 'mobile')
        resp = other_response(json_a=json_a)
        return resp

    @view_config(route_name='test', renderer='json')
    def send_test(self):
        redis_host = self.request.registry.settings['redis.sessions.host']
        pool = redis.ConnectionPool(host=redis_host, port=6379, db=0)
        r = redis.StrictRedis(connection_pool=pool)
        # r.set(ip, num)
        date1 = datetime.now().strftime('%Y-%m-%d 23:59:59 %f')
        date2 = datetime.now().strftime('%Y-%m-%d 23:59:59 %f')
        date3 = datetime.now().strftime('%Y-%m-%d 23:59:59 %f')
        add_code_redis(15800786806, 201293, redis_host)
        # add_code_redis(15800786807, 201294, redis_host)
