#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/14
"""

import redis


def create_redis(redis_host='127.0.0.1'):
    pool = redis.ConnectionPool(host=redis_host, port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    return r
