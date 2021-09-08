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


class zcfzb_quota(object):
    def __init__(self, zcfzb_df):
        self.zcfzb = zcfzb_df


class xjllb_quota(object):
    def __init__(self, xjllb_df):
        self.xjllb = xjllb_df


if __name__ == "__main__":
    pass



