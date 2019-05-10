# -*- coding: utf-8 -*-#
# @Time :2019/4/1514:57
# @Author :xuqiao  
# @Email :1462942304@qq.com
# @File :test_register_testcase.py
import unittest
from API_7.conmon.read_write_excel import *
from API_7.conmon.http_request import HttpRquests
from API_7.conmon import cantins
from ddt import ddt,data,unpack
from API_7.conmon.do_pymysql import DoMysql
from API_7.conmon.context import getdata
from API_7.conmon.logger import logger
logger = logger(__file__)
@ddt
class RegisterTestcase(unittest.TestCase):
    doexcel = ExcelTest(cantins.data_path, "register")
    case = doexcel.read_excel()
    @classmethod
    def setUpClass(cls):
        cls.session = HttpRquests()
        logger.info("执行用例前的前置工作")
    def setUp(self):
        self.mysql = DoMysql()
    @data(*case)
    def test_register(self,case):
        print("开始执行测试用例：",case.title)
        if case.data.find("register_mobilephone")>-1:
            if case.sql:
                data = eval(case.sql)
                res_data = self.mysql.fecth_one(data["sql1"])
                logger.info("读取数据库里面的最大的手机号是：{}".format(res_data))
                data_2 = str(int(res_data["max(mobilephone)"])+1)
                case.data = case.data.replace("register_mobilephone",data_2)
                logger.info("变成最新的手机号：{}".format(case.data))
        case.data = getdata(case.data)
        logger.debug("测试数据是：{}".format(case.data))
        res = self.session.http_res(case.method,case.url,case.data).json()
        try:
            self.assertEqual(str(case.exp),res["code"])
        except AssertionError as e:
            self.doexcel.write_excel(case.case_id + 1, res["code"], "FIAL")
            logger.error("测试出错了：{}".format(e))
            raise e
        else:
            self.doexcel.write_excel(case.case_id + 1, res["code"], "PASS")
            if res["msg"] == "注册成功":
                after = self.mysql.fecth_one("select mobilephone from future.member where mobilephone = {}".format(eval(case.data)["mobilephone"]))
                self.assertEqual(eval(case.data)["mobilephone"],after["mobilephone"])
        logger.info("测试结束：{}".format(case.title))
    def tearDown(self):
        self.mysql.close_mysql()
    @classmethod
    def tearDownClass(cls):
        cls.session.session_close()
        logger.info("测试结束后的后置工作")
