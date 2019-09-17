# -*- encoding: utf-8 -*-
# @Time : 2018/10/19/019 9:35
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : restful.py
# @Software: PyCharm

from flask import jsonify


class HttpCode(object):
    ok = 200
    unautherror = 401
    paramserror = 400
    servererror = 500


def restful_result(code, message, data):
    """
    自定义数据格式
    :param code: 状态码
    :param message: 信息
    :param data: 数据
    :return: json
    """
    return jsonify({"code": code, "message": message, "data": data or {}})


def success(message='', data=None):
    return restful_result(code=HttpCode.ok, message=message, data=data)


def unauth_error(message=''):
    return restful_result(code=HttpCode.unautherror, message=message, data=None)


def params_error(message=''):
    return restful_result(code=HttpCode.paramserror, message=message, data=None)


def server_error(message=''):
    return restful_result(code=HttpCode.servererror, message=message or "服务器内部错误", data=None)
