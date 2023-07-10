from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def login_user(request):
    """
    Authenticates and logs in a user.

    If the request method is POST, retrieves the username and password from the request.
    Attempts to authenticate the user using the provided credentials.
    If authentication is successful, logs in the user and redirects to the home page.
    If authentication fails, displays an error message and redirects to the login page.

    If the request method is GET, renders the login page.

    Usage:
    - To handle a login form submission:
      login_user(request)

    - To render the login page:
      return render(request, 'authenticate/login.html', {})
    """

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ('Invalid username or password'))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    """
    Logs out a user.

    Logs out the currently authenticated user and displays a success message.
    Redirects to the login page.

    Usage:
    logout_user(request)
    """

    logout(request)
    messages.success(request, 'You were logged out')
    return redirect('login')


def register_user(request):
    """
    Registers a new user.

    If the request method is POST, creates a new UserCreationForm instance with the request data.
    If the form is valid, saves the form and logs in the newly registered user.
    Displays a success message and redirects to the login page.

    If the request method is GET, renders the register_user page.

    Usage:
    - To handle a user registration form submission:
      register_user(request)

    - To render the registration page:
      return render(request, 'authenticate/register_user.html', {'form': form})
    """

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have registered successfully'))
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'authenticate/register_user.html', {'form': form})
