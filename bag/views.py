from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.

def view_bag(request):
    '''
    A view that renders the shoppping bag contents page
    '''
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id): # form to add_to_bag in product_details.html submits to this view to add product to shopping bag. Takes item_id and quantity(below)
    '''
    Add a quantity of the specified product to the shopping bag.
    The function retrieves the item quantity, redirect URL, and optionally the size from the POST request.
    It checks the session for an existing shopping bag or creates a new one if none exists.
    It updates the shopping bag with the specified item and quantity, handling items with and without sizes.
    The updated shopping bag is saved back into the session.
    The user is redirected to the specified URL.
    '''

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # to store the contents of the shopping bag in the http so the contents persist whilst the user shops within site without losing content of bag
    bag = request.session.get('bag', {}) #  variable to access the requests session, trying to get the variable 'bag' if it already exists or initializing to an empty dictionary if none exists

    if size:
        if item_id in list(bag.keys()):  #  Item Exists: If the item with the given item_id already exists in the bag:
            if size in bag[item_id]['items_by_size'].keys():  # Size Exists: If the specific size of the item exists, increment the quantity.
                bag[item_id]['items_by_size'][size] += quantity
            else:  # Size Doesn't Exist: Add the size and set the quantity.
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}  # Item Doesn't Exist: Create a new entry for the item with the specified size and quantity.
    else:  # without size
        if item_id in list(bag.keys()):  # Item Exists: If the item exists in the bag, simply increment the quantity.
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity  # Item Doesn't Exist: Add the item with the specified quantity.
    
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id): 
    '''
    Adjust the quantity of the specified product to the specified amount
    '''

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # to store the contents of the shopping bag in the http so the contents persist whilst the user shops within site without losing content of bag
    bag = request.session.get('bag', {}) #  variable to access the requests session, trying to get the variable 'bag' if it already exists or initializing to an empty dictionary if none exists

    if size:
        if quantity > 0:
            bag[item_id]["items_by_size"][size] = quantity
        else:
            del bag[item_id]["items_by_size"][size]
            if not bag[item_id]["items_by_size"]:
                bag.pop(item_id)
    else:  # without size
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)  # Item Doesn't Exist: Add the item with the specified quantity.
    
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id): 
    '''
    Adjust the quantity of the specified product to the specified amount
    '''

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
     # to store the contents of the shopping bag in the http so the contents persist whilst the user shops within site without losing content of bag
        bag = request.session.get('bag', {}) #  variable to access the requests session, trying to get the variable 'bag' if it already exists or initializing to an empty dictionary if none exists

        if size:
            del bag[item_id]["items_by_size"][size]
            if not bag[item_id]["items_by_size"]:
                bag.pop(item_id)
            else:
                bag.pop(item_id)  # Item Doesn't Exist: Add the item with the specified quantity.
    
        request.session['bag'] = bag
        return HttpResponse(status=200)
    
    except Exception as e:
        return HttpResponse(status=500)