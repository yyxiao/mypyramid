#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/14
"""

from ..models.model import RiskAnswers, RiskQuestion, CustomerRisk
from ..common.constant import STATE_INVALID, STATE_VALID
from ..common.dateutils import date_now
from ..common.loguntil import HyLog


class RiskService:

    def search_questions(self, dbs):
        ques_list = []
        questions = dbs.query(RiskQuestion.id, RiskQuestion.question_no, RiskQuestion.question_name).all()
        for ques in questions:
            ans_list = self.__search_answer(dbs, ques.id)
            ques_dict = dict()
            ques_dict['id'] = ques[0] if ques[0] else ''
            ques_dict['questionNo'] = ques[1] if ques[1] else ''
            ques_dict['questionName'] = ques[2] if ques[2] else ''
            ques_dict['ansList'] = ans_list
            ques_list.append(ques_dict)
        return ques_list

    @staticmethod
    def __search_answer(dbs, question_id):
        ans_list = []
        answers = dbs.query(RiskAnswers.id, RiskAnswers.question_id, RiskAnswers.answer_name, RiskAnswers.selection_no)\
            .filter(RiskAnswers.question_id == question_id).all()
        for ans in answers:
            ans_dict = dict()
            ans_dict['id'] = ans[0] if ans[0] else ''
            ans_dict['question_id'] = ans[1] if ans[1] else ''
            ans_dict['answer_name'] = ans[2] if ans[2] else ''
            ans_dict['selection_no'] = ans[3] if ans[3] else ''
            ans_list.append(ans_dict)
        return ans_list

    @staticmethod
    def add_risk_assess(dbs, wechat_id, risk_answers, indiinst_flag, cert_type, cert_no, create_user='xyy'):
        # TODO 调用接口，并评测风险等级
        risk_answer_list = risk_answers.split(',')
        score = 0
        for ans in risk_answer_list:
            score += int(ans)
        try:
            customer_risk = CustomerRisk()
            customer_risk.cust_answers = risk_answers
            customer_risk.cust_id = wechat_id
            customer_risk.evaluating_time = date_now()
            customer_risk.score = score
            customer_risk.state = STATE_VALID
            customer_risk.create_user = create_user
            customer_risk.create_time = date_now()
            dbs.add(customer_risk)
            dbs.flush()
            return ''
        except Exception as e:
            HyLog.log_error(e)
            return '添加评测信息失败，请重试！'

    @staticmethod
    def search_customer_risk_level(dbs, customer_id):
        customer_risk = dbs.query(CustomerRisk.risk_level).filter(CustomerRisk.cust_id == customer_id).first()
        risk_level = customer_risk[0] if customer_risk[0] else ''
        return risk_level
