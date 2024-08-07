from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name' #  this means the sort key becomes the category name
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'  # reverses the direction
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


# for store owners..
@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:  # to ensure only shop owner i.e superuser can add products
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))  # redirect to home page with error message

    if request.method == 'POST':  
        form = ProductForm(request.POST, request.FILES) # create a new instance of the product form from request.POSt and include request.files to ensure we capture the image of the product if one was submitted
        if form.is_valid():
            product = form.save()  # if form is valid, save to new variable and add success message
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))  # redirect to the product details page using the product variable above
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')  # if any form errors attach an error message asking user to recheck the form
    else:
        form = ProductForm()  # render an empty instance of the form
    template = 'products/add_product.html' # use the add product template
    context = { # includes a context including the product form
        'form': form,
    }

    return render(request, template, context) 


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:  # to ensure only shop owner i.e superuser can add products
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))  # redirect to home page with error message
        
    product = get_object_or_404(Product, pk=product_id) # get the product by id
    if request.method == 'POST': 
        form = ProductForm(request.POST, request.FILES, instance=product) # instanciate a form and tell it that the instance is using the product obtained above
        if form.is_valid():  # if valid, save and add success message
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id])) # redirect to product detail page using product id
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.') # otherwise error message
    else:
        form = ProductForm(instance=product) # instance of the product form using the product
        messages.info(request, f'You are editing {product.name}') # message informing user they are editing a product

    template = 'products/edit_product.html' # tell it which template to use
    context = {  
        'form': form,
        'product': product, # which products to go in the template
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:  # to ensure only shop owner i.e superuser can add products
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))  # redirect to home page with error message

    product = get_object_or_404(Product, pk=product_id) # get product by id
    product.delete() # delete
    messages.success(request, 'Product deleted!') # successful deletion
    return redirect(reverse('products')) # redirect to products page