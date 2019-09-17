# -*- encoding: utf-8 -*-
# @Time    : 2018/9/30/030 16:35
# @Author  : 山那边的瘦子
# @Email   : 690238539@qq.com
# @File    : redis.py
# @Software: PyCharm

# 从redis包中导入Redis类
from redis import Redis
from config import Config

# 初始化redis实例变量
xtredis = Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    password=Config.REDIS_PASSWORD,
    retry_on_timeout=Config.REDIS_RETRY_ON_TIMEOUT
)


def set(name, value, ex=None):
    """
    Redis设置值
    :param key:
    :param value:
    """
    xtredis.set(name=name, value=value, ex=ex)


def get(name):
    """
    Redis根据key获取值
    :param key:
    :return:
    """
    return xtredis.get(name=name)


def delete(name):
    """
    Redis删除数据
    :param key:标识
    """
    xtredis.delete(name)
