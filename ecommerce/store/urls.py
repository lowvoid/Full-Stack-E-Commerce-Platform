from django.urls import path
from .views import list_product , product_detail , product_search

app_name = 'store'

urlpatterns = [
    path('', list_product , name='products'),
    path('categories/<slug:category_slug>/', list_product , name='categories'),
    path('products/<slug:product_slug>/', product_detail, name='product_detail'),
    path('search/', product_search, name='product_search'),
]

#     path('', home , name='home'),

