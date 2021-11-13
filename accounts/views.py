from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, logout, authenticate
from .forms import UserLoginForm, UserRegisterForm, ChangeProfileForm
from django.contrib import messages
from .models import User
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginUser(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        other_page_url = request.META.get('HTTP_REFERER')
        form = self.form_class
        return render(request, self.template_name, {'form': form, 'other_page_url': other_page_url})

    def post(self, request):
        form = self.form_class(request.POST)
        other_page_url = None
        if 'other_page_url' in request.POST:
            other_page_url = request.POST['other_page_url']
        this_page_url = 'http://127.0.0.1:8000/accounts/login/'
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'your login is successfully', 'success')
                if other_page_url :
                    return redirect(other_page_url)
                return redirect('core:home')
            messages.error(request, 'username or password is not true', 'success')
            return redirect('accounts:login')
        messages.error(request, 'لطفا اطلاعات معتبر وارد کنبد', 'success')
        return redirect('accounts:login')


class UserRegister(View):
        form_class = UserRegisterForm
        template_name = 'accounts/register.html'

        def get(self, request):
            form = self.form_class
            return render(request, self.template_name, {'form': form})

        def post(self, request):
            form = self.form_class(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = User.objects.create_user(email=cd['email'], username=cd['username'], name=cd['name'],
                                                family=cd['family'], phone=cd['phone'], password=cd['password'])
                user.save()
                login(request, user)
                messages.success(request, 'ثبت نام شما باموفقیت انجام شد', 'success')
                return redirect('core:home')
            messages.error(request, 'لطفا اطلاعات را بدرستی وارد کنید')
            return redirect('accounts:register')


class LogoutUser(LoginRequiredMixin, View):

    def get(self, request):
        url = request.META.get('HTTP_REFERER')
        this_page_url = 'http://127.0.0.1:8000/accounts/logout/'
        logout(request)
        if url != this_page_url:
            return redirect(url)
        return redirect('core:home')


class UserProfile(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, self.template_name, {'user': user})


class UpdateProfile(LoginRequiredMixin, View):
    form_class = ChangeProfileForm
    template_name = 'accounts/change_profile.html'

    def get(self, request, user_id):
        if request.user.id == user_id:
            user = get_object_or_404(User, id=user_id)
            return render(request, self.template_name, {'form': self.form_class(instance=user)})

    def post(self, request, user_id):
        if request.user.id == user_id:
            user = get_object_or_404(User, id=user_id)
            # اگه ی فیلد یونیک داشته باشیم و از
            # مدل فرم ها استفاده کرده باشیم برای ایزولید شدنش باید اینجاهم اینستنس یفرستیم
            form = self.form_class(request.POST, instance=user)
            if form.is_valid():
                cd = form.cleaned_data
                user.email = cd['email']
                user.username = cd['username']
                user.name = cd['name']
                user.family = cd['family']
                user.phone = cd['phone']
                user.save()
                messages.success(request, 'پروفایل شما اپدیت شد')
                return redirect('accounts:profile', user.id)
            messages.error(request, 'لطفا دوباره امتحان کنید')
            return redirect('accounts:update_profile', user.id)


# مرحله یک دریافت ایمیل کاربر و فرستادن یه ایمیل برای تغیر  پسورد
class ResetPassword(auth_views.PasswordResetView):
    template_name = 'accounts/reset.html'
    success_url = reverse_lazy('accounts:reset_done')
    # میاد میگرده ببینه برا این فایل اچ تی ام الی تعریف کردیم یا ن و اون لینک رو برمیدارع میفرسته برا کاربر
    email_template_name = 'accounts/link.html'


# مرحله دوم نشون دادن پیام برای اینکه کاربرایمیلش رو چک کنه
class DonePassword(auth_views.PasswordResetDoneView):
    template_name = 'accounts/done.html'


# حالا کاربر میره به ایمیلاش تا رو لینکی ک ما براش فرستادیم کلیک کنه اینجا لینکو میخایم بسازیم
class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/confirm.html'
    success_url = reverse_lazy('accounts:confirm_done')


#  ی پیام ک میگیم برو لاگین کن
class Complete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/complete.html'
