from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, CategoryDescription, ProductComment
from .forms import AddReplyForm, AddCommentForm
from django.views import View
from django.contrib import messages
from django.db.models import Q
from other.forms import SearchProductForm


def add_reply_product(request, product_id, comment_id):
    product = get_object_or_404(Product, id=product_id)
    comment = get_object_or_404(ProductComment, pk=comment_id)
    if request.method == 'POST':
        form = AddReplyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            reply = ProductComment.objects.create(name=cd['name'], product=product, reply=comment,
                                                  comment=cd['comment'], is_reply = True)
            reply.save()
            return redirect('services:detail_product', product.slug)
    return redirect('services:detail_product', product.slug)


# -------------------------------------------- product ----------------------------------------------- #


class AllProduct(View):
    def get(self, request, slug=None):
        products = Product.objects.all().order_by('-created')
        categories = Category.objects.filter(is_sub=False)
        if slug:
            category = get_object_or_404(Category, slug=slug)
            products = products.filter(category=category)
        form = SearchProductForm(request.GET)
        if 'search' in request.GET:
            if form.is_valid():
                cd = form.cleaned_data
                products = products.filter(Q(title__icontains=cd['search']) | Q(short_description=cd['search']))
                return render(request, 'other/search-result.html', {'form': form, 'products': products})
            messages.error(request, 'please inter valid data', 'error')
            return render(request, 'services/all-product.html', {'form': form})
        context = {'products': products, 'categories': categories, 'form': form}
        return render(request, 'services/all-product.html', context)


class DetailProduct(View):
    form_class = AddCommentForm

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        product.most_visited += 1
        product.save()
        comments = ProductComment.objects.filter(product=product, is_reply=False)
        reply_form = AddReplyForm()
        similar_products = product.tags.similar_objects()
        context = {'product': product, 'similar_products': similar_products, 'comments': comments,
                   'form': self.form_class, 'reply': reply_form}
        return render(request, 'services/detail-product.html', context)

    def post(self,  request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_comment = ProductComment.objects.create(comment=cd['comment'], product=product, name=cd['name'])
            new_comment.save()
            messages.success(request, 'نظر شما با موفقیت اضافه شد')
            return redirect('services:detail_product', product.slug)
        messages.success(request, 'لطفادوباره امتحان کنید')
        return redirect('services:detail_product', product.slug)


# --------------------------------------------- خدمات -------------------------------------


class WebDesign(View):
    def get(self, request):
        products = Product.objects.filter(category__name='طراحی سایت')[:5]
        description = CategoryDescription.objects.get(category__name='طراحی سایت')
        context = {'products': products, 'description': description}
        return render(request, 'services/services.html', context)


class GraphicDesign(View):
    def get(self, request):
        products = Product.objects.filter(category__name='طراحی گرافیکی')[:5]
        description = CategoryDescription.objects.get(category__name='طراحی گرافیکی')
        context = {'products': products, 'description': description}
        return render(request, 'services/services.html', context)


class Translation(View):
    def get(self, request):
        products = Product.objects.filter(category__name='ترجمه')[:5]
        description = CategoryDescription.objects.get(category__name='ترجمه')
        context = {'products': products, 'description': description}
        return render(request, 'services/services.html', context)


class OnlineRegistration(View):
    def get(self, request):
        products = Product.objects.filter(category__name='ثبت نام اینترنتی')[:5]
        description = CategoryDescription.objects.get(category__name='ثبت نام اینترنتی')
        context = {'products': products, 'description': description}
        return render(request, 'services/services.html', context)


class ResearchAndTyping(View):
    def get(self, request):
        products = Product.objects.filter(category__name='تحقیق و تایپ')[:5]
        description = CategoryDescription.objects.get(category__name='تحقیق و تایپ')
        context = {'products': products, 'description': description}
        return render(request, 'services/services.html', context)
