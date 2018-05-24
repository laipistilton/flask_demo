from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import  pymysql

app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@127.0.0.1:3306/movie?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

#会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)  #编码
    name = db.Column(db.String(100),unique=True)  #呢称
    pwd  = db.Column(db.String(100))
    email = db.Column(db.String(100),unique=True)
    phone = db.Column(db.String(11),unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255),unique=True)
    addtime = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    uuid = db.Column(db.String(255),unique=True)
    userlogs  = db.relationship('Userlog',backref='user')  #会员日志外键关系
    comments  = db.relationship('Comment',backref='user') #评论外键关联
    moviecols  = db.relationship('Moviecol',backref='user') #评论外键关联
    def __repr__(self):
        return '<User %r>' % (self.name)


class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer,primary_key=True)  #编码
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime,index=True,default=datetime.utcnow)

    def __repr__(self):
        return '<Userlog %r>' % self.id

class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer,primary_key=True)  #编码
    name = db.Column(db.String(100),unique=True)
    addtime = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    movies  = db.relationship('Movie',backref='tag') #电影外键关联
    def __repr__(self):
        return '<Tag %r>' % self.name

class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer,primary_key=True)  #编号
    title = db.Column(db.String(255),unique=True)
    url = db.Column(db.String(255),unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255),unique=True)
    star = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)
    tag_id = db.Column(db.Integer,db.ForeignKey('tag.id'))
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    length = db.Column(db.String(100))
    addtime = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    comments  = db.relationship('Comment',backref='movie') #评论外键关联
    moviecols  = db.relationship('Moviecol',backref='movie') #电影收藏外键关联

    def __repr__(self):
        return '<Movie %r>' % self.title

class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer,primary_key=True)  #编号
    title = db.Column(db.String(255),unique=True)
    logo = db.Column(db.String(255),unique=True)
    addtime = db.Column(db.DateTime,index=True,default=datetime.utcnow)

    def __repr__(self):
        return '<Preview %r>' % self.title

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer,primary_key=True)  #编号
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime,index=True,default=datetime.utcnow)

    def __repr__(self):
        return '<Comment %r>' % self.id

#电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer,primary_key=True)  #编号
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id')) #所属电影
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))   #所属用户
    addtime = db.Column(db.DateTime,index=True,default=datetime.utcnow)

    def __repr__(self):
        return '<Moviecol %r>' % self.title

#权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer,primary_key=True)  #编号
    name = db.Column(db.String(100),unique=True)
    url = db.Column(db.String(255),unique=True)
    addtime = db.Column(db.DateTime,index=True,default=datetime.utcnow)

    def __repr__(self):
        return '<Auth %r>' % self.id

#角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer,primary_key=True)  #编号
    name = db.Column(db.String(100),unique=True)
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    admins  = db.relationship('Admin',backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name

#管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer,primary_key=True)  #编号
    name = db.Column(db.String(100),unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.column(db.SmallInteger) #是否超级管理员 0为管理员
    role_id = db.Column(db.Integer,db.ForeignKey('role.id')) #所属角色
    addtime = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    adminlogs  = db.relationship('Adminlog',backref='admin')
    oplogs  = db.relationship('Oplog',backref='admin') #管理员操作日志

    def __repr__(self):
        return '<Admin %r>' % self.name
#管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer,primary_key=True)  #编号
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id')) #
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime,index=True,default=datetime.utcnow)

    def __repr__(self):
        return '<Adminlog %r>' % self.name
#操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer,primary_key=True)  #编号
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id')) #
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    addtime = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    adminlogs = db.Column(db.Integer,db.ForeignKey('admin.id')) #

    def __repr__(self):
        return '<Oplog %r>' % self.name

if __name__ =="__main__":
    db.create_all()