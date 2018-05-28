import re
import os
from flask import Blueprint, render_template, request, jsonify, session
from user.models import db, User
from utils import status_code
from utils.settings import UPLOAD_DIRS
from utils.functions import is_login

user = Blueprint('user', __name__)


@user.route('/createdb')
def createdb():
    db.create_all()
    return '创建成功'


"""
注册页面
"""
@user.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


"""
注册请求
"""
@user.route('/register/', methods=['POST'])
def user_register():
    register_dict = request.form

    mobile = register_dict.get('mobile')
    password = register_dict.get('password')
    password2 = register_dict.get('password2')

    #  检查这个3值是否有空，如果有一个值为空，返回True
    if not all([mobile, password, password2]):
        return jsonify(status_code.PARAMS_ERROR)

    if not re.match(r'^1[345789]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)

    if User.query.filter(User.phone == mobile).count():
        return jsonify(status_code.USER_REGISTER_MOBILE_IS_EXSITS)

    if password != password2:
        return jsonify(status_code.USER_REGISTER_PASSWORD_IS_ERROR)

    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = password
    try:
        user.add_update()
        return jsonify(status_code.SUCCESS)
    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)


"""
登录页面
"""
@user.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


"""
post登录api
"""
@user.route('/login/', methods=['POST'])
def user_login():

    user_dict = request.form

    mobile = user_dict.get('mobile')
    password = user_dict.get('password')

    if not all([mobile, password]):
        return jsonify(status_code.PARAMS_ERROR)

    # 测试人员需要再次测试这部分内容
    if not re.match(r'^1[345789]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)

    user = User.query.filter(User.phone == mobile).first()
    if user:
        # 判断密码是否正确
        if user.check_pwd(password):
            session['user_id'] = user.id
            return jsonify(status_code.SUCCESS)
        else:
            return jsonify(status_code.USER_LOGIN_PASSWORD_IS_ERROR)
    else:
        return jsonify(status_code.USER_LOGIN_IS_NOT_EXSIST)


@user.route('/my/', methods=['GET'])
@is_login
def my():
    return render_template('my.html')


@user.route('/user/', methods=['GET'])
@is_login
def get_user_profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify(user=user.to_basic_dict(), code='200')


@user.route('/profile/', methods=['GET'])
@is_login
def profile():
    return render_template('profile.html')


@user.route('/user/', methods=['PUT'])
@is_login
def user_profile():

    profile_dict = request.form
    file_dict = request.files
    user = User.query.filter(User.id == session['user_id']).first()

    if 'avatar' in file_dict:

        f1 = file_dict['avatar']
        # mimetype文件类型
        if not re.match(r'^image/.*$', f1.mimetype):
            return jsonify(status_code.USER_UPLOAD_IMAGE_IS_ERROR)
        # 图片在flask中的存储路径
        url = os.path.join(UPLOAD_DIRS, f1.filename)
        # 将图片存在flask中
        f1.save(url)

        image_url = os.path.join('/static/upload', f1.filename)
        user.avatar = image_url
        try:
            db.session.commit()
            return jsonify(code=status_code.OK, url=image_url)
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)

    elif 'name' in profile_dict:
        name = profile_dict.get('name')
        if User.query.filter(User.name == name).count():
            return jsonify(status_code.USER_NAME_IS_EXSIT)

        user.name = name
        try:
            db.session.commit()
            return jsonify(code=status_code.OK)
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)
    # 如果没有传参数，然后参数错误
    else:
        return jsonify(status_code.PARAMS_ERROR)


@user.route('/auth/', methods=['GET'])
@is_login
def auth():
    return render_template('auth.html')


@user.route('/auths/', methods=['GET'])
@is_login
def get_user_auth():

    user = User.query.get(session['user_id'])
    if all([user.id_name, user.id_card]):
        return jsonify(
            code=status_code.OK,
            id_name=user.id_name,
            id_card=user.id_card
        )


@user.route('/auths/', methods=['PUT'])
@is_login
def user_auth():
    auth_dict = request.form
    real_name = auth_dict.get('real_name')
    id_card = auth_dict.get('id_card')
    if not all([real_name, id_card]):
        return jsonify(status_code.PARAMS_ERROR)

    if not re.match(r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', id_card):
        return jsonify(status_code.USER_AUTH_ID_CARD_IS_ERROR)

    user = User.query.filter(User.id == session['user_id']).first()
    user.id_name = real_name
    user.id_card = id_card
    try:
        user.add_update()
        return jsonify(status_code.SUCCESS)
    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)


@user.route('/logout/', methods=['DELETE'])
@is_login
def logout():
    session.clear()
    return jsonify(status_code.SUCCESS)