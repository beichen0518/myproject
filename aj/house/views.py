import re
import os
from flask import Blueprint, render_template, request, jsonify, session
from user.models import User, House, Area, Facility, HouseImage

from utils import status_code
from user.models import db
from utils.settings import UPLOAD_DIRS
from utils.functions import is_login

house = Blueprint('house', __name__)


@house.route('/myhouse/', methods=['GET'])
@is_login
def myhouse():
    return render_template('myhouse.html')


@house.route('/auth_myhouse/', methods=['GET'])
@is_login
def auth_myhouse():

    user = User.query.get(session['user_id'])
    if user.id_card:
        houses = House.query.filter(House.user_id == user.id).order_by(House.id.desc())
        hlist_list = []
        for house in houses:
            house.to_dict()
            hlist_list.append(house.to_dict())
        return jsonify(hlist_list=hlist_list, code=status_code.OK)
    else:
        return jsonify(status_code.MYHOUSE_USER_IS_NOT_AUTH)


@house.route('/newhouse/', methods=['GET'])
@is_login
def newhouse():
    return render_template('newhouse.html')


@house.route('/area_facility/', methods=['GET'])
def area_facility():
    areas = Area.query.all()
    area_list = [area.to_dict() for area in areas]
    facilitys = Facility.query.all()
    facility_list = [facility.to_dict() for facility in facilitys]
    return jsonify(area_list=area_list, facility_list=facility_list)


@house.route('/createhouse/', methods=['POST'])
@is_login
def create_house():
    user = User.query.get(session['user_id'])
    title = request.form.get('title')
    price = request.form.get('price')
    area_id = request.form.get('area_id')
    address = request.form.get('address')
    room_count = request.form.get('room_count')
    acreage = request.form.get('acreage')
    unit = request.form.get('unit')
    capacity = request.form.get('capacity')
    beds = request.form.get('beds')
    deposit = request.form.get('deposit')
    min_days = request.form.get('min_days')
    max_days = request.form.get('max_days')
    facilities = request.form.getlist('facility')

    house = House()
    house.user_id = user.id
    house.title = title
    house.price = price
    house.area_id = area_id
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days
    house.add_update()

    facilities_list = []
    for fac_id in facilities:
        fac = Facility.query.get(fac_id)
        house.facilities.append(fac)
        facilities_list.append(fac)

    db.session.add_all(facilities_list)
    try:
        db.session.commit()

        # 通过这种方法可以实现和上面一样的效果
        # if facilities:
        #   可以找到facilities中所有的id
        #     facilitys = Facility.query.filter(Facility.id.in_(facilities)).all()
        #     house.facilities = facilitys
        # house.add_update()
        return jsonify(code=status_code.OK, houseid=house.id)
    except:
        return jsonify(status_code.DATABASE_ERROR)


@house.route('/addimage/', methods=['POST'])
@is_login
def add_image():
    image_dict = request.files
    house_id = request.form.get('house_id')
    house = House.query.get(house_id)
    if 'house_image' in image_dict:

        house_img = image_dict['house_image']
        # mimetype文件类型
        if not re.match(r'^image/.*$', house_img.mimetype):
            return jsonify(status_code.MYHOUSE_UPLOAD_IMAGE_IS_ERROR)
        # 图片在flask中的存储路径
        url = os.path.join(UPLOAD_DIRS, house_img.filename)
        # 将图片存在flask中
        house_img.save(url)

        image_url = os.path.join('/static/upload', house_img.filename)

        try:
            if not house.index_image_url:
                house.index_image_url = image_url
                house.add_update()
            house_image = HouseImage()
            house_image.house_id = house.id
            if not HouseImage.query.filter(HouseImage.url == image_url).all():
                house_image.url = image_url
                house_image.add_update()
                return jsonify(code=status_code.OK, url=image_url)
            return jsonify(status_code.MYHOUSE_UPLOAD_IMAGE_IS_EXIST)
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)


@house.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


@house.route('/housedetail/', methods=['GET'])
def house_detail():
    house_id = request.args.get('id')
    house = House.query.get(house_id)

    booking = 1
    #  判断立即预约按钮是否展示
    if 'user_id' in session:
        if house.user_id == session['user_id']:
            booking = 0

    return jsonify(code=status_code.OK, house_dict=house.to_full_dict(), booking=booking)


@house.route('/booking/', methods=['GET'])
@is_login
def booking():
    return render_template('booking.html')
