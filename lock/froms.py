# -*- encoding: utf-8 -*-
# @Time : 2018/10/25/025 21:05
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : froms.py
# @Software: PyCharm

from wtforms import Form


class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message