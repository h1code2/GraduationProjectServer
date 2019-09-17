# -*- encoding: utf-8 -*-
# @Time : 2018/10/24/024 20:20
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : views.py
# @Software: PyCharm

from flask import Blueprint

bp = Blueprint('common', __name__, url_prefix='/common')


@bp.route('/test/')
def test():
    return 'common'
