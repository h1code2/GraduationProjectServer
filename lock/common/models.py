# -*- encoding: utf-8 -*-
# @Time : 2018/10/24/024 20:20
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : models.py
# @Software: PyCharm

from exts import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class UserPermission(object):
    """
    用户权限类型
    """
    """
    用户权限定义
    """
    # 255的二进制方式来表示 1111 1111
    GUEST = 0b00000000  # 游客，无开锁权限
    USER = 0b00000001  # 普通用户，基本开锁权限
    ADMIN = 0b00000011  # 管理员
    SUPER_ADMIN = 0b00001111  # 超级管理员
    DEVELOPER = 0b11111111  # 开发者


class LockStatus(object):
    """
    定义门锁状态类型
    """
    OPEN = 1
    CLOSE = 0


user_lock = db.Table(
    'user_lock',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('locks_id', db.Integer, db.ForeignKey('locks.id'), primary_key=True)
)


class UserModel(db.Model):
    """
    用户数据库模型
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openID = db.Column(db.String(100), nullable=False, unique=True)
    nickName = db.Column(db.String(100), nullable=False)
    # 学生信息
    nameU = db.Column(db.String(10), nullable=True)  # 学生名字
    classU = db.Column(db.String(10), nullable=True)  # 学生班级
    studentID = db.Column(db.String(16), nullable=True)  # 学生学号
    _password = db.Column(db.String(200), nullable=True)  # 学生密码
    # 微信信息
    avatarUrl = db.Column(db.String(500), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(10), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)
    # 用户权限
    permission = db.Column(db.Integer, default=UserPermission.USER)
    # 门锁
    locks = db.relationship('LocksModel', secondary=user_lock, backref=db.backref('users'))  # 多对多反向引用
    # 开锁记录
    logs = db.relationship('LogsModel', cascade='all', backref=db.backref('user'))  # 一对多反向引用

    __mapper_args__ = {
        "order_by": time.desc()
    }

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pw):
        self._password = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self._password, pw)

    def has_lock_per(self, lock):
        """
        :param lock: 门锁的对象
        :return: 布尔值
        """
        flag = False
        if lock in self.locks:
            flag = True
        return flag

    def has_permission(self, perm):
        """
        判断用户是否有某种权限
        :param perm: 需要判断的权限
        :return: 布尔值
        """
        # GUEST = 0b00000000  # 游客，无开锁权限
        # USER = 0b00000001  # 普通用户，基本开锁权限
        # ADMIN = 0b00000011  # 管理员
        # SUPER_ADMIN = 0b00001111  # 超级管理员
        # DEVELOPER = 0b11111111  # 开发者
        return self.permission & perm == perm

    def is_super_admin(self):
        """
        判断是否是管理员
        :return: 布尔值
        """
        return self.permission & UserPermission.SUPER_ADMIN == UserPermission.SUPER_ADMIN

    def is_developer(self):
        """
        判断是否为开发者
        :return:布尔值
        """
        return self.permission & UserPermission.DEVELOPER == UserPermission.DEVELOPER


class LocksModel(db.Model):
    """
    锁数据库的模型》多锁
    """
    __tablename__ = 'locks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lock_id = db.Column(db.String(5), nullable=False, unique=True)
    status = db.Column(db.String(5), default=LockStatus.CLOSE)
    remark = db.Column(db.String(100), nullable=True)  # 备注说明
    time = db.Column(db.DateTime, default=datetime.now)

    __mapper_args__ = {
        "order_by": time.desc()
    }


class LogsModel(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    remark = db.Column(db.String(50), nullable=False)  # 弃坑不想
    reason = db.Column(db.String(50), nullable=False)  # 后期添加，开门缘故改了，门室名称
    lock_id = db.Column(db.String(5), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    __mapper_args__ = {
        "order_by": time.desc()
    }

    def to_json(self):
        """
        转JSON
        :return:
        """
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
