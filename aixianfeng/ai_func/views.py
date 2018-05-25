import random
import time
import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import mixins, viewsets
from django.core.urlresolvers import reverse

from ai_func.models import Banner, Nav, Recommend, Shop, MainShow, UserModel, Ticket, Goods, FoodType, CartModel, \
    OrderModel, OrderGoodsModel
from ai_func.serializers import GoodsSerializer, CartSerializer
from ai_func.filters import GoodsFilter, CartFilter


# Create your views here.


def home(request):
    if request.method == 'GET':
        banners = Banner.objects.all()
        navs = Nav.objects.all()
        recoms = Recommend.objects.all()
        shops = Shop.objects.all()
        shows = MainShow.objects.all()
        data = {
            'banners': banners,
            'navs': navs,
            'recoms': recoms,
            'shops': shops,
            'shows': shows
        }
        return render(request, 'home/home.html', data)


def register(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        sex = request.POST.get('sex')
        if sex == '男':
            sex = 1
        else:
            sex = 0
        password = request.POST.get('password')
        password = make_password(password)
        icon = request.FILES.get('icon')
        UserModel.objects.create(
            username=username,
            email=email,
            password=password,
            sex=sex,
            icon=icon
        )
        return HttpResponseRedirect('/axf/login/')


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            if check_password(password, user.password):
                s = 'qwertyuiopasdfghjklzxcvbnm1234567890'
                ticket = ''
                for _ in range(15):
                    ticket += random.choice(s)
                now_times = int(time.time())
                ticket = 'TK_' + ticket + str(now_times)
                response = HttpResponseRedirect('/axf/home/')
                response.set_cookie('ticket', ticket, max_age=86400)
                Ticket.objects.create(
                    ticket=ticket,
                    user=user,
                    expire_date=datetime.datetime.now() + datetime.timedelta(days=1)
                )
                return response
            else:
                return render(request, 'user/user_login.html/', {'password': '密码错误'})
        else:
            return render(request, 'user/user_login.html/', {'name':'用户不存在'})


def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect('/axf/login/')
        ticket = request.COOKIES.get('ticket')
        if ticket:
            Ticket.objects.get(ticket=ticket).delete()
        response.delete_cookie('ticket')
        return response


def mine(request):
    if request.method == 'GET':
        user = request.user
        data = {}
        if user:
            no_pays = user.ordermodel_set.filter(o_status=0).count()
            wait_rev = user.ordermodel_set.exclude(o_status=0).count()
            data = {
                'no_pays': no_pays,
                'wait_rev': wait_rev
            }
        return render(request, 'mine/mine.html/', data)


def cart(request):
    user = request.user
    if user and request.method == 'GET':

        carts = CartModel.objects.filter(user=user)
        for cart in carts:
            if cart.is_select == b'\x01':
                cart.is_select = True
            else:
                cart.is_select = False
        return render(request, 'cart/cart.html/', {'carts': carts})
    elif user and request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': 200
        }
        goods_id = request.POST.get('goodsid')
        is_select = request.POST.get('is_select')
        all_select = request.POST.get('all_select')
        cartorder = CartModel.objects.filter(goods_id=goods_id, user=user).first()
        if cartorder:
            cartorder.is_select = int(is_select)
            cartorder.save()
            data['is_select'] = cartorder.is_select
        elif all_select:
            cartorders = CartModel.objects.filter(user=user)
            data['goods_id']=[]
            for cartorder in cartorders:
                cartorder.is_select = int(all_select)
                cartorder.save()
                data['goods_id'].append(cartorder.goods_id)
            data['all_select'] = all_select
        return JsonResponse(data)
    else:
        return HttpResponseRedirect('/axf/login/')


def order(request):
    user = request.user
    if user and request.method == 'GET':
        carts = CartModel.objects.filter(user=user, is_select=True)
        if carts:
            order = OrderModel.objects.create(user=user)
            for cart in carts:
                OrderGoodsModel.objects.create(order=order,
                                               goods=cart.goods,
                                               goods_num=cart.c_num)
                cart.delete()
        return HttpResponseRedirect(reverse('axf:order_info', args=(str(order.id),)))
    return HttpResponseRedirect(reverse('axf:login'))


