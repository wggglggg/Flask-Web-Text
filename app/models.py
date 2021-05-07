from datetime import datetime
from app import db, login_manager
from flask import current_app
from flask_login import UserMixin
import jwt

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

#订阅与被订阅
relationships = db.Table('relationships',
            db.Column('subscribe_to_one_id',db.Integer, db.ForeignKey('user.id'), primary_key=True),
            db.Column('is_subscribed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

#用户表,关联 留言表,订阅表
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar_img = db.Column(db.String(120), default='/static/assets/duitang.jpg', nullable=False)
    texts = db.relationship('Text', backref=db.backref('user', lazy=True))
    subscribe = db.relationship('User',
                           secondary=relationships,
                           primaryjoin=(relationships.c.subscribe_to_one_id == id),
                           secondaryjoin=(relationships.c.is_subscribed_id == id),
                           backref=db.backref('fans', lazy=True),
                           lazy=True
                           )

    def __repr__(self):
        return '<User %r>' % self.username

    #发送修改密码email前将用户id通过pyjwt加密成token
    def generate_reset_password_token(self):

        return jwt.encode({"id": self.id}, current_app.config['SECRET_KEY'], algorithm="HS256")

    #解密token,检测id
    @staticmethod
    def check_reset_password_token(token):
        try:
            decode = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.filter_by(id=decode['id']).first()
        except:
            return None

    def to_subscrib(self,user):
        if not self.check_subscrib_status(user):
            print('self.subscribe.append(user);;;;',self.subscribe.append(user))
            # self.subscribe.append(user)

    def del_followers(self,user):
        if  self.check_subscrib_status(user):
            print('self.subscribe.remove(user)===', self.subscribe.remove(user))
            # self.subscribe.remove(user)

    def check_subscrib_status(self,user):
       # return self.subscribe.filter(relationships.c.is_subscribed_id == user.id).count() > 0
        return self.subscribe.count(user) > 0





#留言板表
class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(400), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now) #注意是now,不是now(),如果有()就只创建时间不更新，反之会更新           时间
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):

        return '<Text %r>' % self.body

