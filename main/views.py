from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, UserLoginForm

# Create your views here.
def register_user(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, message="Registered successfully. Please Log In")
            return redirect("login")

        messages.warning(request, form.errors)

    context = {"form": form}
    return render(request, "register.html", context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = UserLoginForm()

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.warning(
            request, message="User with provided credentials does not exist!"
        )

    messages.warning(request, message=form.errors)

    context = {"form": form}
    return render(request, "login.html", context)


@login_required(login_url="login")
def logout_user(request):
    logout(request)
    return redirect("login")


def dashboard(request):
    return render(request, "dashboard.html")


# def loans(request):

