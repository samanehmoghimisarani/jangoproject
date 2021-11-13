from django import forms
from .models import HomeContent


class HomeContentForm(forms.ModelForm):
    class Meta:
        model = HomeContent
        fields = '__all__'

