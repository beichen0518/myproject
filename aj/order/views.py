from datetime import datetime

from flask import Blueprint, request, session, jsonify, render_template

from utils import status_code
from utils.functions import is_login
from user.models import Order, House, User


orders = Blueprint('orders', __name__)


@orders.route('/', methods=['POST'])
@is_login
def order():

    order_dict = request.form

    house_id = order_dict.get('house_id')
    # datastrptime 将
    start_time = datetime.strptime(order_dict.get('start_time'), '%Y-%m-%d')
    end_time = datetime.strptime(order_dict.get('end_time'), '%Y-%m-%d')

    if not all([house_id, start_time, end_time]):
        return jsonify(status_code.PARAMS_ERROR)

    if start_time > end_time:
        return jsonify(status_code.ORDER_START_TIME_GT_END_TIME)

    house = House.query.get(house_id)

    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = start_time
    order.end_date = end_time
    order.house_price = house.price
    order.days = (end_time - start_time).days + 1
    order.amount = order.days * order.house_price
    try:
        order.add_update()
        return jsonify(code = status_code.OK)
    except:
        return jsonify(status_code.DATABASE_ERROR)


@orders.route('/', methods=['GET'])
@is_login
def get_order():
    return render_template('orders.html')


@orders.route('/orders/', methods=['GET'])
@is_login
def show_orders():
    user = User.query.get(session['user_id'])
    orders = user.orders
    return jsonify(code=status_code.OK, orders=[order.to_dict() for order in orders])


@orders.route('/lorders/', methods=['GET'])
@is_login
def lorders():
    return render_template('lorders.html')


@orders.route('/showlorders/', methods=['GET'])
@is_login
def show_lorders():
    user = User.query.get(session['user_id'])
    houses = user.houses
    orders_list = []
    for house in houses:
        orders = house.orders
        for order in orders:
            orders_list.append(order)

    return jsonify(code=status_code.OK, lorders=[order.to_dict() for order in orders_list])


@orders.route('/changeorder/<int:id>/', methods=['PATCH'])
@is_login
def change_order(id):
    order_status = request.form.get('status')
    order = Order.query.get(id)
    order.status = order_status
    if order_status == 'REJECTED':
        comment = request.form.get('comment')
        order.comment = comment
    try:
        order.add_update()
        return jsonify(code=status_code.OK, order_status=order_status)
    except:
        return jsonify(status_code.DATABASE_ERROR)


@orders.route('/comment/', methods=['PUT'])
@is_login
def comment():
    comment = request.form.get('comment')
    id = request.form.get('orderId')

    order = Order.query.get(id)
    order.comment = comment
    order.status = "COMPLETE"
    try:
        order.add_update()
        return jsonify(status_code.SUCCESS)
    except:
        return jsonify(status_code.DATABASE_ERROR)


