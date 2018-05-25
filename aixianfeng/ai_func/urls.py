from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from ai_func import views

router = SimpleRouter()
router.register(r'goods', views.ShowGoods)
router.register(r'addcart', views.AddCart)

urlpatterns = [
     url(r'^home/', views.home, name='home'),
     url(r'^register/', views.register, name='register'),
     url(r'^login/', views.login, name='login'),
     url(r'^logout', views.logout, name='logout'),
     url(r'^mine/', views.mine, name='mine'),
     url(r'^cart/$', views.cart, name='cart'),
     url(r'^order/$', views.order, name='order'),
     url(r'^orderinfo/(\d+)/', views.order_info, name='order_info'),
     url(r'^payed/', views.order_list_payed, name='order_list_payed'),
     url(r'^waitpay', views.order_list_wait_pay, name='order_list_wait_pay'),
     url(r'^market/$', views.market, name='market'),
     url(r'^market/(\d+)/(\d+)/(\d+)/', views.market_filter, name='market_filter'),
     url(r'^createcart/', views.createcart, name='createacart'),
     url(r'^subcart/', views.subcart, name='subcart'),
     url(r'^pay/(\d+)/', views.pay, name='pay'),
     url(r'^carttotal/', views.carttotal)

]
urlpatterns += router.urls

