# -*- coding: utf-8 -*-#
# @Time :2019/4/1714:05
# @Author :xuqiao  
# @Email :1462942304@qq.com
# @File :test_invest_testcase.py
import unittest
from API_7.conmon.http_request import *
from API_7.conmon import cantins
from API_7.conmon.read_write_excel import *
from ddt import ddt,data,unpack
from API_7.conmon.context import getdata
from API_7.conmon.do_pymysql import DoMysql
from API_7.conmon.context import Loan
from API_7.conmon.logger import logger
logger = logger(__file__)
@ddt
class BidLoanCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http_request = HttpRquests()
        logger.info("执行用例前的前置工作")
    def setUp(self):
        self.mysql = DoMysql()
    @data(*(ExcelTest(cantins.data_path,"bidLoan").read_excel()))
    def test_bidloan(self,case):
        logger.info("执行用例开始：{}".format(case.title))
        case.data = getdata(case.data)
        case.data = getdata(case.data)
        logger.debug("请求的数据是：{}".format(case.data))
        if case.title == "正常添加项目":
            case.sql = getdata(case.sql)
        if case.title == "正常投标":
            case.sql = getdata(case.sql)
            before_data_1 = self.mysql.fecth_one(eval(case.sql)["sql2"])["leaveamount"]
            logger.info("投标之前的用户余额是：{}".format(before_data_1))

        res = self.http_request.http_res(case.method,case.url,case.data).json()
        try:
            self.assertEqual(str(case.exp),res["code"])
        except AssertionError as e:
            ExcelTest(cantins.data_path, "bidLoan").write_excel(case.case_id+1,res["code"],"FAILD")
            logger.error("测试报错了：{}".format(e))
            raise e
        else:
            ExcelTest(cantins.data_path, "bidLoan").write_excel(case.case_id + 1, res["code"], "PASS")
            if res["msg"] == "加标成功":
                data_new = self.mysql.fecth_one(case.sql)["id"]
                setattr(Loan,"loan_id",data_new)
            if res["msg"] == "竞标成功":
                #投资成功后，校验数据库的数据信息
                after_data_1 = self.mysql.fecth_one(eval(case.sql)["sql1"])["amount"]
                logger.info("用户投资的金额是：{}".format(after_data_1))
                after_data_2 = self.mysql.fecth_one(eval(case.sql)["sql2"])["leaveamount"]
                logger.info("用户投标成功后的余额：{}".format(after_data_2))
                after_data_3 = self.mysql.fecth_one(eval(case.sql)["sql3"])["amount"]
                self.assertEqual(before_data_1-after_data_2,after_data_1)
                self.assertEqual(before_data_1-after_data_2,after_data_3)
        logger.info("测试结束：{}".format(case.title))

    def tearDown(self):
        self.mysql.close_mysql()
    @classmethod
    def tearDownClass(cls):
        cls.session.session_close()
        logger.info("用例执行结束后的后置工作")
