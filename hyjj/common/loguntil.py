#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016-10-14
"""

import logging


class HyLog(object):
    operator_logger = logging.getLogger(__name__)

    @staticmethod
    def log_in(ip, msg='', client='web'):
        HyLog.log_info('[login]['+client+'] ip:' + ip + ' login ' + msg + '.')

    @staticmethod
    def log_out(ip, user_account, client='web'):
        HyLog.log_info(('[logout]['+client+'] ip:' + ip + ' \"' + user_account + '\" logout.'))

    @staticmethod
    def log_access(ip, user_account, url, client='web'):
        HyLog.log_info('[access]['+client+'] ip:' + ip + ' \"' + user_account + '\" accessed ' + url)

    @staticmethod
    def log_research(ip, user_account, msg='', research_type='', client='web'):
        HyLog.log_info('[research]['+client+'][' + research_type + '] ip:' + ip + ' \"' + user_account + '\"' + msg)

    @staticmethod
    def log_add(ip, user_account, msg='', add_type='', client='web'):
        HyLog.log_info('[add]['+client+'][' + add_type + '] ip:' + ip + ' \"' + user_account + '\"' + msg)

    @staticmethod
    def log_update(ip, user_account, msg='', update_type='', client='web'):
        HyLog.log_info('[update]['+client+'][' + update_type + '] ip:' + ip + ' \"' + user_account + '\"' + msg)

    @staticmethod
    def log_delete(ip, user_account, msg='', delete_type='', client='web'):
        HyLog.log_info('[delete]['+client+'][' + delete_type + '] ip:' + ip + ' \"' + user_account + '\"' + msg)

    @staticmethod
    def log_auth(ip, user_account, authed_user, authority, auth_type, client='web'):
        HyLog.log_info('[auth]['+client+'][' + auth_type + '] ip:' + ip + ' \"' + user_account + '\" licensed to \"' + authed_user + '\" with authority:' + authority)

    @staticmethod
    def log_error(msg):
        HyLog.operator_logger.error(msg)

    @staticmethod
    def log_warn(msg):
        HyLog.operator_logger.warn(msg)

    @staticmethod
    def log_info(msg):
        HyLog.operator_logger.info(msg)
