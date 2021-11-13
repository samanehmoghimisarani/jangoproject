from django.shortcuts import render
from django.views import View
from .models import HomeContent


class Home(View):
    def get(self, request):
        home_content = HomeContent.objects.last()
        context = {'home_content': home_content}
        return render(request, 'core/home.html', context)

