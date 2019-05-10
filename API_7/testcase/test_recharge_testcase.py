# -*- coding: utf-8 -*-#
# @Time :2019/4/2413:38
# @Author :xuqiao  
# @Email :1462942304@qq.com
# @File :test_recharge_testcase.py
import unittest
from API_7.conmon.do_pymysql import DoMysql
from API_7.conmon import cantins
from API_7.conmon.read_write_excel import *
from API_7.conmon.context import getdata
from API_7.conmon.http_request import HttpRquests
from ddt import ddt,data,unpack
from API_7.conmon.logger import logger
logger = logger(__file__)
@ddt
class Recharge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = HttpRquests()
        logger.info("执行用例前的前置工作")
    def setUp(self):
        self.mysql = DoMysql()
    @data(*ExcelTest(cantins.data_path,"recharge").read_excel())
    def test_recharge(self,case):
        logger.info("执行用例开始：{}".format(case.title))
        case.data = getdata(case.data)
        logger.debug("请求的数据是：{}".format(case.data))
        if case.sql:
            case.sql = getdata(case.sql)
            before_data = self.mysql.fecth_one(eval(case.sql)["sql1"])["leaveamount"]
            logger.info("用户充值之前的余额是：{}".format(before_data))
        res = self.session.http_res(case.method,case.url,case.data).json()
        try:
            self.assertEqual(str(case.exp),res["code"])
            ExcelTest(cantins.data_path, "recharge").write_excel(case.case_id+1,res["code"],"PASS")
            if res["msg"] == "充值成功":
                after_data = self.mysql.fecth_one(eval(case.sql)["sql1"])["leaveamount"]
                logger.info("充值之后用户的余额是：".format(after_data))
                self.assertEqual(before_data + eval(case.data)["amount"],after_data)
                financelog_data = self.mysql.fecth_one(eval(case.sql)["sql2"])
                logger.info(financelog_data["incomemembermoney"])
                self.assertEqual(after_data, financelog_data["incomemembermoney"])
        except AssertionError as e:
            ExcelTest(cantins.data_path, "recharge").write_excel(case.case_id + 1, res["code"], "FILE")
            logger.error("测试报错了：{}".format(e))
            raise e
        logger.info("测试结束：{}".format(case.title))
    def tearDown(self):
        self.mysql.close_mysql()
    @classmethod
    def tearDownClass(cls):
        cls.session.session_close()
        logger.info("用例执行结束后的后置工作")
