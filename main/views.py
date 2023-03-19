from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import *

# Create your views here.
def register_user(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = UserRegistrationForm

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

    form = UserLoginForm

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


@login_required(login_url="login")
def dashboard(request):
    total_loan = Loan.total_loan_amount(user=request.user)
    context = {"total_loan": total_loan["total_loan"]}
    return render(request, "dashboard.html", context)


@login_required(login_url="login")
def profile_update(request):
    user = User.objects.get(id=request.user.id)
    form = ProfileUpdateForm(instance=user)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, message="Profile updated successfully")
            return redirect("profile_update")

        messages.success(request, message=form.errors)

    context = {"user": user, "form": form}
    return render(request, "profile_update.html", context)


@login_required(login_url="login")
def view_loans(request):
    form = AddLoanForm

    if request.method == "POST":
        form = AddLoanForm(request.POST)

        if form.is_valid():
            new_loan = form.save(commit=False)
            new_loan.lender = request.user
            new_loan.save()

            messages.success(request, message="Loanee added successfully")
            return redirect("view_loans")

        messages.success(request, message=form.errors)

    loans = Loan.objects.filter(lender=request.user)
    total_loan = Loan.total_loan_amount(user=request.user)
    context = {"loans": loans, "total_loan": total_loan["total_loan"], "form": form}
    return render(request, "loans.html", context)


@login_required(login_url="login")
def search_loans(request):
    form = AddLoanForm

    if request.method == "POST":
        form = AddLoanForm(request.POST)

        if form.is_valid():
            new_loan = form.save(commit=False)
            new_loan.lender = request.user
            new_loan.save()

            messages.success(request, message="Loanee added successfully")
            return redirect("view_loans")

        messages.success(request, message=form.errors)

    borrower = request.GET.get('search')
    loans = Loan.objects.filter(lender=request.user).filter(
        loanee_full_name__icontains=borrower
    )
    total_loan = Loan.total_loan_amount(user=request.user)
    context = {"loans": loans, "total_loan": total_loan["total_loan"], "form": form}
    return render(request, "loans.html", context)


@login_required(login_url="login")
def view_analytics(request):
    return render(request, "analytics.html")
