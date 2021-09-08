#!/usr/bin/env python37
# -*- coding:utf-8 -*-
# author:Luqueli@wisers.com time:2021/9/7
import pandas as pd


#导入对应代码的三张表
def sheet_load(stock):
    for sheet_type in ['lrb', 'zcfzb', 'xjllb']:
        file_path = './all_sheets/' + stock + '_' + f'{sheet_type}.csv'
        if sheet_type == 'lrb':
            lrb_df = pd.read_csv(file_path)
        if sheet_type == 'zcfzb':
            zcfzb_df = pd.read_csv(file_path)
        if sheet_type == 'xjllb':
            xjllb_df = pd.read_csv(file_path)
    return lrb_df, zcfzb_df, xjllb_df


class lrb_quota(object):
    def __init__(self, lrb_df):
        self.lrb = lrb_df

    @property
    def income(self):
        self.income = self.lrb['营业收入(万元)']
        return self.income


class zcfzb_quota(object):
    def __init__(self, zcfzb_df):
        self.zcfzb = zcfzb_df

    @staticmethod
    def short_term_debt_crisis(zcfzb_df):
        '''
        短期负债危机 = 货币资金占流动性负债的占比
        :param zcfzb_df:
        :return: 短期负债偿还能力占比
        '''
        return zcfzb_df['货币资金(万元)']/zcfzb_df['流动负债合计(万元)']

    @property
    def _liability_interest(self):
        '''

        :return: 有息负债金额
        '''
        self.liability_interest = self.zcfzb['长期借款(万元)'] + self.zcfzb['应付债券(万元)'] \
                             + self.zcfzb['一年内到期的非流动负债(万元)'] + self.zcfzb['短期借款(万元)'] + self.zcfzb['交易性金融负债(万元)']
        return self.liability_interest


class xjllb_quota(object):
    def __init__(self, xjllb_df):
        self.xjllb = xjllb_df


class inter_sheet_compute(object):
    def __init__(self):
        pass

    @staticmethod
    def open_book_credit_income_ratio(open_book_credit, income):
        '''

        :param open_book_credit: 应收账款
        :param income: 营业收入
        :return:对应比例
        '''
        return open_book_credit/income




if __name__ == "__main__":
    pass



