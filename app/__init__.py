from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_mail import Mail




app = Flask(__name__)

bootstrap = Bootstrap(app)
app.config.from_object(Config)      #一定要在SQLALCHEMY实例化对象前面
bcrypt = Bcrypt(app)
mail = Mail(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登陆'
login_manager.login_message_category = 'info'


from app.routes import *   #连接routes.py路由
