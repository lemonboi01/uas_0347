import os
from flask_sqlalchemy import SQLAlchemy
from project import app
from project.config.DatetimeEncoder import DatetimeEncoder
from project.config.Hash import Hash

from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping' : True}
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_akademik'

db = SQLAlchemy(app)

class NewsModel(db.Model):
   __tablename__ = "tbl_news"

   id = db.Column(db.INTEGER, autoincrement=True, primary_key=True) 
   title = db.Column(db.String(255), nullable=False)
   content = db.Column(db.TEXT, nullable=False)
   datetime = db.Column(db.DATETIME, nullable=False, default=datetime.now)
   flag = db.Column(db.INTEGER, nullable=False, default=1)
   created_by = db.Column(db.INTEGER, ForeignKey("tbl_users.id"), nullable=False)
   updated_by = db.Column(db.INTEGER, ForeignKey("tbl_users.id"), nullable=False)

class UserModel(db.Model):
    __tablename__ = "tbl_users"

    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True) 
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    read_key = db.Column(db.String(255), nullable=True)
    write_key = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.BOOLEAN, nullable=False, default=1)

create_db = False
if not os.path.isfile('db_akademik'):
    db.create_all()
    create_db = True


if create_db:
    user = UserModel(name='Ferdinand', username='admin', password=Hash().getHash('0347'), read_key=Hash().md5(os.urandom(32)), write_key=Hash().md5(os.urandom(32)), is_active=True)
    db.session.add(user)
    db.session.commit()