from webservice_api.conmon.webservice_request import WebApi
from webservice_api.conmon.logger import logger
from webservice_api.conmon import cantins
from webservice_api.conmon.context import *
from webservice_api.conmon.read_write_excel import *
from ddt import ddt,data,unpack
from webservice_api.conmon.do_pymysql import DoMysql
from webservice_api.conmon.random_phone import create_phone
from webservice_api.conmon.random_name import random_name
import unittest
logger = logger(__name__)
@ddt
class Register(unittest.TestCase):
    data_1 = ExcelTest(cantins.data_path,"register").read_excel()
    @classmethod
    def setUpClass(cls):
        cls.phone = create_phone()
        logger.info("执行用例前的前置工作")
    @data(*data_1)
    def test_register(self,case):
        logger.info("开始执行测试用例：{}".format(case.title))
        if case.data.find("mobile_phone") > -1:
            case.data = case.data.replace("mobile_phone",self.phone)
        if case.data.find("name") >-1:
            name = random_name()
            case.data = case.data.replace("name",name)
        case.data = getdata(case.data)
        logger.info("测试的数据是：{}".format(case.data))
        res = WebApi(case.url).info_api(case.api,case.data)
        print(res)
        try:
            if case.title == "正常获得验证码":
                self.assertEqual(str(case.exp),res["retCode"])
                ExcelTest(cantins.data_path, "register").write_excel(case.case_id+1,eval(res["retCode"]),"pass")
            if res["retCode"] == "0" and case.title == "正常获得验证码":
                data = DoMysql().fecth_one(eval(case.sql)["sql"])
                setattr(Code,"verify_code",data["Fverify_code"])
            else:
                self.assertEqual(str(case.exp), res["retInfo"])
                ExcelTest(cantins.data_path, "register").write_excel(case.case_id + 1, str(res["retInfo"]), "pass")
                if case.sql:
                    case.sql = case.sql.replace("name",name)
                    #查询数据库，断言数据是否存在，条数是否是一条
                    after = DoMysql().fecth_one(eval(case.sql)["sql"])
                    self.assertIsNotNone(after)
                    after_1 = DoMysql().fecth_one(eval(case.sql)["sql2"])
                    self.assertEqual(1,int(after_1["count(*)"]))
        except AssertionError as e:
            if res["retCode"] == "0" and case.title == "正常获得验证码":
                ExcelTest(cantins.data_path, "register").write_excel(case.case_id + 1, eval(res["retCode"]), "filed")
            else:
                ExcelTest(cantins.data_path, "register").write_excel(case.case_id + 1, str(res["retInfo"]), "filed")
            logger.error("报错了：{}".format(e))
            raise e
        logger.info("{}用例执行完成".format(case.title))
    @classmethod
    def tearDownClass(cls):
        logger.info("用例执行结束后置工作")
