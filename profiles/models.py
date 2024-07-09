from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save # in order for reciever to work
from django.dispatch import receiver # in order for reciever to work

from django_countries.fields import CountryField # as using a country filed in the UserProfile


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE) # just like a FK but says that each user can only have one profile and each profile can only have one user
    default_phone_number = models.CharField(max_length=20, null=True, blank=True) # all below taken from Order model
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True) 
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True) # null and blank=true means theyre optional

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User) # only one signal so just putting it at the bottom of thisrather than in a signal.py file
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile 
    """
    if created:
        UserProfile.objects.create(user=instance) # create a new instance when a user creates a new profile
    # Existing users: just save the profile when user updates it
    instance.userprofile.save()
