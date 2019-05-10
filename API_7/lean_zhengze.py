# -*- coding: utf-8 -*-#
# @Time :2019/4/2212:41
# @Author :xuqiao  
# @Email :1462942304@qq.com
# @File :lean_zhengze.py
import re
from API_7.conmon.read_conf import Config
data='{"mobilephone":"#mobilephone#","pwd":"#password#","regna":"haha"}'
f = "#(.*?)#"
# res = re.search(f,data)#从任意位置开始找，找到第一个就返回,找到Match就返回对象，没有就返回None
# res_1 = re.findall(f,data)#返回表达式和组里面的内容
# print(res)
# print(res.group(1))#只返回组里面的内容
# print(res_1)
# data_new = re.sub(f,"a",data,count=1)#查找替换，count查找替换的次数
# print(data_new)
#如果匹配多次的内容，继续用data接收
def replace(data):
    f = "#(.*?)#"
    while re.search(f,data):
        m = re.search(f,data)
        data_1 = m.group(1)
        v = Config().getvalue("user_info",data_1)
        data = re.sub(f,v,data,count=1)
    return data