#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/10/14
"""

from ..models.model import RiskAnswers, RiskQuestion, CustomerRisk
from ..common.constant import STATE_INVALID, STATE_VALID


class RiskService:

    def search_questions(self, dbs):
        ques_list = []
        questions = dbs.query(RiskQuestion.id, RiskQuestion.question_no, RiskQuestion.question_name).all()
        for ques in questions:
            ans_list = self.search_answer(dbs, ques.id)
            ques_dict = dict()
            ques_dict['id'] = ques[0] if ques[0] else ''
            ques_dict['questionNo'] = ques[1] if ques[1] else ''
            ques_dict['questionName'] = ques[2] if ques[2] else ''
            ques_dict['ansList'] = ans_list
            ques_list.append(ques_dict)
        return ques_list

    @staticmethod
    def search_answer(dbs, question_id):
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
