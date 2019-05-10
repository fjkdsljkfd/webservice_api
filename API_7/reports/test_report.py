# -*- coding: utf-8 -*-#
# @Time :2019/4/1516:42
# @Author :xuqiao  
# @Email :1462942304@qq.com
# @File :test_report.py
from API_7.testcase import test_register_testcase
from API_7.testcase import test_invest_testcase
from API_7.testcase import test_recharge_testcase
from API_7.testcase import test_login_testcase
import unittest
import HTMLTestRunner
suite = unittest.TestSuite()
loader = unittest.TestLoader()
suite.addTest(loader.loadTestsFromModule(test_recharge_testcase))
suite.addTest(loader.loadTestsFromModule(test_invest_testcase))
suite.addTest(loader.loadTestsFromModule(test_login_testcase))
with open("report.html","wb")as file:
    runner = HTMLTestRunner.HTMLTestRunner(stream=file, verbosity=2, title="这是一个测试用例", description="三个功能的测试用例")
    runner.run(suite)
