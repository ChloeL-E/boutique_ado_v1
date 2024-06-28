from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    '''
    A view that renders the shoppping bag contents page
    '''
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id): # form to add_to_bag in product_details.html submits to this view to add product to shopping bag. Takes item_id and quantity(below)
    '''
    Add a quantity of the specified product to the shopping bag.
    Once in the view will get the bag variable if it exists in session or create if it doesnt.
    Add the item to the bag or update the quanitty if item already exists. Update variable bag in session. Redirect to redirect_url.
    '''

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # to store the contents of the shopping bag in the http so the contents persist whilst the user shops within site withou losing ocontent of bag
    bag = request.session.get('bag', {}) #  variable to access the requests session, trying to get the variable 'bag' if it already exists or initializing to an empty dictionary if none exists

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
    
    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)