from django.contrib import admin
from .models import Product, Category

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )
#  ordering by 'sku', must be a tuple as possible to sort on multiple cols. to reverse order put - in front of 'sku'
    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin): #  extends the built in ModelAdmin class
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)