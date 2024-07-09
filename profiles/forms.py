# similar to checkout forms.py- copied and pasted and models and classes renamed
from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs) # call the default __init__ method to set the form up as it would be by default
        placeholders = { # created a dictionary of placeholders that will appear in form fields rather than clunky looking placeholder and empty text boxes in the template
            'default_phone_number': 'Phone Number', # removed name and email placeholders as don't exist on UserProfile model
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True  # cursor will start in the full name field when user comes to page
        for field in self.fields: # iterate through form fields
            if field != 'default_country': # as don't need a placeholder in this dropdown 
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *' # add an asterix to all form fields set to required on the model
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder # setting all the placeholder attributed to the value in the dictionary above
                self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input' # adding a css class
                self.fields[field].label = False # removing the form fields labels as the placeholders are now set