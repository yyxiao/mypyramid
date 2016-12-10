#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/10
"""
from sqlalchemy.orm import class_mapper
from pyramid.response import Response


def serialize(model):
    """
    Transforms a model into a dictionary which can be dumped to JSON.
    :param model:
    :return:
    """
    # first we get the names of all the columns on your model
    columns = [c.key for c in class_mapper(model.__class__).columns]
    # then we return their values in a dict
    return dict((c, getattr(model, c)) for c in columns)


def other_response(json_a):
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.json = json_a
    return resp
