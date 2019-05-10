# -*- coding: utf-8 -*-#
# @Time :2019/4/1711:03
# @Author :xuqiao  
# @Email :1462942304@qq.com
# @File :test_login_testcase.py
import unittest
from ddt import ddt,data,unpack
from API_7.conmon.http_request import HttpRquests
from API_7.conmon.read_write_excel import *
from API_7.conmon import cantins
from API_7.conmon.context import getdata
from API_7.conmon.logger import logger
logger = logger(__file__)
@ddt
class Login(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http_request = HttpRquests()
        logger.info("执行用例前的前置工作")
    @data(*ExcelTest(cantins.data_path,"login").read_excel())
    def test_logintest(self,case):
        logger.info("----------------------------------------------------------------")
        logger.info("执行用例开始：{}".format(case.title))
        case.data = getdata(case.data)
        logger.info("请求的数据是：{}".format(case.data))
        res = self.http_request.http_res(case.method,case.url,case.data).text
        try:
            self.assertEqual(case.exp,res)
        except AssertionError as e:
            ExcelTest(cantins.data_path,"login").write_excel(case.case_id+1,res,"FAIL")
            logger.error("测试报错了：{}".format(e))
            raise e
        else:
            ExcelTest(cantins.data_path,"login").write_excel(case.case_id+1,res,"PASS")
        logger.info("测试结束：{}".format(case.title))
        logger.info("----------------------------------------------------------------")
    @classmethod
    def tearDownClass(cls):
        cls.http_request.session_close()
        logger.info("用例执行结束后的后置工作")



