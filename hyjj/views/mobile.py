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
from ..service.sendsms_service import add_sms, add_code_redis, make_random
from ..common.sendsms import send
from ..common.constant import CODE_ERROR, CODE_SUCCESS, CODE_WRONG
from ..common.loguntil import HyLog
from ..common.jsonutils import other_response


@view_config(route_name='sendCode', renderer='json')
def send_code(request):
    """
    设备初始化登录
    :param request:
    :return:
    """
    error_msg = ''
    dbs = request.dbsession
    user_phone = request.POST.get('phone', '')
    user_name = request.POST.get('name', '')
    content = '尊敬的%s先生，您好，您网上交易重置登录密码验证码为%s，请在三分钟内输入该有效验证码'
    if not user_phone:
        error_msg = '用户手机不能为空！'
    elif not user_name:
        error_msg = '用户姓名不能为空！'
    if not error_msg:
        code = make_random(6)
        content = content % (user_name, code)
        send(user_phone, content)
        redis_host = request.registry.settings['redis.sessions.host']
        add_code_redis(user_phone, code, redis_host)
        error_msg = add_sms(dbs, sms_content=content, phone=user_phone)
    if error_msg:
        json_a = {
            'returnCode': CODE_ERROR,
            'returnMsg': error_msg
        }
    else:
        json_a = {
            'returnCode': CODE_SUCCESS,
            'returnMsg': ''
        }
    HyLog.log_in(request.client_addr, '', ('sendCode failed ' + error_msg if error_msg else 'sendCode success'),
                 'mobile')
    resp = other_response(json_a=json_a)
    return resp


@view_config(route_name='test', renderer='json')
def send_test(request):
    redis_host = request.registry.settings['redis.sessions.host']
    pool = redis.ConnectionPool(host=redis_host, port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    r.set(ip, num)
    date1 = datetime.now().strftime('%Y-%m-%d 23:59:59 %f')
    date2 = datetime.now().strftime('%Y-%m-%d 23:59:59 %f')
    date3 = datetime.now().strftime('%Y-%m-%d 23:59:59 %f')
    add_code_redis(15800786806, 201293, redis_host)
    # add_code_redis(15800786807, 201294, redis_host)
