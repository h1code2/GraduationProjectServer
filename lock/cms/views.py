# -*- encoding: utf-8 -*-
# @Time : 2018/10/24/024 20:21
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : views.py
# @Software: PyCharm

from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g
)
import os
import xlwt
import time
from exts import db
from config import Config as config
from lock.common.models import (
    UserModel,
    LogsModel,
    LocksModel,
    LockStatus,
    UserPermission
)
from utils import restful
from utils.tools import per_transform
from .decorators import login_required, permission_required
from .forms import CmsLoginForm

bp = Blueprint('cms', __name__)


@bp.route('/default/')
@login_required
def default():
    return render_template('cms/default.html')


class CMSLogin(views.MethodView):
    def post(self):
        form = CmsLoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            remember = form.remember.data
            user = UserModel.query.filter_by(nameU=username).first()
            if user:
                if user.check_password(password):
                    if user.permission >= 3:
                        session[config.CMS_USER_ID] = user.id
                        if remember:
                            session.permanent = False
                        return restful.success('登录成功')
                    else:
                        return restful.params_error('抱歉，普通用户无权登录')
                else:
                    return restful.params_error('密码错误')
            else:
                return restful.params_error('用户不存在')

        else:
            return restful.params_error(form.get_error())

    def get(self, message=None):
        return render_template('cms/login.html', message=message)


@bp.route('/openLockLogs/', methods=['GET', 'POST'])
@login_required
@permission_required(UserPermission.USER)
def openLockLogs():
    current_user = g.cms_user

    if request.method == 'GET':

        reason = request.args.get('reason', type=str, default=None)
        page = request.args.get('page', type=int, default=1)
        pagination = None
        if current_user.is_super_admin() or current_user.is_developer():
            if reason and reason not in ['上课', '实验', '签到']:
                pagination = LogsModel.query.filter(
                    LogsModel.reason != '上课',
                    LogsModel.reason != '实验',
                    LogsModel.reason != '签到') \
                    .paginate(page, per_page=config.LOGS_PER_PAGE, error_out=False)

            elif reason and reason in ['上课', '实验', '签到']:
                pagination = LogsModel.query.filter(
                    LogsModel.reason == reason) \
                    .paginate(page, per_page=config.LOGS_PER_PAGE, error_out=False)

            else:
                pagination = LogsModel.query \
                    .paginate(page, per_page=config.LOGS_PER_PAGE, error_out=False)

        elif current_user.permission == 3:
            if reason and reason not in ['上课', '实验', '签到']:
                pagination = LogsModel.query.join(UserModel.__table__).filter(
                    UserModel.permission <= 3,
                    LogsModel.reason != '上课',
                    LogsModel.reason != '实验',
                    LogsModel.reason != '签到') \
                    .paginate(page, per_page=config.LOGS_PER_PAGE, error_out=False)

            elif reason and reason in ['上课', '实验', '签到']:
                pagination = LogsModel.query.join(UserModel.__table__).filter(
                    UserModel.permission <= 3,
                    LogsModel.reason == reason) \
                    .paginate(page, per_page=config.LOGS_PER_PAGE, error_out=False)

            else:
                pagination = LogsModel.query.join(UserModel.__table__).filter(
                    UserModel.permission <= 3) \
                    .paginate(page, per_page=config.LOGS_PER_PAGE, error_out=False)

        # 普通用户登录功能去除
        # else:
        #     if reason and reason not in ['上课', '实验', '签到']:
        #         pagination = user.logs.query.filter(
        #             UserModel.permission <= 3,
        #             LogsModel.reason != '上课',
        #             LogsModel.reason != '实验',
        #             LogsModel.reason != '签到') \
        #             .paginate(page, per_page=config.LOGS_PER_PAGE, error_out=False)
        #
        #     elif reason and reason in ['上课', '实验', '签到']:
        #         pagination = user.logs.filter(UserModel.permission <= 3, LogsModel.reason == reason) \
        #             .paginate(page, per_page=config.LOGS_PER_PAGE, error_out=False)
        #
        #     else:
        #         pagination = user.logs \
        #             .paginate(page, per_page=config.LOGS_PER_PAGE, error_out=False)

        logs = pagination.items

        content = {
            'logs': logs,
            'current_reason': reason,
            'pagination': pagination
        }
        return render_template('cms/openLockLogs.html', **content)

    else:
        """
        删除开锁记录功能在这呢
        """
        if current_user.is_super_admin() and current_user.is_developer():
            ids = request.form.getlist('ids[]')
            for i in ids:
                log = LogsModel.query.get(i)
                db.session.delete(log)
            db.session.commit()
            return restful.success('记录删除成功')
        else:
            return restful.success('你无权限删除开锁记录')


