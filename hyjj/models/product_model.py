#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/18
"""

from sqlalchemy import (
    Column,
    INT,
    VARCHAR,
    Sequence,
    DateTime,
    TEXT
)

from .meta import Other
from datetime import datetime


class City(Other):
    __tablename__ = 'city'                                                              # 测试多数据源多表
    code = Column(VARCHAR(5), primary_key=True)                   # code
    name = Column(VARCHAR(20))                  # name
