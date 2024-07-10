from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),  # product id should be an integer. Django will always use the first url it finds to match the pattern for
    path('add/', views.add_product, name='add_product'),
]
