import functools
from flask import session, redirect
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



def get_db_uri(DATABASE):

    user = DATABASE.get('USER')
    db = DATABASE.get('DB')
    port = DATABASE.get('PORT')
    host = DATABASE.get('HOST')
    password = DATABASE.get('PASSWORD')
    name = DATABASE.get('NAME')
    driver = DATABASE.get('DRIVER')

    return '{}+{}://{}:{}@{}:{}/{}'.format(db, driver, user, password, host, port, name)


def init_ext(app):

    db.init_app(app=app)


# 定义了一个判断是否登录的装饰器
def is_login(view_fun):
    @functools.wraps(view_fun)
    def decorator():
        try:
            # 验证用户是否登录
            # if session['user_id']:
            if 'user_id' in session:
                return view_fun()
            else:
                return redirect('/user/login/')
        except:
            return redirect('/user/login/')
    return decorator