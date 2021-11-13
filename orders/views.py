from django.shortcuts import render
from cart.cart_sessions import Cart
from .models import Order
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class CreateOrder(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        if request.user.order_rel.all():
            order = request.user.order_rel.get()
        else:
            order = Order.objects.create(user=request.user)
        for item in cart:
            if not item['product'] in order.product.values():
                order.product.add(item['product'])
                order.price = item['price']
                order.save()
        order.total_Price = cart.all_total_price()
        order.save()
        context = {'cart': cart}
        return render(request, 'orders/detail-order.html', context)
'''
class DeleteItme(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
'''


class History(LoginRequiredMixin, View):
    def get(self, request):
        histories = Order.objects.filter(user_id=request.user.id)
        return render(request, 'orders/history.html', {"histories": histories})




