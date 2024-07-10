from django.forms.widgets import ClearableFileInput  # access to the django ClearableFileInput class which affects the image inout on the forms
from django.utils.translation import gettext_lazy as _  # the as _ acts as an alias so we can call the gettext_lazy() using _(). Using this import to keep the customs classes as close to the django original


class CustomClearableFileInput(ClearableFileInput): # inherits the built in django 'ClearableFileInput' class
    clear_checkbox_label = _('Remove')  # overriding these inputs with our own values
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'