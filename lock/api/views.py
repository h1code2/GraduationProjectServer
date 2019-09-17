# -*- encoding: utf-8 -*-
# @Time : 2018/10/24/024 20:20
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : views.py
# @Software: PyCharm

import json

import requests
from flask import Blueprint
from flask import request

from config import Config as config
from exts import db
from lock.common.models import (
    LocksModel,
    LogsModel,
    UserModel,
    LockStatus,
    UserPermission
)
from utils import tools
from utils.pictools import image_aspect
from utils.tools import img_to_arr
from utils import redis
from utils import restful
from config import Config

requests.packages.urllib3.disable_warnings()

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/user_info/', methods=['GET'])
def user_info():
    """
    拉取用户信息
    :return: 用户信息
    """
    openid = request.args.get('openid')
    if openid != '':
        user = UserModel.query.filter_by(openID=openid).first()
        if user:
            return restful.success('用户数据拉取成功', data={
                'openid': user.openID,
                'nickName': user.nickName,
                'avatarUrl': user.avatarUrl,
                'province': user.province,
                'city': user.city,
                'permission': user.permission,
                'name': user.nameU,
                'class': user.classU,
                'studentID': user.studentID
            })
        else:
            return restful.params_error('异常，联系管理员')
    else:
        return restful.params_error('缺少openid关键参数')


@bp.route('/modifyUserInfo/', methods=['GET'])
def modifyUserInfo():
    openid = request.args.get('openId')
    userName = request.args.get('userName')
    userClass = request.args.get('userClass')
    userID = request.args.get('userID')

    user = UserModel.query.filter_by(openID=openid).first()
    if user:
        user.nameU = userName
        user.classU = userClass
        user.studentID = userID
        user.password = '123456789'
        db.session.commit()
        return restful.success('用户信息更新完成')
    else:
        return restful.params_error('用户不在')


@bp.route('/modify_password/', methods=['GET'])
def modify_password():
    openid = request.args.get('openid')
    old_password = request.args.get('old_password')
    new_password = request.args.get('new_password')
    user = UserModel.query.filter_by(openID=openid).first()
    if user:
        if user.check_password(old_password):
            user.password = new_password
            db.session.commit()
            return restful.success('密码修改成功')
        else:
            return restful.params_error('原密码错误')
    else:
        return restful.params_error('openid参数无效')


@bp.route('/register/', methods=['GET'])
def register():
    """
     插入用户信息
     """
    openid = request.args.get('openid')
    user = UserModel.query.filter_by(openID=openid).first()
    if user:
        return restful.success('老用户，不需要插入')
    else:
        nickName = request.args.get('nickName')
        avatarUrl = request.args.get('avatarUrl')
        province = request.args.get('province')
        city = request.args.get('city')
        user = UserModel(openID=openid, nickName=nickName, avatarUrl=avatarUrl, province=province, city=city)
        db.session.add(user)
        db.session.commit()
        return restful.success('插入数据成功')


@bp.route('/open_lock/', methods=['GET'])
def open_lock():
    """
    测试阶段
    开锁接口
    :return:
    """
    open_id = request.args.get('open_id')  # 用户标示
    lock_id = request.args.get('lock_id')  # 门锁ID，例AB
    code_c = request.args.get('code_c')  # 门上动态码
    reason = request.args.get('reason')  # 开门缘由
    # with app.app_context():
    user = UserModel.query.filter_by(openID=open_id).first()
    if user:
        if user.has_permission(UserPermission.USER):  # 检查当前用户权限
            locks = user.locks
            lock = LocksModel.query.filter_by(lock_id=lock_id).first()
            if user.is_developer() or user.is_super_admin() or lock in locks:  # 检查当前用户是否拥有当前锁的权限 检查是否为超级管理员,开发者
                code_s = redis.get(lock_id)  # 服务器动态码
                if code_s is not None:  # 防止异常处理,判断redis里面是否有内容<服务器只要不炸，这个条件都会成立>
                    code_s = code_s.decode('utf-8')
                    if code_s == code_c:  # 判断门锁动态码是否与当前服务器上一致
                        lock.status = LockStatus.OPEN
                        db.session.commit()
                        # 记录开锁记录
                        log = LogsModel(  # BUG已经修复
                            username=user.nameU,
                            lock_id=lock_id,
                            remark=lock.remark,
                            reason=reason)
                        user.logs.append(log)
                        db.session.commit()
                        return restful.success("开锁成功", data={
                            'msg': '本次开锁已被记录'
                        })
                    else:
                        return restful.params_error("当前动态码已失效")
                else:
                    return restful.server_error("未提供锁ID，导致内部服务器Redis错误")  # 日了狗，竟然会执行..
            else:
                return restful.success("开锁失败，权限不足")
        else:
            return restful.params_error('无权限开锁')
    else:
        return restful.params_error('无该用户信息')


@bp.route('/lock_info/', methods=['GET'])
def lock_info():
    """
    查询门锁信息
    :return: json
    """
    lock_id = request.args.get('lock_id')
    lock = LocksModel.query.filter_by(lock_id=lock_id).first()
    if lock:
        return restful.success('门锁信息拉取成功', data={
            'lock_id': lock.lock_id,
            'remark': lock.remark,
            'status': lock.status,
            'time': lock.time
        })
    else:
        return restful.params_error('门锁信息拉取失败')


