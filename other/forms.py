from django import forms
from .models import Contact


class SearchProductForm(forms.Form):
    search = forms.CharField(required=False,  max_length=100)


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'
