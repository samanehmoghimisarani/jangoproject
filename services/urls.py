from . import views
from django.urls import path


app_name = 'services'

urlpatterns = [
    path('add_reply/<int:product_id>/<int:comment_id>/', views.add_reply_product, name='add_reply'),
    # ---------------------------------- services ----------------------------------- #
    path('web_design/', views.WebDesign.as_view(), name='web_design'),
    path('graphic_design/', views.GraphicDesign.as_view(), name='graphic_design'),
    path('research_and_type/', views.ResearchAndTyping.as_view(), name='research_and_type'),
    path('online_registration/', views.OnlineRegistration.as_view(), name='online_registration'),
    path('translation/', views.Translation.as_view(), name='translation'),


    # __________________________________ product  ____________________________________ #
    path('products/', views.AllProduct.as_view(), name='all_product'),
    path('products/<slug:slug>/', views.AllProduct.as_view(), name='category_filter'),
    path('detail_product/<slug:slug>/', views.DetailProduct.as_view(), name='detail_product'),

]