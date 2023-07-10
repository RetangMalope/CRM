from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from . models import *
from . forms import OrderForm
# Create your views here.


def home(request):
    """
    Renders the home/dashboard page.

    Retrieves the last 5 orders and all customers from the database.
    Counts the total number of customers, total orders, delivered orders, and pending orders.
    Passes the retrieved data and counts to the template for rendering.

    Args:
        request: HttpRequest object representing the request made to the server.

    Returns:
        HttpResponse object representing the rendered HTML template.
    """
    orders = Order.objects.order_by('-date_created')[:5]  # Retrieve the last 5 orders
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = Order.objects.count()
    delivered = Order.objects.filter(status='Delivered').count()
    pending = Order.objects.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    """
    Renders the products page.

    Retrieves all products from the database.
    Passes the retrieved products to the template for rendering.

    Args:
        request: HttpRequest object representing the request made to the server.

    Returns:
        HttpResponse object representing the rendered HTML template.
    """
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customers(request, pk):
    """
    Renders the customer details page.

    Retrieves the customer with the specified primary key (pk) from the database.
    Retrieves all orders associated with the customer.
    Counts the total number of orders.
    Passes the retrieved customer, orders, and order count to the template for rendering.

    Args:
        request: HttpRequest object representing the request made to the server.
        pk: Primary key of the customer.

    Returns:
        HttpResponse object representing the rendered HTML template.
    """
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer': customer, 'orders': orders, 'order_count': order_count}
    return render(request, 'accounts/customer.html', context)

def createOrder(request, pk):
    """
    Renders the order creation form page and handles form submission.

    Retrieves the customer with the specified primary key (pk) from the database.
    Initializes an OrderForm with the initial value of the customer field.
    If the request method is POST, validates the submitted form data and saves the order.
    Redirects to the home/dashboard page upon successful form submission.

    Args:
        request: HttpRequest object representing the request made to the server.
        pk: Primary key of the customer.

    Returns:
        HttpResponse object representing the rendered HTML template or redirect response.
    """
    customer = Customer.objects.get(id = pk)
    form = OrderForm(initial = {'customer': customer})
    if request.method == "POST":
        
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)




def updateOrder(request, pk):
    """
    Renders the order update form page and handles form submission.

    Retrieves the order with the specified primary key (pk) from the database.
    Initializes an OrderForm with the instance of the retrieved order.
    If the request method is POST, validates the submitted form data and updates the order.
    Redirects to the home/dashboard page upon successful form submission.

    Args:
        request: HttpRequest object representing the request made to the server.
        pk: Primary key of the order.

    Returns:
        HttpResponse object representing the rendered HTML template or redirect response.
    """
    order = Order.objects.get(id = pk)
    form = OrderForm(instance = order)

    if request.method == "POST":
        form = OrderForm(request.POST, isinstance)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)



def DeleteOrder(request, pk):
    """
    Renders the order deletion confirmation page and handles form submission.

    Retrieves the order with the specified primary key (pk) from the database.
    If the request method is POST, deletes the order.
    Redirects to the home/dashboard page upon successful order deletion.

    Args:
        request: HttpRequest object representing the request made to the server.
        pk: Primary key of the order.

    Returns:
        HttpResponse object representing the rendered HTML template or redirect response.
    """
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('home')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)