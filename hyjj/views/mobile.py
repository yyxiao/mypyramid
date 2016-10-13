#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/13
"""
from pyramid.view import view_config
from ..service.sendsms_service import sendSmsService
from ..common.sendsms import send
from ..common.constant import CODE_ERROR, CODE_SUCCESS, CODE_WRONG


@view_config(route_name='sendCode', renderer='json')
def send_code(request):
    """
    设备初始化登录
    :param request:
    :return:
    """
    self = request.dbsession
    user_id = request.POST.get('user_id', '')
    user_phone = request.POST.get('phone', 0)
    user_name = request.POST.get('name', '')
    content = '尊敬的%s先生，您好，您网上交易重置登录密码验证码为%s，请在三分钟内输入该有效验证码'
    if not user_phone:
        error_msg = '用户手机不能为空！'
    elif not user_name:
        error_msg = '用户姓名不能为空！'
    if not error_msg:
        send(user_phone, content % (user_name, '111111'))
        error_msg = sendSmsService.add_sms(self, sms_content=content, phone=user_phone, create_user=user_id)
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
    return json_a


@view_config(route_name='sendCode', renderer='json')
def send_code(request):
    """
    设备初始化登录
    :param request:
    :return:
    """
    self = request.dbsession
    request.session['12'] = '122'
    request.session['13'] = '133'
    request.session['14'] = '144'
    request.session['14']['timeout'] = 10
