from django.shortcuts import get_object_or_404
from .models import News, NewsComment, Contact
from services.models import Product
from django.db.models import Q
from services.forms import AddCommentForm, AddReplyForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import SearchProductForm, ContactForm


# ____________________________________________ NEWS ___________________________________________ #


class AllNews(View):
    def get(self, request):
        news = News.objects.order_by('-created')
        form = SearchProductForm(request.GET)
        if 'search' in request.GET:
            if form.is_valid():
                cd = form.cleaned_data
                news = news.filter(title__icontains=cd['search'])
                return render(request, 'other/search-result.html', {'form': form, 'news': news})
            messages.error(request, 'لطفا اطلاعات معتبر وارد کنید', 'error')
            return render(request, 'other/all-news.html', {'form': form, 'news': news})
        return render(request, 'other/all-news.html', {'form': form, 'news': news})


class DetailNews(View):
    template_name = 'other/detail-news.html'
    form_class = AddCommentForm

    def get(self, request, slug):
        news = get_object_or_404(News, slug=slug)
        news.most_visited += 1
        news.save()
        comments = NewsComment.objects.filter(news=news, is_reply=False)
        reply_form = AddReplyForm()
        similar_news = news.tags.similar_objects()
        return render(request, self.template_name, {'news': news, 'similar_news': similar_news, 'comments': comments,
                                                    'form': self.form_class, 'reply': reply_form})

    def post(self,  request, slug):
        news = get_object_or_404(News, slug=slug)
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_comment = NewsComment.objects.create(comment=cd['comment'], news=news, name=cd['name'])
            new_comment.save()
            messages.success(request, 'نظر شما با موفقیت اضافه شد')
            return redirect('other:detail_news', news.slug)
        messages.success(request, 'لطفادوباره امتحان کنید')
        return redirect('other:detail_news', news.slug)


def add_reply_news(request, news_id, comment_id):
    news = get_object_or_404(News, id=news_id)
    comment = get_object_or_404(NewsComment, id=comment_id)
    if request.method == 'POST':
        form = AddReplyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            reply = NewsComment.objects.create(name=cd['name'], news=news, reply=comment, comment=cd['comment'],
                                               is_reply=True).save()
            return redirect('other:detail_news', news.slug)
    return redirect('other:detail_news', news.slug)
# ____________________________________________ SORT ___________________________________________ #


class SortByDate(View):
    def get(self, request):
        products = Product.objects.order_by('-updated')
        form = SearchProductForm(request.GET)
        if 'search' in request.GET:
            if form.is_valid():
                cd = form.cleaned_data
                products = products.filter(Q(title__icontains=cd['search']) | Q(short_description=cd['search']))
                return render(request, 'other/search-result.html', {'form': form, 'products': products})
            messages.error(request, 'please inter valid data', 'error')
            return render(request, 'services/all-product.html', {'form': form})
        context = {'products': products, 'form': form}
        return render(request, 'services/all-product.html', context)


class SortProductByMustVisit(View):      # پر بازدید ترین
    def get(self, request):
        products = Product.objects.order_by('-most_visited')
        form = SearchProductForm(request.GET)
        if 'search' in request.GET:
            if form.is_valid():
                cd = form.cleaned_data
                products = products.filter(Q(title__icontains=cd['search']) | Q(short_description=cd['search']))
                return render(request, 'other/search-result.html', {'form': form, 'products': products})
            messages.error(request, 'please inter valid data', 'error')
            return render(request, 'services/all-product.html', {'form': form})
        context = {'products': products, 'form': form}
        return render(request, 'services/all-product.html', context)


class SortByLowestPrice(View):
    def get(self, request):
        products = Product.objects.order_by('price')
        form = SearchProductForm(request.GET)
        if 'search' in request.GET:
            if form.is_valid():
                cd = form.cleaned_data
                products = products.filter(Q(title__icontains=cd['search']) | Q(short_description=cd['search']))
                return render(request, 'other/search-result.html', {'form': form, 'products': products})
            messages.error(request, 'please inter valid data', 'error')
            return render(request, 'services/all-product.html', {'form': form})
        context = {'products': products, 'form': form}
        return render(request, 'services/all-product.html', context)

