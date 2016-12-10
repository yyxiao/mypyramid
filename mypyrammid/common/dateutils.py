#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/12
"""
import datetime

date_pattern = '%Y%m%d'  # 日期格式
date_pattern1 = '%Y-%m-%d'  # 日期格式
date_pattern2 = '%Y/%m/%d'  # 日期格式
time_pattern = '%H%M%S'  # 时间模式
datetime_pattern = '%Y%m%d %H%M%S'  # 日期时间模式
datetime_format = '%Y-%m-%d %H:%M:%S' # 标准时间格式

START_QUARTER = '2012-1'


def get_now_quarter():
    '''返回当前季度'''
    dnow = datetime.datetime.now()
    syear = str(dnow.year)
    if (dnow.month >= 1) and (dnow.month <= 3):
        return syear + '-1'
    elif (dnow.month >= 4) and (dnow.month <= 6):
        return syear + '-2'
    elif (dnow.month >= 7) and (dnow.month <= 9):
        return syear + '-3'
    else:
        return syear + '-4'


def get_pre_data_date_quarter(data_date):
    '''返回当前数据日期前一季度'''
    syear = str(data_date[0:4])
    smonth = int(data_date[5:6])
    smonth = smonth - 3
    if (smonth >= 1) and (smonth <= 3):
        return syear + '-1'
    elif (smonth >= 4) and (smonth <= 6):
        return syear + '-2'
    elif (smonth >= 7) and (smonth <= 9):
        return syear + '-3'
    else:
        syear = str(int(syear) - 1)
        return syear + '-4'


def get_welcome():
    ''''''
    dnow = datetime.datetime.now()
    stime = dnow.strftime('%H%M%S')
    if (stime >= '080000') and stime < '120000':
        return '上午好！'
    elif (stime >= '120000') and stime < '140000':
        return '中午好！'
    elif (stime >= '140000') and stime < '180000':
        return '下午好！'
    elif (stime >= '180000') and stime < '240000':
        return '晚上好！'
    else:
        return ''


def date_to_cn(d):
    '''将yyyyMMdd格式的日期转换为"yyyy年MM月dd日"'''
    if d and len(d) == 8:
        return d[0:4] + '年' + d[4:6] + '月' + d[6:] + '日'
    else:
        return ''


def date_now(time_format=datetime_format):
    """
    获取当前时间——用于创建时间
    :return:
    """
    dnow = datetime.datetime.now().strftime(time_format)
    return dnow


# 获取下一天, 日期格式为:yyyyMMdd
def get_next_date(sdate):
    ddate = datetime.datetime.strptime(sdate, date_pattern1)
    rdate = ddate + datetime.timedelta(days=1)
    return rdate.strftime(date_pattern1)


# 获取前一天, 日期格式为:yyyyMMdd
def get_pre_date(sdate):
    ddate = datetime.datetime.strptime(sdate, date_pattern1)
    ddate.weekday()
    rdate = ddate + datetime.timedelta(days=-1)
    return rdate.strftime(date_pattern)


# 获取当前时间某days天, 日期格式为:yyyyMMdd
def get_predate_days(sdate, days, time_format=date_pattern2):
    ddate = datetime.datetime.strptime(sdate, date_pattern1)
    rdate = ddate + datetime.timedelta(days=days)
    return rdate.strftime(time_format)


def get_pre_month_end(sdate):
    '''前一个月最后一天'''
    ddate = datetime.datetime.strptime(sdate[0:6] + '01', date_pattern)
    rdate = ddate + datetime.timedelta(days=-1)
    return rdate.strftime(date_pattern)


def get_weekday(start_date, end_date, weekday_nums, repeat=None):
    """
    获取一段时间范围内每个周天对应的日期
    :param start_date:
    :param end_date:
    :param weekday_nums: list, 星期对应数字 0 ～ 6
    :param repeat:
    :return:
    """

    sdate = datetime.datetime.strptime(start_date, date_pattern1)
    edate = datetime.datetime.strptime(end_date, date_pattern1)

    if not repeat:
        edate += datetime.timedelta(days=1)

    weekdays = []

    for weekday_num in weekday_nums:
        tmp_date = sdate
        while tmp_date < edate:
            now_weekday = tmp_date.weekday()
            tmp_date += datetime.timedelta(days=(((int(weekday_num)+6) % 7 - now_weekday + 7) % 7))
            if tmp_date < edate:
                weekdays.append(tmp_date.strftime(date_pattern1))
                tmp_date += datetime.timedelta(days=7)
            else:
                break
    return weekdays


def add_date(max_period):
    """
    计算用户预定范围使用：日期增加、删除
    :param max_period:
    :return:
    """
    u = datetime.datetime.now().strptime(datetime.datetime.now().strftime(date_pattern1),date_pattern1)
    d = datetime.timedelta(days=max_period)
    t = u + d
    return str(t)


def compare_pad_date(date1, date2):
    if not date1:
        sub_date = 31
    else:
        date0 = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
        date3 = datetime.datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")
        sub_date = round((date3 - date0).seconds/60)+(date3 - date0).days*24*60
    return sub_date
