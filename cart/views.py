from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


from services.models import Product
from .cart_sessions import Cart
from .models import Coupon
from .forms import CouponForm


class ApplyCoupon(LoginRequiredMixin, View):
    def post(self, request):
        cart = Cart(request)
        if cart:
            form = CouponForm(request.POST)
            if form.is_valid():
                coupon_code = form.cleaned_data['code']
                try:
                    coupon = get_object_or_404(Coupon, code=coupon_code)
                    if coupon.active_date_start > timezone.now():
                        coupon.active = False
                        messages.error(request, f'This Coupon Has Not Been Activated yet. Please wait Until '
                                                f'{coupon.active_date_start}', 'error')
                    elif timezone.now() > coupon.active_date_end:
                        coupon.active = False
                        messages.error(request, 'The Deadline For Using This Coupon has passed', 'error')
                    else:
                        if coupon.active:
                            discount = cart.all_total_price() / 100 * coupon.discount  # عدد تقسیم 100 ضربدر درصد
                            new_total_price = cart.all_total_price() - discount
                            context = {'cart': cart, 'coupon': coupon, 'new_total_price': new_total_price}
                            return render(request, 'cart/checkout.html.html', context)
                except:
                    messages.error(request, 'this coupon is not active')
                    context = {'cart': cart, 'coupon': coupon_code, 'form': form}
                    return render(request, 'cart/checkout.html', context)
        return redirect('cart:checkout_cart')


class CheckoutCart(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
      #  form = CouponForm()
        context = {'cart': cart}    # , 'form': form
        return render(request, 'cart/checkout.html', context)


class DetailCart(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/detail-cart.html', {'cart': cart})


class AddCartObject(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        messages.success(request, 'محصول مورد نظر به سبد خرید شما اضافه شد . ')
        return redirect('services:detail_product', product.slug)


class RemoveObject(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product=product)
        return redirect('cart:detail_cart')

