# -*- coding: utf-8 -*-#
# @Time :2019/4/1513:43
# @Author :xuqiao  
# @Email :1462942304@qq.com
# @File :webservice_request.py
from suds.client import Client
from webservice_api.conmon.read_conf import Config
import suds
from webservice_api.conmon.logger import logger
logger = logger(__name__)
class WebApi:
    def __init__(self,url):
        url = Config().getvalue("url","pre_url") + url
        self.client = Client(url)
    def info_api(self,api,data):
        logger.info("测试数据是：{}".format(data))
        if type(data) == str:
            data = eval(data)
        if api.lower() == "sendmcode":
            try:
                return  self.client.service.sendMCode(data)
            except suds.WebFault as e:
                return e.fault
        elif api.lower() == "userregister":
            return self.client.service.userRegister(data)
        elif api.lower() == "verifyuserauth":
            return self.client.service.verifyUserAuth(data)
        elif api.lower() == "bindbankcard":
            return self.client.service.bindBankCard(data)
        else:
            print("你输入的api不正确")
            return None

if __name__ == '__main__':
    url = "http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
    # url = "http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl"
    client = Client(url)
    # data = {"verify_code":"100058","user_id":"张三","channel_id":"1","pwd":123456,"mobile":15511085201,"ip":"192.168.2.223"}
    data = {"uid":"100010496","pay_pwd":"xiaoming123456","mobile":"18811085209","cre_id":"533423195210202766","user_name":"赵同出","cardid":"381525623256235622","bank_type":1001,"bank_name":"中国银行"}
    # data = {"client_ip":"168.12.23","tmpl_id":"1","mobile":"18811085206"}
    res = client.service.bindBankCard(data)

    print(res)