# ____________________________________________ SEARCH ___________________________________________ #


class SearchProduct(View):
    def get(self, request):
        products = Product.objects.all()
        form = SearchProductForm
        if 'search' in request.GET:
            if form.is_valid():
                cd = form.cleaned_data
                products = products.filter(Q(title__icontains=cd['search']) | Q(short_description__icontains=cd['search']))
                return render(request, 'other/search-result.html', {'form': form, 'products': products})
            messages.error(request, 'please inter valid data', 'error')
            return render(request, 'services/all-product.html', {'form': form})
        return render(request, 'services/all-product.html', {'form': form})


class SearchResult(View):
    def get(self, request):
        return render(request, 'other/search-result.html')

# ____________________________________________ Other ___________________________________________ #


class FreeProduct(View):
    def get(self, request):
        products = Product.objects.filter(price=0)
        form = SearchProductForm(request.GET)
        if 'search' in request.GET:
            if form.is_valid():
                cd = form.cleaned_data
                products = products.filter(Q(title__icontains=cd['search']) | Q(short_description=cd['search']))
                return render(request, 'other/search-result.html', {'form': form, 'products': products})
            messages.error(request, 'please inter valid data', 'error')
            return render(request, 'services/all-product.html', {'form': form})
        context = {'products': products, 'form': form}
        return render(request, 'services/all-product.html', context)


# ____________________________________________ CONTACT ___________________________________________ #


class ContactUs(View):
    template_name = 'other/cantact-us.html'
    form_class = ContactForm

    def get(self, request):
        contact = Contact.objects.last()
        return render(request, self.template_name, {'contact': contact, 'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'پیام شما با موفقیت ارسال به زودی پاسخ شماراخواهیم داد', 'success')
            return redirect('other:contact_us')
        messages.error(request, 'لطفا اطلاعات معتبر وارد کنید', 'error')
        return redirect('other:contact_us')


# ____________________________________________ SORT BY ___________________________________________ #


class SortNewsByDate(View):
    def get(self, request):
        news = News.objects.order_by('-updated')
        form = SearchProductForm(request.GET)
        if 'search' in request.GET:
            if form.is_valid():
                cd = form.cleaned_data
                news = news.filter(title__icontains=cd['search'])
                return render(request, 'other/search-result.html', {'form': form, 'news': news})
            messages.error(request, 'لطفا اطلاعات معتبر وارد کنید', 'error')
            return render(request, 'other/all-news.html', {'form': form})
        context = {'news': news, 'form': form}
        return render(request, 'other/all-news.html', context)


class SortNewsByMustVisit(View):      # پر بازدید ترین
    def get(self, request):
        news = News.objects.order_by('-most_visited')
        form = SearchProductForm(request.GET)
        if 'search' in request.GET:
            if form.is_valid():
                cd = form.cleaned_data
                news = news.filter(title__icontains=cd['search'])
                return render(request, 'other/search-result.html', {'form': form, 'news': news})
            messages.error(request, 'لطفا اطلاعات معتبروارد کنید', 'error')
            return render(request, 'other/all-news.html', {'form': form})
        context = {'news': news, 'form': form}
        return render(request, 'other/all-news.html', context)


class SearchNews(View):
    def get(self, request):
        news = News.objects.all()
        form = SearchProductForm
        if 'search' in request.GET:
            if form.is_valid():
                cd = form.cleaned_data
                news = news.filter(title__icontains=cd['search'])
                return render(request, 'other/search-result.html', {'form': form, 'news': news})
            messages.error(request, 'لطفا اطلاعات معتبر وارد کنید', 'error')
            return render(request, 'other/all-news.html', {'form': form, 'news': news})
        return render(request, 'other/all-news.html', {'form': form, 'news': news})





