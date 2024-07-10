from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm): # create a new class which extends the built in forms.modelform

    class Meta: # meta class which defines the models and fields we want to include
        model = Product
        fields = '__all__' # dunder (double underscore string which will include all the fields)
    
    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)  # replace the image frield with the new one which ustilises the widgey we've created in widgets.py and the template

    def __init__(self, *args, **kwargs): # to make some changes to the fields
        super().__init__(*args, **kwargs) 
        categories = Category.objects.all() # categories to show up in the form using their friendly name in a list of tuples associated with their category id below
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories] # list comprehension- a for loop that adds items to a list

        self.fields['category'].choices = friendly_names  # updated the category field to update with the friendly name rather than the cat id/name field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0' # iterate throught the rest of the fields to set some class on them so they look like the rest of the store design