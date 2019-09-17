# -*- encoding: utf-8 -*-
# @Time : 2018/10/26/026 9:38
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : hooks.py
# @Software: PyCharm

from flask import session, g

from config import Config as config
from lock.common.models import UserModel
from .views import bp


@bp.before_request
def berfore_request():
    """
    全局g(cms_user)
    :return:
    """
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = UserModel.query.get(user_id)
        if user:
            g.cms_user = user
