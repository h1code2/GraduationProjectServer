# -*- encoding: utf-8 -*-
# @Time : 2018/10/24/024 20:13
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : manage.py
# @Software: PyCharm

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps import create_app
from exts import db
from lock.common.models import (
    UserModel,
    LocksModel,
    LogsModel,
    UserPermission,
    LockStatus
)

app = create_app()

manager = Manager(app)
Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.option('-o', '--openID', dest='openID')
def add_test_user(openID):
    """
    测试手动添加一个用户
    :param openid:用户openid
    openid: getApp().globalData=openID,
    nickName: e.detail.userInfo.nickName,
    avatarUrl: e.detail.userInfo.avatarUrl,
    province: e.detail.userInfo.province,
    city: e.detail.userInfo.city
    """
    user = UserModel(openID=openID,
                     nickName='二狗子',
                     avatarUrl='http://developer.huangtongx.cn/ifsdfmg.png',
                     province='信阳',
                     city='河南',
                     permission=UserPermission.SUPER_ADMIN)
    db.session.add(user)
    db.session.commit()
    print('数据添加完成')


@manager.option('-i', '--id', dest='id')
def test_user(id):
    """
    查看某用户当前权限
    :param id: 用户在数据库中的id
    """
    user = UserModel.query.filter_by(id=id).first()
    if user:
        print("该用户的权限：" + str(user.permission))
    else:
        print("无该用户")


@manager.command
def init_lock():
    """
    初始化已有门锁信息
    """
    lock_info = [
        {
            'lock_id': 'AB',
            'lock_desc': '实验室01'
        },
        {
            'lock_id': 'AC',
            'lock_desc': '实验室02'
        },
        {
            'lock_id': 'AD',
            'lock_desc': '实验室03'
        },
        {
            'lock_id': 'AE',
            'lock_desc': '实验室04'
        },
        {
            'lock_id': 'AF',
            'lock_desc': '实验室05'
        },
        {
            'lock_id': 'AG',
            'lock_desc': '实验室06'
        },
        {
            'lock_id': 'AH',
            'lock_desc': '实验室07'
        }
    ]
    for info in lock_info:
        lock = LocksModel(lock_id=info['lock_id'], remark=info['lock_desc'])
        db.session.add(lock)
        db.session.commit()
    print('门锁初始化测试信息完成')


@manager.option('-o', '--openID', dest='openID')
@manager.option('-l', '--lock_id', dest='lock_id')
def user_add_lock(openID, lock_id):
    """
    给某用户授权某门锁
    :param openid:用户openid
    :param lock_id:门锁lock_id
    """
    user = UserModel.query.filter_by(openID=openID).first()
    lock = LocksModel.query.filter_by(lock_id=lock_id).first()
    user.locks.append(lock)
    db.session.commit()
    print('用户“' + user.nickName + "”授权开“" + lock.remark + "门”锁成功")


@manager.option('-o', '--openID', dest='openID')
@manager.option('-l', '--lock_id', dest='lock_id')
def user_remove_lock(openID, lock_id):
    """
    移除某用户对某门锁的授权
    :param openid:用户openid
    :param lock_id:门锁lock_id
    """
    user = UserModel.query.filter_by(openID=openID).first()
    lock = LocksModel.query.filter_by(lock_id=lock_id).first()
    user.locks.remove(lock)
    db.session.commit()
    print('用户“' + user.nickName + "”开“" + lock.remark + "门”锁权限已经移除")


@manager.option('-i', '--id', dest='id')
def print_user_lock(id):
    """
    打印某个用户已授权的所有门锁
    :param id:
    :return:
    """
    user = UserModel.query.get(id)
    if user:
        for lock in user.locks:
            print(lock.remark + ":" + lock.lock_id)
    else:
        print('无效openid')


@manager.option('-l', '--lock_id', dest='lock_id')
def print_lock_user(lock_id):
    """
    打印某个门锁已授权的用户
    :param lock_id:
    :return:
    """
    lock = LocksModel.query.filter_by(lock_id=lock_id).first()
    if lock:
        for user in lock.users:
            print(user.nickName + ":" + user.openID)
    else:
        print('无效lock_id')


@manager.option('-o', '--openID', dest='openID')
@manager.option('-p', '--permission', dest='permission')
def modify_user_per(openID, permission):
    """
    修改用户权限
    :param openid: 用户openid
    :param permission: 用户权限 0 guest,1 user,3 admin,255 super_amdin
    """
    user = UserModel.query.filter_by(openID=openID).first()
    if user:
        if permission == '0':
            user.permission = UserPermission.GUEST
        elif permission == '1':
            user.permission = UserPermission.USER
        elif permission == '2':
            user.permission = UserPermission.ADMIN
        elif permission == '15':
            user.permission = UserPermission.SUPER_ADMIN
        elif permission == '255':
            user.permission = UserPermission.DEVELOPER
        else:
            print('权限输入错误')
        db.session.commit()
        print('用户“' + user.nickName + "”的权限已经更新")
    else:
        print('用户不存在')


@manager.command
def close_all_lock():
    """
    重置所有门锁的状态，调试功能
    """
    locks = LocksModel.query.filter_by().all()
    for lock in locks:
        lock.status = LockStatus.CLOSE
    db.session.commit()
    print('所有的门锁状态重置完成')


@manager.command
def delete_lock_logs():
    logs = LogsModel.query.filter_by().all()
    for log in logs:
        db.session.delete(log)
        db.session.commit()
    print('开锁记录全部删除，ok!')


@manager.command
def add_logs():
    user = UserModel.query.get(3)
    for l in range(13):
        log = LogsModel(username='宋江', remark='实验室01', reason='上课', lock_id='AB', user_id=1)
        user.logs.append(log)
        db.session.commit()
    print('haha')


if __name__ == '__main__':
    manager.run()
