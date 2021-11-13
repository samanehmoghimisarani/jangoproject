from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create_order/', views.CreateOrder.as_view(), name='create_order'),
   # path('detail_order/', views.DetailOrder.as_view(), name='detail_order'),
    path('history/', views.History.as_view(), name='history'),
]