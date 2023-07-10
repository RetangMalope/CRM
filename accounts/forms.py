from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
    """
    A form used for creating and updating Order instances.

    Inherits from Django's ModelForm class and is associated with the Order model.

    The form includes fields for all the attributes of the Order model.

    Usage:
    form = OrderForm()  # Create a new instance of the form
    form = OrderForm(instance=order)  # Populate the form with existing order data
    form = OrderForm(request.POST, instance=order)  # Bind form data to an existing order instance
    """

    class Meta:
        """
        Inner Meta class that provides metadata for the OrderForm class.

        Specifies the model to be used and the fields to include in the form.
        In this case, all fields of the Order model are included.

        Usage:
        form = OrderForm()  # Create a new instance of the form
        """

        model = Order  # Specifies the model associated with the form
        fields = '__all__'  # Includes all fields of the Order model in the form

