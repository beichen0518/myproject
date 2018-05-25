import datetime
import pytz

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from ai_func.models import UserModel, Ticket


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):

        ticket = request.COOKIES.get('ticket')
        request.user = None
        if ticket:
            user_ticket = Ticket.objects.filter(ticket=ticket)
            # if user_ticket[0].expire_date < datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC')):
            # 数据库中返回的时间要比实际小8个小时，需要用与之对应的utcnow， 并且因为utcnow()是带时区的时间，需要转化
            try:
                if user_ticket[0].expire_date < datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')):
                    user_ticket[0].delete()

                else:
                    request.user = user_ticket[0].user
            except IndexError as e:
                pass

