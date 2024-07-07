from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs) # call the default __init__ method to set the form up as it would be by default
        placeholders = { # created a dictionary of placeholders that will appear in form fields rather than clunky looking placeholder and empty text boxes in the template
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True  # cursor will start in the full name field when user comes to page
        for field in self.fields: # iterate through form fields
            if field != 'country': # as don't need a placeholder in this dropdown 
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *' # add an asterix to all form fields set to required on the model
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder # setting all the placeholder attributed to the value in the dictionary above
                self.fields[field].widget.attrs['class'] = 'stripe-style-input' # adding a css class
                self.fields[field].label = False # removing the form fields labels as the placeholders are now set