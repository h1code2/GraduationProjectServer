# -*- encoding: utf-8 -*-
# @Time : 2018/10/24/024 20:09
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : config.py
# @Software: PyCharm

class Config(object):
    # session必须要设置key
    SECRET_KEY = 'qwertyuioplmnkjbhgvcfdxs'
    # SECRET_KEY = os.urandom(24)

    # 数据库配置
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = '123'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'autoLock'

    # mysql数据库连接信息,这里改为自己的账号
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
        DIALECT,
        DRIVER,
        USERNAME,
        PASSWORD,
        HOST,
        PORT,
        DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_TEARDOWN = True

    # Redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'
    REDIS_PASSWORD = '690238539'
    REDIS_RETRY_ON_TIMEOUT = '2'

    # 小程序配置
    API_URL = 'https://api.weixin.qq.com/sns/jscode2session'  # 登录
    API_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token'  # 获取Token
    API_QR_URL = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token='  # 获取参数二维码

    # <--物联网001
    APP_ID = 'wx6375f9435e72ebd7'
    SESSION_KEY = 'cdf45398fa1e6b160c346f6c5d05069e'
    # 物联网001-->

    # <--测试环境
    # APP_ID = 'wx5dde094cd8021cb0'
    # SESSION_KEY = 'ef6c2d3c552dfe8a9d981fa9eccd417e'
    # 测试环境-->

    ENCRYPTED_DATA = 'CiyLU1Aw2KjvrjMdj8YKliAjtP4gsMZMQmRzooG2xrDcvSnxIMXFufNstNGTyaGS9uT5geRa0W4oTOb1WT7fJlAC+oNPdbB+3hVbJSRgv+4lGOETKUQz6OYStslQ142dNCuabNPGBzlooOmB231qMM85d2/fV6ChevvXvQP8Hkue1poOFtnEtpyxVLW1zAo6/1Xx1COxFvrc2d7UL/lmHInNlxuacJXwu0fjpXfz/YqYzBIBzD6WUfTIF9GRHpOn/Hz7saL8xz+W//FRAUid1OksQaQx4CMs8LOddcQhULW4ucetDf96JcR3g0gfRK4PC7E/r7Z6xNrXd2UIeorGj5Ef7b1pJAYB6Y5anaHqZ9J6nKEBvB4DnNLIVWSgARns/8wR2SiRS7MNACwTyrGvt9ts8p12PKFdlqYTopNHR1Vf7XjfhQlVsAJdNiKdYmYVoKlaRv85IfVunYzO0IKXsyl7JCUjCpoG20f0a04COwfneQAGGwd5oa+T8yO5hzuyDb/XcxxmK01EpqOyuxINew=='
    IV = 'r7BXXKkLb8qrSNn05n0qiA=='

    CMS_USER_ID = 'jkfgsjdgfsdahgfjsh'

    # Celery配置
    # CELERY_BACKEND_URL = 'redis://localhost:6379/0'
    # CELERY_BROKER_URL = 'redis://localhost:6379/0'

    # Flask - APScheduler配置
    # JOBS = [
    #     {
    #         'id': 'qr001',
    #         'func': 'produce:qr',
    #         'args': None,
    #         'trigger': 'interval',
    #         'seconds': 15,
    #         'max_instances': 10
    #     }
    # ]
    #
    # SCHEDULER_API_ENABLED = True

    # 分页相关配置
    LOGS_PER_PAGE = 15
    USERS_PER_PAGE = 16
