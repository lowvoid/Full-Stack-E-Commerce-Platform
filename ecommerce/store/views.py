from django.shortcuts import render , get_object_or_404
from .models import Products , Category
from django.contrib.postgres.search import SearchVector , SearchRank ,SearchQuery
from cart.forms import CartAddProductForm
from django.core.cache import cache
from django.core.paginator import Paginator

# Create your views here.
# def home(request):
#     return render(request, 'store/home.html')


def list_product(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Products.objects.filter(status=Products.Status.AVAILABLE)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    context = {
        'products':  page_obj,
        'category':category,
        'categories':categories,
        'page_obj':page_obj,
    }
    return render(request, 'store/list_product.html',context)


def product_detail(request, product_slug):
    cache_key = f'product_{product_slug}'
    product = cache.get(cache_key)
    if product is None:
        product = get_object_or_404(Products,slug=product_slug, status=Products.Status.AVAILABLE)
        cache.set(cache_key, product, timeout=60*30)
    cart_product_form =  CartAddProductForm()
    context = {
        'detail': product,
        'cart_product_form':cart_product_form
    }
    return render(request, 'store/product_detail.html',context)


def product_search(request):
    query = None
    result = []
    if 'query' in request.GET:
        query = request.GET.get('query')
        search_vector = SearchVector('name', 'description')
        search_query = SearchQuery(query)
        result = Products.objects.annotate(search=search_vector, rank=SearchRank(search_vector,search_query)).filter(search=search_query,status=Products.Status.AVAILABLE).order_by('-rank')

        context = {
            'query':query,
            'results': result
        }
    return render(request, 'store/search.html',context)