@bp.route('/refreshLock/')
@login_required
@permission_required(UserPermission.DEVELOPER)
def refreshLock():
    """
    测试api刷新锁的状态为关
    :return:
    """
    locks = LocksModel.query.filter_by().all()
    for lock in locks:
        lock.status = LockStatus.CLOSE
    db.session.commit()
    return render_template('cms/refreshLock.html')


@bp.route('/userManage/', methods=['GET'])
@login_required
@permission_required(UserPermission.ADMIN)
def userManage():
    page = request.args.get('page', type=int, default=1)

    user = UserModel.query.get(session.get(config.CMS_USER_ID))
    pagination = None
    if user.permission == 3:
        pagination = UserModel.query.filter(UserModel.permission < 3) \
            .paginate(page, per_page=config.USERS_PER_PAGE, error_out=False)
    elif user.permission == 15:
        pagination = UserModel.query.filter(UserModel.permission < 15) \
            .paginate(page, per_page=config.USERS_PER_PAGE, error_out=False)
    elif user.permission == 255:
        pagination = UserModel.query.filter(UserModel.permission < 255) \
            .paginate(page, per_page=config.USERS_PER_PAGE, error_out=False)

    users = pagination.items

    content = {
        'users': users,  # 拿自己权限下的用户
        'currentUser': user,  # 当前用户对象,
        'pagination': pagination
    }
    return render_template('cms/userManage.html', **content)


@bp.route('/lockManage/')
@login_required
@permission_required(UserPermission.SUPER_ADMIN)
def lockManage():
    locks = LocksModel.query.filter_by().all()
    user = UserModel.query.get(session.get(config.CMS_USER_ID))
    content = {
        'locks': locks,
        'user': user
    }
    return render_template('cms/lockManage.html', **content)


@bp.route('/userInfo/')
@login_required
def userInfo():
    return render_template('cms/userInfo.html')


@bp.route('/remoteControl/', methods=['POST'])
@login_required
@permission_required(UserPermission.ADMIN)
def remoteControl():
    lock_id = request.form.get('lock_id')
    password = request.form.get('password')

    lock = LocksModel.query.get(lock_id)
    user = UserModel.query.get(session[config.CMS_USER_ID])
    if user.check_password(password):
        if user.is_developer() or user.is_super_admin() or lock in user.locks:  # 开发者真牛逼
            if lock:
                lock.status = LockStatus.OPEN
                db.session.commit()
                return restful.success('{}的门锁已开'.format(lock.remark, lock.lock_id))
            else:
                return restful.params_error('异常，可以联系开发者处理')
        else:
            return restful.params_error('你无权限远程操作次门锁')
    else:
        return restful.params_error('密码输入错误')


@bp.route('/modifyLockInfo/', methods=['POST'])
@login_required
@permission_required(UserPermission.SUPER_ADMIN)
def modifyLockInfo():
    id = request.form.get('id')
    tmpMsg = request.form.get('tmpMsg')
    lock = LocksModel.query.get(id)
    if lock:
        lock.remark = tmpMsg
        db.session.commit()
        return restful.success('锁:{}信息修改成功'.format(lock.lock_id))
    else:
        return restful.success('异常，可以联系开发者处理')


