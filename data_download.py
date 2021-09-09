#!/usr/bin/env python37
# -*- coding:utf-8 -*-
# author:Luqueli@wisers.com time:2021/9/7

import urllib.request
import pandas as pd
from time import sleep
import os


def sheet_load(stock_num: list, sheet_type: str):
    for stock in stock_num:
        url = f'http://quotes.money.163.com/service/{sheet_type}_' + stock + '.html'
        while True:
            try:
                content = urllib.request.urlopen(url, timeout=2).read()
                # content = content.decode("gbk").encode("utf-8")
                file_path = './all_sheets/' + stock + '_' + f'{sheet_type}.csv'
                if not os.path.isfile(file_path):
                    empty_df = pd.DataFrame()
                    empty_df.to_csv(file_path)
                with open(file_path, 'wb') as f:
                    f.write(content)
                print(stock + '_' + f'{sheet_type}' + "更新完成")
                sleep(1)
                break
            except Exception as e:
                if str(e) == 'HTTP Error 404: Not Found':
                    break
                else:
                    print(e)
                    continue


if __name__ == "__main__":
    stock_no = ['601012', '002027', '002304']
    for sheet_ty in ['lrb', 'xjllb', 'zcfzb']:
        sheet_load(stock_no, sheet_ty)
