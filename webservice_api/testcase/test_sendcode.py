from webservice_api.conmon.webservice_request import *
from webservice_api.conmon.logger import logger
from webservice_api.conmon.do_pymysql import DoMysql
from webservice_api.conmon import cantins
from webservice_api.conmon.read_write_excel import *
import unittest
from ddt import ddt,data,unpack
logger = logger(__name__)
@ddt
class Sendcode(unittest.TestCase):
    data_1 = ExcelTest(cantins.data_path,"sendcode").read_excel()
    @classmethod
    def setUpClass(cls):
        logger.info("执行用例的前置工作")
    @data(*data_1)
    def test_sendcode(self,case):
        logger.info("开始执行测试用例：{}".format(case.title))
        res = WebApi(case.url).info_api(case.api,case.data)
        logger.info("请求接口返回的结果：{}".format(res))
        logger.info("得到的数据是：{}".format(res))
        try:
            if case.exp == 0:
                self.assertEqual(str(case.exp),res["retCode"])
                ExcelTest(cantins.data_path,"sendcode").write_excel(case.case_id+1,eval(res["retCode"]),"pass")
            else:
                self.assertEqual(case.exp, res["faultstring"])
                ExcelTest(cantins.data_path, "sendcode").write_excel(case.case_id + 1, str(res["faultstring"]), "pass")
        except AssertionError as e:
            if case.exp == 0:
                ExcelTest(cantins.data_path, "sendcode").write_excel(case.case_id + 1, eval(res["retCode"]), "filed")
            else:
                ExcelTest(cantins.data_path, "sendcode").write_excel(case.case_id + 1, str(res["faultstring"]), "filed")
            logger.error("报错了：{}".format(e))
            raise e
        logger.info("{}:用例执行结束".format(case.title))
    @classmethod
    def tearDownClass(cls):
        logger.info("用例执行结束的后置工作")