@bp.route('/lockInfo/', methods=['POST'])
@login_required
@permission_required(UserPermission.SUPER_ADMIN)
def lockInfo():
    lockID = request.form.get('id')
    lock = LocksModel.query.get(lockID)
    return restful.success('数据拉取成功', data={
        'id': lock.id,
        'lock_id': lock.lock_id,
        'remark': lock.remark,
        'time': str(lock.time)
    })


@bp.route('/deleteLock/', methods=['POST'])
@login_required
@permission_required(UserPermission.SUPER_ADMIN)
def deleteLock():
    lockID = request.form.get('id')
    lock = LocksModel.query.get(lockID)
    db.session.delete(lock)
    db.session.commit()
    return restful.success(lock.lock_id + '已经删除')


@bp.route('/deleteUser/', methods=['POST'])
@login_required
@permission_required(UserPermission.ADMIN)
def deleteUser():
    user_id = request.form.get('user_id')
    user = UserModel.query.get(user_id)
    currentUser = UserModel.query.get(session.get(config.CMS_USER_ID))
    if currentUser.permission > user.permission:
        db.session.delete(user)
        db.session.commit()
        return restful.success(user.nameU + '用户已被删除')
    else:
        return restful.success('越权行为不允许')


@bp.route('/setAdminPer/', methods=['POST'])
@login_required
@permission_required(UserPermission.SUPER_ADMIN)
def setAdminPer():
    user_id = request.form.get('user_id')
    user = UserModel.query.get(user_id)
    currentUser = UserModel.query.get(session.get(config.CMS_USER_ID))
    if currentUser.permission > user.permission:
        user.permission = UserPermission.ADMIN
        db.session.commit()
        return restful.success(user.nameU + '已经被设置管理员')
    else:
        return restful.success('越权行为不允许')


@bp.route('/export_data/', methods=['POST'])
@login_required
@permission_required(UserPermission.SUPER_ADMIN)
def export_data():
    exportType = request.form.get('exportType', type=int)
    reason = None
    # 我靠,尽然没switch语句
    if exportType == 1:
        reason = '签到'
        logs = LogsModel.query.filter_by(reason='签到').all()
    elif exportType == 2:
        reason = '上课'
        logs = LogsModel.query.filter_by(reason='上课').all()
    elif exportType == 3:
        reason = '实验'
        logs = LogsModel.query.filter_by(reason='实验').all()
    elif exportType == 4:
        reason = '其他'
        logs = LogsModel.query.filter(
            LogsModel.reason != '签到',
            LogsModel.reason != '上课',
            LogsModel.reason != '实验').all()
    else:
        reason = '全部'
        logs = LogsModel.query.filter_by().all()

    # 删除之前的文件
    # 此处而已非常的灵活,后期实现
    root_path = os.getcwd()
    for f in os.listdir(os.path.join(root_path, 'export/excel')):
        path = os.path.join(os.path.join(root_path, 'export/excel'), f)
        if os.path.exists(path):
            os.remove(path)

    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    sheet.write(0, 0, '姓名')
    sheet.write(0, 1, '班级')
    sheet.write(0, 2, '权限')
    sheet.write(0, 3, '备注')
    sheet.write(0, 4, '门室')
    sheet.write(0, 5, '锁ID')
    sheet.write(0, 6, '时间')

    for index, log in enumerate(logs):
        sheet.write(index + 1, 0, log.username)
        sheet.write(index + 1, 1, log.user.classU)
        sheet.write(index + 1, 2, log.user.permission)
        sheet.write(index + 1, 3, log.reason)
        sheet.write(index + 1, 4, log.remark)
        sheet.write(index + 1, 5, log.lock_id)
        sheet.write(index + 1, 6, str(log.time))
    filename = reason + str(int(time.time())) + '.xls'
    filepath = 'export/excel/' + filename
    wbk.save(filepath)
    # 测试用
    # result = []
    # for log in logs:
    # 	result.append(log.to_json())
    # return jsonify(result), 200

    return restful.success('记录文件生成成功', data={
        'filename': filename,
        'fileurl': filepath
    })


