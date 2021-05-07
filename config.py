import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    #SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY')# or 'asdf865zx3'  or前面的是需要在windows系统环境添加一条SECRET_KEY或者直接写明文密码

    #RECAPTCHA_PUBLIC_KEY
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')  #or前面的是需要在windows系统环境添加或者直接写明文密码
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') #or '6LecxLwaAAAAAGKWK_qbL49GmJsrF6N3rp7pl3C-'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.environ.get('DATABASE_URL'), 'app.db')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\\db\\app.db'
    UPLOAD_FOLDER = os.path.join(basedir)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Gmail邮箱 配置
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')