# -*- coding: utf-8 -*-#
# @Time :2019/4/2210:42
# @Author :xuqiao  
# @Email :1462942304@qq.com
# @File :context.py
import re
from API_7.conmon.read_conf import Config
import configparser
class Loan:
    loan_id=None
def getdata(data):
    d = '#(.*?)#'
    while re.search(d,data):
        data_1 = re.search(d,data)
        data_2 = data_1.group(1)
        try:
            data_3 = Config().getvalue("data",data_2)
        except configparser.NoOptionError as e:
            if hasattr(Loan,data_2):
                data_3 =str(getattr(Loan,data_2))
            else:
                print("如果没有就抛出错误")
                raise e
        data = re.sub(d,data_3,data,count = 1)
    return data
if __name__ == '__main__':
    data_haha = getdata('{"mobilephone":"register_mobilephone","pwd":"#password#","regna":"#name#"}')
    print(data_haha)