from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('detail_cart/', views.DetailCart.as_view(), name='detail_cart'),
    path('add_object/<int:product_id>/', views.AddCartObject.as_view(), name='add_object'),
    path('remove_object/<int:product_id>/', views.RemoveObject.as_view(), name='remove_object'),
#    path('apply_coupon/', views.ApplyCoupon.as_view(), name='apply_coupon'),
    path('checkout_cart/', views.CheckoutCart.as_view(), name='checkout_cart'),

]

