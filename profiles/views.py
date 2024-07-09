from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm # from profiles/forms.py

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
