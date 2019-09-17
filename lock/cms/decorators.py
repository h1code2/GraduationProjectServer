# -*- encoding: utf-8 -*-
# @Time : 2018/10/26/026 9:17
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : decorators.py
# @Software: PyCharm

from functools import wraps

from flask import session, redirect, url_for, g
from config import Config as config


def login_required(func):
    """
    登录验证装饰器
    :param func:
    :return:
    """

    @wraps(func)
    def inner(*args, **kwargs):
        if config.CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))

    return inner


def permission_required(permission):
    """
    权限验证装饰器
    :param permission: 需要验证的权限
    :return:
    """

    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.default'))

        return inner

    return outter
