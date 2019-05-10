from webservice_api.conmon.logger import logger
from webservice_api.conmon import cantins
from webservice_api.conmon.random_carid import RandomCarid
from webservice_api.conmon.do_pymysql import DoMysql
from webservice_api.conmon.read_write_excel import ExcelTest
from webservice_api.conmon.context import *
from webservice_api.conmon.webservice_request import WebApi
from webservice_api.conmon.random_name import random_name
logger = logger(__name__)
from ddt import ddt,data,unpack
import unittest
@ddt
class VerifyAuthcase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("测试前的前置工作")
    @data(*ExcelTest(cantins.data_path,"verifyUserAuth").read_excel())
    def test_verfyauthcase(self,case):
        logger.info("开始执行:{}".format(case.title))
        logger.info("--------------------")
        if case.data.find("user_name") > -1:
            name = random_name()
            case.data = case.data.replace("user_name",name)
            logger.info(case.data)  # {"uid":"#uid#","true_name":"周已相","cre_id":"card_number"}
        if case.data.find("card_number") > -1:
            logger.info(case.data)
            car_id = RandomCarid().gennerator()
            logger.info(car_id)
            case.data = case.data.replace("card_number",car_id)
            logger.info(case.data)
        case.data = getdata(case.data)
        res = WebApi(case.url).info_api(case.api,case.data)
        logger.info("请求接口后得到的数据：{}".format(res))
        try:
            if case.title == "身份认证通过":
                self.assertEqual(str(case.exp),res["retCode"])
                ExcelTest(cantins.data_path, "verifyUserAuth").write_excel(case.case_id+1,eval(res["retCode"]),"pass")
                #断言数据库中的数据
                if case.sql:
                    case.sql = getdata(case.sql)
                    after = DoMysql().fecth_one(eval(case.sql)["sql"])
                    self.assertIsNotNone(name,after["Ftrue_name"])
                    after_2 = DoMysql().fecth_one(eval(case.sql)["sql2"])
                    self.assertEqual(1,int(after_2["count(*)"]))
            else:
                self.assertEqual(case.exp,res["retInfo"])
                ExcelTest(cantins.data_path, "verifyUserAuth").write_excel(case.case_id + 1, str(res["retInfo"]),"pass")
        except AssertionError as e:
            if case.title == "身份认证通过":
                ExcelTest(cantins.data_path, "verifyUserAuth").write_excel(case.case_id + 1, eval(res["retCode"]), "failed")
            else:
                ExcelTest(cantins.data_path, "verifyUserAuth").write_excel(case.case_id + 1, str(res["retInfo"]),"pass")
            logger.error("报错了：{}".format(e))
            raise e
        logger.info("{}用例执行完成".format(case.title))
    @classmethod
    def tearDownClass(cls):
        logger.info("用例执行结束的后置工作")
