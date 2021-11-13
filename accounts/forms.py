from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='confirm_password')

    class Meta:
        model = User
        fields = ('username', 'name', 'family', 'email', 'phone')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('please enter true password')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()  # برای اینکه پسورد رو هش شده ببینیم

    class Meta:
        model = User
        fields = ('username', 'name', 'family', 'email', 'phone')

    def clean_password(self):
        return self.initial['password']

# __________________________________________________________________________________


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    name = forms.CharField(max_length=50, required=False)
    family = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(max_length=100, required=False)
    phone = forms.CharField(max_length=11, required=False)
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='confirm_password')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password2'] and cd['password'] != cd['password2']:
            raise forms.ValidationError('please enter true password')
        return cd['password2']


class ChangeProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'username', 'name', 'family', 'phone')

