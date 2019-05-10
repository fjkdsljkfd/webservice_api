# -*- coding: utf-8 -*-#
# @Time :2019/4/2813:50
# @Author :xuqiao  
# @Email :1462942304@qq.com
# @File :logger.py
import logging
from webservice_api.conmon import cantins
from webservice_api.conmon.read_conf import Config
def logger(case):
    logger = logging.getLogger(case)
    logger.setLevel("INFO")
    if Config().getvalue("data","hander") == "console":
        console_hander = logging.StreamHandler()
        sonsole_level = Config().getvalue("data","console_level")
        console_hander.setLevel(sonsole_level)
        logger.addHandler(console_hander)
        fmt = Config().getvalue("data","fmt")
        console_hander.setFormatter(logging.Formatter(fmt))
    elif Config().getvalue("data","hander") == "file_hander":
        file_hander = logging.FileHandler(cantins.log_path + "/case.log",encoding="utf-8")
        file_level = Config().getvalue("data","filehander_level")
        file_hander.setLevel(file_level)
        fmt = Config().getvalue("data", "fmt")
        file_hander.setFormatter(logging.Formatter(fmt))
        logger.addHandler(file_hander)
    else:
        print("输出渠道不正确")
    return logger
if __name__ == '__main__':
    logger = logger("case")
    logger.info("这是测试用的")