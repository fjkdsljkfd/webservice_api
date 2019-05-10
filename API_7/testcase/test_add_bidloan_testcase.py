# -*- coding: utf-8 -*-#
# @Time :2019/4/1716:11
# @Author :xuqiao  
# @Email :1462942304@qq.com
# @File :test_add_bidloan_testcase.py
import unittest
from API_7.conmon.http_request import HttpRquests
from API_7.conmon.read_write_excel import *
from ddt import ddt,data,unpack
from API_7.conmon import cantins
from API_7.conmon.context import *
from API_7.conmon.do_pymysql import DoMysql
from API_7.conmon.logger import logger
logger = logger(__file__)
@ddt
class AddBidloan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http_request = HttpRquests()
        logger.info("执行用例前的前置工作")
    def setUp(self):
        self.mysql = DoMysql()
    @data(*ExcelTest(cantins.data_path,"addbidloan").read_excel())
    def test_add_bid(self,case):
        logger.info("执行用例开始：{}".format(case.title))
        case.data = getdata(case.data)
        logger.debug("请求的数据是：{}".format(case.data))
        if case.sql:
            case.sql = getdata(case.sql)
            before_data = self.mysql.fecth_one(case.sql)["id"]
            logger.info("添加项目前查询到的id:{}".format(before_data))
        res = self.http_request.http_res(case.method,case.url,case.data).json()
        try:
            self.assertEqual(str(case.exp),res["code"])
        except AssertionError as e:
            ExcelTest(cantins.data_path, "addbidloan").write_excel(case.case_id+1,res["code"],"FAILD")
            logger.error("测试报错了：{}".format(e))
            raise e
        else:
            ExcelTest(cantins.data_path, "addbidloan").write_excel(case.case_id + 1, res["code"], "PASS")
            if res["msg"] == "加标成功":
                data_new = self.mysql.fecth_one(case.sql)["id"]
                self.assertNotEqual(before_data,data_new)
        logger.info("测试结束：{}".format(case.title))
    def tearDown(self):
        self.mysql.close_mysql()
    @classmethod
    def tearDownClass(cls):
        cls.http_request.session_close()
        logger.info("用例执行结束后的后置工作")
