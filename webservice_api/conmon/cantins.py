# -*- coding: utf-8 -*-#
# @Time :2019/4/1513:39
# @Author :xuqiao  
# @Email :1462942304@qq.com
# @File :cantins.py
import os
path_1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(path_1,"data","API.xlsx")
car_path = os.path.join(path_1,"conf","districtcode.txt")
print(car_path)
print(data_path)
global_path = os.path.join(path_1,"conf","global.conf")
online_url_path = os.path.join(path_1,"conf","online_url.conf")
test_url_path = os.path.join(path_1,"conf","test_url.conf")
log_path = os.path.join(path_1,"log")
reports_path = os.path.join(path_1,"reports")
case_path = os.path.join(path_1,"testcase")