@bp.route('/to_arr/', methods=['GET'])
def to_arr():
    """
    硬件下位机获取二维码
    """
    # return '<'
    lock_id = request.args.get('lock_id')[:2]
    code = tools.random_str(6)  # 获取随机六位数字码
    redis.set(lock_id, code, ex=60)
    data = {
        'page': 'pages/lock/lock',
        'scene': lock_id + '_' + code,  # 此处踏坑不使用“=”分割,改用“_”
        'width': '280'
    }
    conn = requests.post(url=config.API_QR_URL + get_token(),
                         data=json.dumps(data),
                         verify=False)
    qr_file_name = "static/images/qr/" + lock_id + ".png"
    with open(qr_file_name, 'wb') as f:  # 保存二维码
        f.write(conn.content)

    image_aspect(qr_file_name, 128, 128). \
        change_aspect_rate(). \
        past_background(). \
        save_result(qr_file_name)

    if img_to_arr(qr_file_name):
        return '{' + img_to_arr(qr_file_name) + '}'
    else:
        return '<'  # 直接返回空<，交给硬件下位机处理,让其再次请求
    # return restful.server_error("内部服务器Redis错误，请联系开发者")  # 日了狗，竟然会执行..


def get_token():
    """
    获取token
    :return: json
    """
    # grant_type = client_credential & appid = APPID & secret = APPSECRET
    token = redis.get('token')
    if token is not None:
        return token.decode('utf-8')
    else:
        conn = requests.get(url=Config.API_TOKEN_URL, params={
            'grant_type': 'client_credential',
            'appid': Config.APP_ID,
            'secret': Config.SESSION_KEY
        }, verify=False)

        json_ = json.dumps(conn.json())
        token = json.loads(json_)['access_token']
        redis.set('token', token, ex=240)  #
        return token


@bp.route('/openLockLogs/', methods=['GET'])
def openLockLogs():
    """
    超级管理员查看全部开锁日志；
    普通用户（管理员）查看自己开锁记录
    :return: json 记录
    """
    openid = request.args.get('openid')
    user = UserModel.query.filter_by(openID=openid).first()
    if user:
        if user.is_super_admin() or user.is_developer():  # 检查是否为超级管理员
            logs = LogsModel.query.filter_by().all()
            data = {}
            result = []
            for index, log in enumerate(logs):
                result.insert(index, {
                    'name': str(log.username)[:8],
                    'remark': log.remark,
                    'lock_id': log.lock_id,
                    'time': str(log.time)[:16]
                })
                print(log.time)
            data['result'] = result
            return restful.success('记录拉取成功', data=data)

        else:  # 普通用户包含管理员
            logs = user.logs
            data = {}
            result = []
            for index, log in enumerate(logs):
                result.insert(index, {
                    'name': str(log.username)[:8],
                    'remark': log.remark,
                    'lock_id': log.lock_id,
                    'time': str(log.time)[:16]
                })
            data['result'] = result
            return restful.success('记录拉取成功', data=data)
    else:
        return restful.params_error('用户不合法')


@bp.route('/lockStatus/', methods=['GET'])
def lockStatus():
    """
    硬件下位机检测门锁状态
    :return: 状态或者提示
    """
    lock_id = request.args.get('lock_id')
    lock = LocksModel.query.filter_by(lock_id=lock_id).first()
    if lock:
        return "{" + str(lock.status) + "}"
    else:
        return restful.params_error('未授权设备')


@bp.route('/closeLock/', methods=['GET'])
def closeLock():
    """
    硬件下位机修改数据库为关门状态，
    :return: 可无
    """
    lock_id = request.args.get('lock_id')
    lock = LocksModel.query.filter_by(lock_id=lock_id).first()
    if lock:
        lock.status = '0'
        db.session.commit()
        return "{ok}"
    else:
        return restful.params_error('未授权设备')


@bp.route('/handleLogin/', methods=['GET'])
def handleLogin():
    """
    开发者服务器请求
    :return:
    """
    code = request.args.get('code')
    conn = requests.get(url=config.API_URL, params={
        'appid': config.APP_ID,
        'secret': config.SESSION_KEY,
        'js_code': code,
        'grant_type': 'authorization_code'
    }, verify=False)

    jsonObj = json.dumps(conn.json())
    return jsonObj


@bp.route('/lock_ids/', methods=['GET'])
def lock_ids():
    openid = request.args.get('openid')
    if openid is not None:
        user = UserModel.query.filter_by(openID=openid).first()
        if user:
            if user.has_permission(UserPermission.ADMIN):
                locks = LocksModel.query.all()
                lock_infos = list()
                for lock in locks:
                    lock_info = dict()
                    lock_info['id'] = lock.lock_id
                    lock_info['remark'] = lock.remark
                    lock_infos.append(lock_info)
                return restful.success('锁ID拉取成功', data=lock_infos)
            else:
                return restful.params_error('权限不足')
        else:
            return restful.params_error('openid不存在!')
    else:
        return restful.params_error('请提交openid参数')


@bp.route('/remote_control/', methods=['GET'])
def remote_control():
    openid = request.args.get('openid')
    lock_id = request.args.get('lock_id')
    password = request.args.get('password')
    if openid is not None and lock_id is not None:
        user = UserModel.query.filter_by(openID=openid).first()
        if user:
            if user.check_password(password):
                if user.has_permission(UserPermission.ADMIN):
                    lock = LocksModel.query.filter_by(lock_id=lock_id).first()
                    if lock:
                        lock.status = LockStatus.OPEN
                        db.session.commit()
                        return restful.success('远程开锁完成')
                    else:
                        return restful.params_error('lock_id不存在')
                else:
                    return restful.params_error('无权限操作')
            else:
                return restful.params_error('密码错误')
        else:
            return restful.params_error('openid不存在')
    else:
        return restful.params_error('请检查openid参数和lock_id参数')
