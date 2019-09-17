# -*- encoding: utf-8 -*-
# @Time : 2018/10/24/024 20:08
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : exts.py
# @Software: PyCharm

from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()
