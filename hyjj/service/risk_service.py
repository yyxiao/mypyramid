#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/14
"""

from ..models.model import RiskAnswers, RiskQuestion, CustomerRisk
from ..common.constant import STATE_VALID, QUESTION_USER, QUESTION_ORG, \
    RISK_FIRST, RISK_SECOND, RISK_THIRD, RISK_MSG, RISK_TYPE_LEVEL
from ..common.dateutils import date_now
from ..common.loguntil import HyLog


class RiskService:

    def search_questions(self, dbs, type):
        ques_list = []
        questions = dbs.query(RiskQuestion.id, RiskQuestion.question_name)\
            .filter(RiskQuestion.state == STATE_VALID).filter(RiskQuestion.question_type == type)\
            .order_by(RiskQuestion.id).all()
        for ques in questions:
            ans_list = self.__search_answers(dbs, ques.id)
            ques_dict = dict()
            ques_dict['id'] = ques[0] if ques[0] else ''
            ques_dict['questionName'] = ques[1] if ques[1] else ''
            ques_dict['ansList'] = ans_list
            ques_list.append(ques_dict)
        HyLog.log_info(ques_list)
        return ques_list

    @staticmethod
    def __search_answers(dbs, question_id):
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

    def add_risk_assess(self, dbs, wechat_id, risk_answers, type, cert_type, cert_no, create_user='xyy'):
        # TODO 调用接口保存用户证件类型、号码
        risk_answer_dict = eval(risk_answers)
        score = 0  # 评测得分
        risk_type = RISK_FIRST
        for i, v in risk_answer_dict.items():
            score += self.__search_answer_score(dbs, i, v)
        if type == QUESTION_USER:
            if score <= 34:
                risk_type = RISK_FIRST
            elif 66 >= score >= 35:
                risk_type = RISK_SECOND
            elif score >= 67:
                risk_type = RISK_THIRD
        else:
            if score <= 10:
                risk_type = RISK_FIRST
            elif 20 >= score >= 11:
                risk_type = RISK_SECOND
            elif score >= 21:
                risk_type = RISK_THIRD
        try:
            customer_risk = CustomerRisk()
            customer_risk.cust_answers = risk_answers
            customer_risk.cust_id = wechat_id
            customer_risk.evaluating_time = date_now()
            customer_risk.score = score
            customer_risk.risk_level = risk_type
            customer_risk.state = STATE_VALID
            customer_risk.create_user = create_user
            customer_risk.create_time = date_now()
            dbs.add(customer_risk)
            dbs.flush()
        except Exception as e:
            HyLog.log_error(e)
        return risk_type

    @staticmethod
    def search_customer_risk_level(dbs, customer_id):
        error_msg = ''
        risk_level = '00'
        riskType = ''
        customer_risk = dbs.query(CustomerRisk.risk_level)\
            .filter(CustomerRisk.cust_id == customer_id).order_by(CustomerRisk.create_time.desc()).first()
        if customer_risk:
            risk_level = customer_risk[0] if customer_risk[0] else ''
        else:
            error_msg = '该用户未进行风险评测！'
        risk_msg = RISK_MSG[risk_level]
        risk_type_level = RISK_TYPE_LEVEL[risk_level]
        return error_msg, risk_level, risk_msg, risk_type_level

    @staticmethod
    def __search_answer_score(dbs, question_id, selection_no):
        ans = dbs.query(RiskAnswers.score).filter(RiskAnswers.question_id == question_id)
        if selection_no:
            ans = ans.filter(RiskAnswers.selection_no == selection_no)
        ans = ans.first()
        if not ans:
            return 0
        return ans[0]
