from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm # from profiles/forms.py

from checkout.models import Order # import the Order model so that we can use the order in the order_history view

def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST': # the POST handler for the profile view
        form = UserProfileForm(request.POST, instance=profile) # create a new instance of the user profile for m using the POST data, the instance is the profile object from above
        if form.is_valid(): # if form is valid
            form.save() # save the form
            messages.success(request, 'Profile updated successfully') # success message

    form = UserProfileForm(instance=profile)  # populate the form with the users current profile info
    orders = profile.orders.all() # get all users order history

    template = 'profiles/profile.html'
    context = {
        'form': form,   # return form to the template
        'orders': orders, # return orders to the template
        'on_profile_page': True, # to ensure the bag isnt included in the success message on the prolie page when userprofile form updated
    }

    return render(request, template, context)


def order_history(request, order_number): # take in the order number as a parmaeter
    order = get_object_or_404(Order, order_number=order_number) # get the order 

    messages.info(request, ( # message to inform user they are looking at a past order confirmation
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html' # uses the checkout_success template
    context = {
        'order': order,
        'from_profile': True, # check in the template if the user got to the template via the order history view
    }

    return render(request, template, context)