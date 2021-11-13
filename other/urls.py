from . import views
from django.urls import path


app_name = 'other'

urlpatterns = [

    # --------------------------------------- contact us --------------------------------------------- #
    path('contact_us/', views.ContactUs.as_view(), name='contact_us'),

    # ------------------------------------ news ------------------------------------------------------- #
    path('sort_news_by_date/', views.SortNewsByDate.as_view(), name='sort_news_by_date'),
    path('sort_news_by_must_visited/', views.SortNewsByMustVisit.as_view(), name='sort_news_by_must_visited'),
    path('search_news/', views.SearchNews.as_view(), name='search_news'),
    path('add_reply_news/<int:news_id>/<int:comment_id>/', views.add_reply_news, name='add_reply_news'),
    path('news/', views.AllNews.as_view(), name='all_news'),
    path('detail_news/<slug:slug>/', views.DetailNews.as_view(), name='detail_news'),
    # ------------------------------------ product filter ---------------------------------------------- #
    path('search/', views.SearchProduct.as_view(), name='search'),
    path('search_result/', views.SearchResult.as_view(), name='search_result'),
    path('sort_by_lowest_price/', views.SortByLowestPrice.as_view(), name='sort_by_lowest_price'),
    path('sort_by_date/', views.SortByDate.as_view(), name='sort_by_date'),
    path('free_products/', views.FreeProduct.as_view(), name='free-products'),
    path('sort_by_must_visited/', views.SortProductByMustVisit.as_view(), name='sort_by_must_visited'),

]