@bp.route('/add_lock/', methods=['POST'])
@login_required
@permission_required(UserPermission.SUPER_ADMIN)
def add_lock():
    lock_id = request.form.get('lock_id')
    lock_remark = request.form.get('lock_remark')

    if lock_id.replace(" ", "") != "" and lock_remark.replace(" ", "") != "":
        lock = LocksModel(lock_id=lock_id, remark=lock_remark)
        db.session.add(lock)
        db.session.commit()

        if LocksModel.query.filter_by(lock_id=lock_id).first():
            return restful.success('门锁设备添加成功')
        else:
            return restful.success('门锁设备添加失败')
    else:
        return restful.params_error('请检查你输入的内容')


@bp.route('/cancelAdminPer/', methods=['POST'])
@login_required
@permission_required(UserPermission.SUPER_ADMIN)
def cancelAdminPer():
    user_id = request.form.get('user_id')
    user = UserModel.query.get(user_id)
    currentUser = UserModel.query.get(session.get(config.CMS_USER_ID))
    if currentUser.permission > user.permission:
        user.permission = UserPermission.USER
        db.session.commit()
        return restful.success(user.nameU + '已经被取消管理员')
    else:
        return restful.success('越权行为不允许')


@bp.route('/userAuthorizationMange/', methods=['POST'])
@login_required
@permission_required(UserPermission.ADMIN)
def userAuthorizationMange():
    user_id = request.form.get('user_id')
    currentUser = UserModel.query.get(user_id)
    user = UserModel.query.get(session.get(config.CMS_USER_ID))
    locks = None
    if user.permission == 3:
        locks = user.locks
    elif user.permission >= 15:
        locks = LocksModel.query.filter_by().all()

    data = dict()
    data['currentUser'] = {
        'id': currentUser.id,
        'name': currentUser.nameU,
        'permission': currentUser.permission
    }
    lockResult = []
    for index, lock in enumerate(locks):
        lockResult.insert(index, {
            'id': lock.id,
            'lock_id': lock.lock_id,
            'remark': lock.remark,
            'time': str(lock.time),
            'flag': currentUser.has_lock_per(lock)
        })
    data['lockResult'] = lockResult
    return restful.success('数据拉取成功', data=data)


@bp.route("/addUserLockPer/", methods=['POST'])
@login_required
@permission_required(UserPermission.ADMIN)
def addUserLockAuth():
    user_id = request.form.get('user_id')
    lock_id = request.form.get('lock_id')
    user = UserModel.query.get(user_id)
    lock = LocksModel.query.filter_by(lock_id=lock_id).first()
    if lock in user.locks:
        return restful.success(user.nameU + '已经拥有该门锁权限')
    else:
        user.locks.append(lock)
        db.session.commit()
        return restful.success(user.nameU + "授权开" + lock.remark + "门成功")


@bp.route('/removeUserLockPer/', methods=['POST'])
@login_required
@permission_required(UserPermission.ADMIN)
def removeUserLockAuth():
    user_id = request.form.get('user_id')
    lock_id = request.form.get('lock_id')
    user = UserModel.query.get(user_id)
    lock = LocksModel.query.filter_by(lock_id=lock_id).first()
    if lock in user.locks:
        user.locks.remove(lock)
        db.session.commit()
        return restful.success(user.nameU + "开" + lock.remark + "门权限已移除")
    else:
        return restful.success(user.nameU + '无该授权，无需取消')


@bp.route('/check_lock_per/', methods=['POST'])
@login_required
@permission_required(UserPermission.ADMIN)
def check_lock_per():
    lock_id = request.form.get('lock_id')
    lock = LocksModel.query.get(lock_id)
    users = list()
    for user in lock.users:
        users.append({
            'name': user.nameU,
            'class': user.classU,
            'permission': per_transform(user.permission),
            'number': user.studentID
        })
    return restful.success('success', data=users)


@bp.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect(url_for('cms.login'))


bp.add_url_rule('/', view_func=CMSLogin.as_view('login'))
