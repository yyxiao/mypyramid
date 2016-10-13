#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/13
"""
from pyramid.view import view_config
from ..service.sendsms_service import sendSmsService
from ..common.sendsms import send_sms


@view_config(route_name='sendSms', renderer='json')
def send_sms(request):
    """
    设备初始化登录
    :param request:
    :return:
    """
    self = request.dbsession
    user_id = request.POST.get('user_id', 'sdf')
    phone = request.POST.get('phone', 15800786806)
    content = request.POST.get('content', '尊敬的肖先生，您好，您网上交易重置登录密码验证码为457345，请在三分钟内输入该有效验证码')
    crm_msg = send_sms(phone, content)
    msg = sendSmsService.add_sms(self, sms_content=content, phone=phone, create_user=user_id)

    if msg:
        json_a = {
            'status': False,
            'message': msg
        }
    else:
        json_a = {
            'status': True,
            'message': ''
        }
    return json_a