def order_info(request, id):
    user = request.user
    if user and request.method == 'GET':
        order_goods = OrderGoodsModel.objects.filter(order_id=id)

        return render(request, 'order/order_info.html', {'order_goods': order_goods})
    else:
        return HttpResponseRedirect('/axf/login/')


def order_list_payed(request):
    user = request.user
    if user and request.method == 'GET':
        data = {}
        orders = OrderModel.objects.filter(user=user).exclude(o_status=0)
        data['order_goods'] = []
        for order in orders:
            order_goods = OrderGoodsModel.objects.filter(order=order)
            data['order_goods'].append(order_goods)
        return render(request, 'order/order_list_payed.html', data)
    else:
        return HttpResponseRedirect('/axf/login/')


def order_list_wait_pay(request):
    user = request.user
    if user and request.method == 'GET':
        data = {}
        orders = OrderModel.objects.filter(user=user, o_status=0)
        data['order_goods'] = []
        for order in orders:
            order_goods = OrderGoodsModel.objects.filter(order=order)
            data['order_goods'].append(order_goods)
        return render(request, 'order/order_list_wait_pay.html', data)
    else:
        return HttpResponseRedirect('/axf/login/')


def market(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('axf:market_filter', args=('104749', '0', '0')))


def market_filter(request, typeid, cid, sortid):
    if request.method == 'GET':
        foodtypes = FoodType.objects.all()
        data = {}

        goods = Goods.objects.filter(categoryid=typeid) if cid == '0' else \
            Goods.objects.filter(categoryid=typeid, childcid=cid)
        if sortid == '1':
            goods = goods.order_by('-productnum')
        elif sortid == '2':
            goods = goods.order_by('-price')
        elif sortid == '3':
            goods = goods.order_by('price')

        alltypes = FoodType.objects.filter(typeid=typeid).first()
        childrentype = []
        for childtypename in alltypes.childtypenames.split('#'):
            childtype = childtypename.split(':')
            childrentype.append(childtype)

        data['foodtypes'] = foodtypes
        data['typeid'] = typeid
        data['goods'] = goods
        data['childrentype'] = childrentype
        data['cid'] = cid

        return render(request, 'market/market.html', data)


class ShowGoods(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    filter_class = GoodsFilter


class AddCart(mixins.ListModelMixin,
              mixins.RetrieveModelMixin,
              mixins.UpdateModelMixin,
              mixins.DestroyModelMixin,
              mixins.CreateModelMixin,
              viewsets.GenericViewSet):

    queryset = CartModel.objects.all()
    serializer_class = CartSerializer
    filter_class = CartFilter


def createcart(request):
    user = request.user
    if user and request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': 200
        }
        goodsid = request.POST.get('goodsid')
        user_cart = CartModel.objects.filter(user=user, goods_id=goodsid).first()
        if user_cart:
            user_cart.c_num += 1
            user_cart.is_select = 1
            user_cart.save()
            data['c_num'] = user_cart.c_num
        else:
            CartModel.objects.create(
                user=user,
                goods_id=goodsid
            )
            data['c_num'] = 1
        return JsonResponse(data)
    return JsonResponse({'code': 400})


def subcart(request):
    user = request.user
    if user and request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': 200
        }
        goodsid = request.POST.get('goodsid')
        user_cart = CartModel.objects.filter(user=user, goods_id=goodsid).first()
        if user_cart:
            if user_cart.c_num == 1:
                user_cart.delete()
                data['c_num'] = 0
            else:
                user_cart.c_num -= 1
                user_cart.is_select =1
                user_cart.save()
                data['c_num'] = user_cart.c_num
        else:
            data['c_num'] = 0
        return JsonResponse(data)
    return JsonResponse({'code': 400})


def pay(request, id):
    user = request.user
    if user and request.method == 'GET':
        order = OrderModel.objects.filter(pk=id).first()
        if order:
            order.o_status = 1
            order.save()
        return HttpResponseRedirect(reverse('axf:mine'))


def carttotal(request):
    user = request.user
    if user and request.method == 'GET':
        data = {
            'msg': '请求成功',
            'code': 200
        }
        data['carttotal'] = 0
        carts = CartModel.objects.filter(user=user)
        for cart in carts:
            print(cart.is_select)
            if cart.is_select == b'\x01':
                data['carttotal'] += float(cart.goods.price) * int(cart.c_num)
        data['carttotal'] = '%.2f' % data['carttotal']
        return JsonResponse(data)
