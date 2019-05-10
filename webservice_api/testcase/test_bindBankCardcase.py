from webservice_api.conmon.logger import logger
from webservice_api.conmon.webservice_request import WebApi
from webservice_api.conmon.read_write_excel import ExcelTest
from webservice_api.conmon import cantins
from ddt import ddt,data,unpack
import unittest
logger = logger(__name__)
@ddt
class BindBankCard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("用例执行前置工作")
    @data(*ExcelTest(cantins.data_path,"bindBankCard").read_excel())
    def test_bindBankCard(self,case):
        logger.info("开始执行测试用例：{}".format(case.title))
        res = WebApi(case.url).info_api(case.api,case.data)
        try:
            self.assertEqual(case.exp,res["retInfo"])
            ExcelTest(cantins.data_path,"bindBankCard").write_excel(case.case_id+1,str(res["retInfo"]),"pass")
        except AssertionError as e:
            ExcelTest(cantins.data_path,"bindBankCard").write_excel(case.case_id+1,str(res["retInfo"]),"failed")
            logger.error("报错了：{}".format(e))
            raise e
        logger.info("{}用例执行完成".format(case.title))
    @classmethod
    def tearDownClass(cls):
        logger.info("用例执行结束的后置工作")
