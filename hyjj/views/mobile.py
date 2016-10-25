#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/13
"""
from pyramid.view import view_config
from ..common.sendsms import send
from ..common import constant
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
            code = self.sendSmsService.make_random(6)
            content = constant.SMS_DESC % (user_name, code)
            redis_host = self.request.registry.settings['redis.sessions.host']
            r = create_redis(redis_host)
            num = r.get(self.request.client_addr)
            num = int(num) if num else 0
            if num <= 9:
                self.sendSmsService.add_code_redis(user_phone, code, redis_host)
                self.sendSmsService.add_ip_no_redis(self.request.client_addr, num + 1, redis_host)
                send(user_phone, content)
                error_msg = self.sendSmsService.add_sms(dbs, sms_content=content, phone=user_phone)
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
        self.hyLog.log_in(self.request.client_addr, '', ('sendCode failed ' +
                                                         error_msg if error_msg else 'sendCode success'), 'mobile')
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
        dbs = self.request.dbsession
        error_code = constant.CODE_ERROR
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
                self.customerService.add_customer(dbs, cust_id='a', openid=wechat_id, indiinst_flag='a', cust_name='b',
                                                  phone=user_phone, risk_level=1)
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
        self.hyLog.log_in(self.request.client_addr, '', ('accountBinding failed ' + error_msg if error_msg
                                                         else 'sendCode success'), 'mobile')
        resp = other_response(json_a=json_a)
        return resp

    @view_config(route_name='riskQuestion', renderer='json')
    def risk_question(self):
        """
        风险题目查询
        :param self:
        :return:
        """
        error_msg = ''
        dbs = self.request.dbsession
        wechat_id = self.request.POST.get('wechatId', '')
        type = self.request.POST.get('type', '0')
        if not wechat_id:
            error_msg = '用户wechat_id不能为空！'
        if not error_msg:
            questions = self.riskService.search_questions(dbs, type)
        if error_msg:
            json_a = {
                'returnCode': constant.CODE_ERROR,
                'returnMsg': error_msg
            }
        else:
            json_a = {
                'returnCode': constant.CODE_SUCCESS,
                'returnMsg': '',
                'questionList': questions
            }
        self.hyLog.log_in(self.request.client_addr, '',
                          ('riskQuestion failed ' + error_msg if error_msg else 'riskQuestion success'),
                          'mobile')
        resp = other_response(json_a=json_a)
        return resp

    @view_config(route_name='riskAssess', renderer='json')
    def risk_assess(self):
        """
        风险评估
        :param self:
        :return:
        """
        error_msg = ''
        dbs = self.request.dbsession
        wechat_id = self.request.POST.get('wechatId', '')
        risk_answers = self.request.POST.get('riskAnswer', '')
        type = self.request.POST.get('type', '')
        cert_type = self.request.POST.get('certType', '')
        cert_no = self.request.POST.get('certNo', '')
        if not wechat_id:
            error_msg = '用户wechat_id不能为空！'
        elif not risk_answers:
            error_msg = '风险题目答案！'
        elif not type:
            error_msg = '对私对公标志不能为空！'
        if not error_msg:
            risk_level = self.riskService.add_risk_assess(dbs, wechat_id, risk_answers,
                                                          type, cert_type, cert_no)
        if error_msg:
            json_a = {
                'returnCode': constant.CODE_ERROR,
                'returnMsg': error_msg
            }
        else:
            json_a = {
                'returnCode': constant.CODE_SUCCESS,
                'returnMsg': '',
                'riskLevel': risk_level
            }
        self.hyLog.log_in(self.request.client_addr, '',
                          ('riskAssess failed ' + error_msg if error_msg else 'riskAssess success'),
                          'mobile')
        resp = other_response(json_a=json_a)
        return resp

    @view_config(route_name='riskSearch', renderer='json')
    def risk_search(self):
        """
        风险评估查询
        :param self:
        :return:
        """
        error_msg = ''
        dbs = self.request.dbsession
        wechat_id = self.request.POST.get('wechatId', '')
        if not wechat_id:
            error_msg = '用户wechat_id不能为空！'
        if not error_msg:
            error_msg, risk_level, risk_msg, risk_type_level = self.riskService.search_customer_risk_level(dbs, wechat_id)
        if error_msg:
            json_a = {
                'returnCode': constant.CODE_ERROR,
                'returnMsg': error_msg
            }
        else:
            json_a = {
                'returnCode': constant.CODE_SUCCESS,
                'returnMsg': '',
                'riskLevel': risk_level,
                'riskMessage': risk_msg,
                'riskType': risk_type_level
            }
        self.hyLog.log_in(self.request.client_addr, '',
                          ('riskSearch failed ' + error_msg if error_msg else 'riskSearch success'),
                          'mobile')
        resp = other_response(json_a=json_a)
        return resp

    @view_config(route_name='navList', renderer='json')
    def nav_list(self):
        """
        风险评估净值走势
        :param self:
        :return:
        """
        error_msg = ''
        dbms = self.request.mysqldbsession
        wechat_id = self.request.POST.get('wechatId', '')
        pro_id = self.request.POST.get('productId', '')
        nav_type = self.request.POST.get('navType', 1)
        if not wechat_id:
            error_msg = '用户wechat_id不能为空！'
        elif not pro_id:
            error_msg = '产品id不能为空！'
        elif not nav_type:
            error_msg = '净值走势类型不能为空！'
        if not error_msg:
            nav_list = self.productService.search_navs(dbms, wechat_id, pro_id, nav_type)
        if error_msg:
            json_a = {
                'returnCode': constant.CODE_ERROR,
                'returnMsg': error_msg
            }
        else:
            json_a = {
                'returnCode': constant.CODE_SUCCESS,
                'returnMsg': '',
                'navList': nav_list
            }
        self.hyLog.log_in(self.request.client_addr, '',
                          ('navList failed ' + error_msg if error_msg else 'navList success'),
                          'mobile')
        resp = other_response(json_a=json_a)
        return resp

    @view_config(route_name='productList', renderer='json')
    def product_list(self):
        """
        查找产品列表
        :param self:
        :return:
        """
        error_msg = ''
        dbms = self.request.mysqldbsession
        wechat_id = self.request.POST.get('wechatId', '')
        page_no = self.request.POST.get('pageNo', 0)
        search_key = self.request.POST.get('searchKey', '')
        if not wechat_id:
            error_msg = '用户wechat_id不能为空！'
        elif not page_no:
            error_msg = '页码不能为空！'
        if not error_msg:
            pro_list = self.productService.search_products(dbms, wechat_id, page_no, search_key)
        if error_msg:
            json_a = {
                'returnCode': constant.CODE_ERROR,
                'returnMsg': error_msg
            }
        else:
            json_a = {
                'returnCode': constant.CODE_SUCCESS,
                'returnMsg': '',
                'productList': pro_list
            }
        self.hyLog.log_in(self.request.client_addr, '',
                          ('productList failed ' + error_msg if error_msg else 'productList success'),
                          'mobile')
        resp = other_response(json_a=json_a)
        return resp

    @view_config(route_name='productDetail', renderer='json')
    def product_detail(self):
        """
        查找产品详情
        :param self:
        :return:
        """
        error_msg = ''
        dbs = self.request.dbsession
        dbms = self.request.mysqldbsession
        wechat_id = self.request.POST.get('wechatId', '')
        product_id = self.request.POST.get('productId', 0)
        if not wechat_id:
            error_msg = '用户wechat_id不能为空！'
        elif not product_id:
            error_msg = '产品ID不能为空！'
        if not error_msg:
            product = self.productService.search_product_info(dbs, dbms, wechat_id, product_id)
        if error_msg:
            json_a = {
                'returnCode': constant.CODE_ERROR,
                'returnMsg': error_msg
            }
        else:
            json_a = {
                'returnCode': constant.CODE_SUCCESS,
                'returnMsg': '',
                'product': product
            }
        self.hyLog.log_in(self.request.client_addr, '',
                          ('productDetail failed ' + error_msg if error_msg else 'productDetail success'),
                          'mobile')
        resp = other_response(json_a=json_a)
        return resp

    @view_config(route_name='productCollect', renderer='json')
    def product_collect(self):
        """
        产品收藏
        :param self:
        :return:
        """
        error_msg = ''
        dbs = self.request.dbsession
        wechat_id = self.request.POST.get('wechatId', '')
        product_id = self.request.POST.get('productId', 0)
        if not wechat_id:
            error_msg = '用户wechat_id不能为空！'
        elif not product_id:
            error_msg = '产品ID不能为空！'
        if not error_msg:
            coll_state = self.customerService.collect_product_by_id(dbs, wechat_id, product_id)
        if error_msg:
            json_a = {
                'returnCode': constant.CODE_ERROR,
                'returnMsg': error_msg
            }
        else:
            json_a = {
                'returnCode': constant.CODE_SUCCESS,
                'returnMsg': '',
                'isCollect': coll_state
            }
        self.hyLog.log_in(self.request.client_addr, '',
                          ('productCollect failed ' + error_msg if error_msg else 'productCollect success'),
                          'mobile')
        resp = other_response(json_a=json_a)
        return resp

    @view_config(route_name='productBook', renderer='json')
    def product_book(self):
        """
        产品预约
        :param self:
        :return:
        """
        error_msg = ''
        dbs = self.request.dbsession
        wechat_id = self.request.POST.get('wechatId', '')
        product_id = self.request.POST.get('productId', 0)
        phone = self.request.POST.get('phone', 0)
        if not wechat_id:
            error_msg = '用户wechat_id不能为空！'
        elif not product_id:
            error_msg = '产品ID不能为空！'
        elif not phone:
            error_msg = '联系电话不能为空！'
        if not error_msg:
            coll_state = self.customerService.book_product_by_id(dbs, wechat_id, product_id, phone)
        if error_msg:
            json_a = {
                'returnCode': constant.CODE_ERROR,
                'returnMsg': error_msg
            }
        else:
            json_a = {
                'returnCode': constant.CODE_SUCCESS,
                'returnMsg': '',
                'isCollect': coll_state
            }
        self.hyLog.log_in(self.request.client_addr, '',
                          ('productCollect failed ' + error_msg if error_msg else 'productCollect success'),
                          'mobile')
        resp = other_response(json_a=json_a)
        return resp

    @view_config(route_name='myCollect', renderer='json')
    def my_collect(self):
        """
        我的收藏
        :param self:
        :return:
        """
        error_msg = ''
        dbms = self.request.mysqldbsession
        dbs = self.request.dbsession
        wechat_id = self.request.POST.get('wechatId', '')
        page_no = self.request.POST.get('pageNo', 0)
        if not wechat_id:
            error_msg = '用户wechat_id不能为空！'
        if not error_msg:
            pro_col_list = self.customerService.search_coll_product(dbs, dbms, wechat_id, page_no)
        if error_msg:
            json_a = {
                'returnCode': constant.CODE_ERROR,
                'returnMsg': error_msg
            }
        else:
            json_a = {
                'returnCode': constant.CODE_SUCCESS,
                'returnMsg': '',
                'productList': pro_col_list
            }
        self.hyLog.log_in(self.request.client_addr, '',
                          ('myCollect failed ' + error_msg if error_msg else 'myCollect success'),
                          'mobile')
        resp = other_response(json_a=json_a)
        return resp
