#!/usr/bin/env python37
# -*- coding:utf-8 -*-
# author:Luqueli@wisers.com time:2021/9/7
import pandas as pd
import numpy as np


# 导入对应代码的三张表
def sheet_load(stock: str):
    sheet_type = ['lrb', 'zcfzb', 'xjllb']
    df_list = [pd.read_csv('./all_sheets/' + stock + '_' + f'{sheet_type}.csv', encoding='gbk') for sheet_type in sheet_type]
    lrb_df = df_list[0].T
    zcfzb_df = df_list[1].T
    xjllb_df = df_list[2].T
    return lrb_df, zcfzb_df, xjllb_df


def annul_filter(df):
    """
    将年报数据筛选出来
    :param df:
    :return: df
    """
    cols = list(df.iloc[0,:])
    df = df[df.index.map(lambda x : x[-5:]) == '12-31']
    df.columns = cols
    df = df.where(df!='--', np.nan)
    for col in df.columns:
        df[col] = df[col].astype("float")
    return df


def if_ratio(ratio, standard):
    """

    :param ratio: 比率
    :param standard: 指标
    :return: 判断是否超过指标
    """
    if ratio > standard:
        if_excel = True
    else:
        if_excel = False
    return if_excel


class lrb_quota(object):
    def __init__(self, lrb_df):
        self.lrb = lrb_df

    @property
    def _operating_revenue(self):
        self.operating_revenue = self.lrb['营业收入(万元)']
        return self._operating_revenue

    @property
    def _operating_cost(self):
        self.operating_cost = self.lrb['营业成本(万元)']
        return self._operating_cost


class zcfzb_quota(object):
    def __init__(self, zcfzb_df):
        self.zcfzb = zcfzb_df

    @property
    def _liability_interest(self):
        """

        :return: 有息负债金额
        """
        self.liability_interest = self.zcfzb['长期借款(万元)'] + self.zcfzb['应付债券(万元)'] \
                             + self.zcfzb['一年内到期的非流动负债(万元)'] + self.zcfzb['短期借款(万元)'] + self.zcfzb['交易性金融负债(万元)']
        return self.liability_interest

    @property
    def _total_asset(self):
        """

        :return:资产总结
        """
        self.total_asset = self.zcfzb['资产总计(万元)']
        return self._total_asset

    @property
    def _currency(self):
        """

        :return:货币资金
        """
        self.currency = self.zcfzb['货币资金(万元)']
        return self._currency

    @property
    def _total_debt(self):
        """

        :return:负债合计
        """
        self.total_debt = self.zcfzb['负债合计(万元)']
        return self._total_debt

    @property
    def _inventory(self):
        """

        :return: 存货
        """
        self.inventory = self.zcfzb['存货(万元)']
        return self._inventory

    @staticmethod
    def short_term_debt_crisis_ratio(zcfzb_df):
        """
        短期负债危机 = 货币资金占流动性负债的占比
        :param zcfzb_df:
        :return: 短期负债偿还能力占比
        """
        return zcfzb_df['货币资金(万元)'] / zcfzb_df['流动负债合计(万元)']

    @staticmethod
    def high_currency_ratio(currency, total_asset, high_ratio_standard=.2):
        ratio = currency / total_asset
        if_high = if_ratio(ratio, high_ratio_standard)
        return if_high

    @staticmethod
    def high_debt_asset_ratio(debt , total_asset, high_ratio_standard=.7):
        ratio = debt / total_asset
        if_high = if_ratio(ratio, high_ratio_standard)
        return if_high


class xjllb_quota(object):
    def __init__(self, xjllb_df):
        self.xjllb = xjllb_df


class inter_sheet_compute(object):
    def __init__(self):
        pass

    @staticmethod
    def open_book_credit_income_ratio(open_book_credit, operating_revenue):
        """

        :param open_book_credit: 应收账款
        :param operating_revenue: 营业收入
        :return:对应比例
        """
        return open_book_credit/operating_revenue

    @staticmethod
    def roa(net_profit, total_asset):
        """

        :param net_profit: 净利润
        :param total_asset: 总资产
        :return: ROA 总资产回报率
        """
        return net_profit/total_asset

    @staticmethod
    def roi(net_profit, total_investment):
        """

        :param net_profit: 净利润
        :param total_investment: 总投资额
        :return: 投资回报率
        """
        return net_profit/total_investment

    @staticmethod
    def net_profit_margin(net_profit, operating_revenue):
        """
        盈利能力
        :param net_profit: 净利率
        :param operating_revenue: 营业收入
        :return: 净利率
        """
        return net_profit/operating_revenue

    @staticmethod
    def gross_margin(gross_profit, operating_revenue):
        """
        盈利能力
        :param gross_profit: 毛利率
        :param operating_revenue: 营业收入
        :return: 毛利率
        """
        return gross_profit/operating_revenue

    @staticmethod
    def high_scale_ratio(currency, operating_revenue, standard=1):
        """

        :param currency: 货币资金
        :param operating_revenue:营业收入
        :param standard:
        :return: 是否超标
        """
        ratio = currency / operating_revenue
        if_high = if_ratio(ratio, standard)
        return if_high

    @staticmethod
    def inventory_turnover_ratio(inventory, operating_cost):
        """

        :param inventory: 存货
        :param operating_cost: 营业成本
        :return: 存货周转率
        """
        pass
        avg_inventory = (zcfzb['存货(万元)'][0:-1].values+zcfzb['存货(万元)'][1:].values)/2
        inventory_turnover_ratio = operating_cost[:-1].divide(pd.Series(avg_inventory,index=operating_cost[:-1].index))
        return inventory_turnover_ratio


if __name__ == "__main__":
    lrb, zcfzb, xjllb = sheet_load('601012')
    lrb = annul_filter(lrb)
    zcfzb = annul_filter(zcfzb)
    xjllb = annul_filter(xjllb)
    print('done')
