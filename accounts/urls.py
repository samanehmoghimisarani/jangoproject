from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('profile/<int:user_id>/', views.UserProfile.as_view(), name='profile'),
    path('update_profile/<int:user_id>/', views.UpdateProfile.as_view(), name='update_profile'),
    # ---------------------------------------- Reset password -------------------------------------- #
    path('reset/', views.ResetPassword.as_view(), name='reset'),
    path('reset/done/', views.DonePassword.as_view(), name='reset_done'),
    path('confirm/<uidb64>/<token>/', views.ConfirmPassword.as_view(), name='confirm_password'),
    path('confirm/done/', views.Complete.as_view(), name='confirm_done'),

]

