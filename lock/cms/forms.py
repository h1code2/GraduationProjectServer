# -*- encoding: utf-8 -*-
# @Time : 2018/10/24/024 20:21
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : forms.py
# @Software: PyCharm

from wtforms import  StringField, IntegerField
from wtforms.validators import InputRequired, Length
from lock.froms import BaseForm

class CmsLoginForm(BaseForm):
    username = StringField(validators=[InputRequired(message='请输入真实姓名')])
    password = StringField(validators=[Length(6, 16, message='您输入的密码格式不正确')])
    remember = IntegerField()
