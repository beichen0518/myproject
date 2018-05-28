from flask import Blueprint, render_template, jsonify, request, session


from user.models import House, Area, User, Order
from utils import status_code

ihome_blueprint = Blueprint('ihome', __name__)


@ihome_blueprint.route('/')
def index():
    return render_template('index.html')


@ihome_blueprint.route('/index/', methods=['GET'])
def show_index():
    # 按房屋id降序
    houses = House.query.order_by(House.id.desc()).all()[:5]
    areas = Area.query.all()
    user_name = ''
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user_name = user.name

    return jsonify(code=status_code.OK, houses=[house.to_dict() for house in houses], areas=[area.to_dict() for area in areas],
                   user=user_name)


@ihome_blueprint.route('/search/', methods=['GET'])
def search_house():
    return render_template('search.html')


@ihome_blueprint.route('/searchhouse/', methods=['GET'])
def show_house():
    search_dict = request.args

    area_id = search_dict.get('aid')
    start_date = search_dict.get('sd')
    end_date = search_dict.get('ed')
    sort_type = search_dict.get('sk')
    houses = House.query
    if area_id:
        houses = House.query.filter(House.area_id == area_id)
    # 对房屋进行处理
    if start_date and end_date:
        order1 = Order.query.filter(Order.begin_date <= start_date,
                               Order.end_date >= start_date)
        order2 = Order.query.filter(Order.begin_date >= start_date,
                                    Order.begin_date <= end_date)
        orders = list(order1) + list(order2)
        orders_id = [order.house_id for order in orders]
        houses = houses.filter(House.id.notin_(orders_id))

    if sort_type == 'booking':
        sort_key = House.room_count.desc()
    elif sort_type == 'price-inc':
        sort_key = House.price.asc()
    elif sort_type == 'price-des':
        sort_key = House.price.desc()
    else:
        sort_key = House.id.desc()

    houses = houses.order_by(sort_key)

    hlist = [house.to_full_dict() for house in houses]

    areas = Area.query.all()
    return jsonify(code=status_code.OK, hlist=hlist, alist=[area.to_dict() for area in areas])





