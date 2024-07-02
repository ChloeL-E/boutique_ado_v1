from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST': # check whether method is POST
        bag = request.session.get('bag', {}) # get the shopping bag

        form_data = { # put the form data into a dictionary
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)  # create an instance of the form using the form_data dictionary above
        if order_form.is_valid(): # if the form is valid, save the order
            order = order_form.save()  # save the order
            for item_id, item_data in bag.items(): # iterate throught the bag items to create each line item
                try:
                    product = Product.objects.get(id=item_id) # first we get the product id out of the bag
                    if isinstance(item_data, int): # then if its an integer we know its an item that doesnt have sizes
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data, # so the quantity will just be the item_data
                        )
                        order_line_item.save()
                    else: # otherwise if the item has sizes...
                        for size, quantity in item_data['items_by_size'].items(): # we'll iterate through each size and create a line item accordingly
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity, # the quantity will be the quantity
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist: # should theroetically never happen but in case a product isnt find, add an error message, delete the empty order and redirect the user to the shopping bag page
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST # attach whether or not the user wants to save their profile info to the session
            return redirect(reverse('checkout_success', args=[order.order_number])) # pass the page 'checkout_success the order number as an argument
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.') # if order form not valid, inform user and redirect to checkout page with form errors shown
    else: # wrap in else block to handle GET requests
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info') # check whether the user wanted to save their profile info by getting the save_info
    order = get_object_or_404(Order, order_number=order_number) # get the order number created in view above and attach success message telling them theyll get an email
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session: # delete the users shopping bag from the session
        del request.session['bag']

    template = 'checkout/checkout_success.html' # set the template and the context
    context = {
        'order': order,
    }

    return render(request, template, context) # render the template