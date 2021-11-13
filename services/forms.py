from django import forms
from .models import ProductComment


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ('comment', 'name')


class AddReplyForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ('comment', 'name')

