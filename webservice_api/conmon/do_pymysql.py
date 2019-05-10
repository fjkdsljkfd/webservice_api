# -*- coding: utf-8 -*-#
# @Time :2019/4/2210:26
# @Author :xuqiao  
# @Email :1462942304@qq.com
# @File :do_pymysql.py
import pymysql
from webservice_api.conmon.read_conf import Config
class DoMysql:
    def __init__(self):
        host = Config().getvalue("data","host")
        user = Config().getvalue("data","user")
        password = Config().getvalue("data","user_password")
        port = Config().getint_value("data","port")
        self.mysql = pymysql.connect(host = host,user = user,password = password,port = port)
        self.cursor = self.mysql.cursor(pymysql.cursors.DictCursor)
    def fecth_one(self,sql):
        self.cursor.execute(sql)
        self.mysql.commit()
        return self.cursor.fetchone()
    def fecth_all(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    def close_mysql(self):
        self.cursor.close()
        self.mysql.close()
if __name__ == '__main__':
    res = DoMysql().fecth_one('select * from user_db.t_user_info where Fuser_id="赵会方"')
    print(res)
