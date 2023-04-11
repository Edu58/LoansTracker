from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db.models import Sum
from datetime import datetime


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide a valid email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.email


class Loan(models.Model):
    lender = models.ForeignKey(User, on_delete=models.CASCADE)
    loanee_full_name = models.CharField(max_length=250)
    loanee_email = models.EmailField(blank=True)
    loan_amount = models.FloatField()
    # interest_rate = models.FloatField(default=0)
    from_date = models.DateField()
    to_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    loan_status = models.BooleanField(default=False)
    notify_loanee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.loanee_full_name

    @classmethod
    def get_current_user_loans(cls, user):
        """Get current logged in user loans

        Args:
            user (User): A User instance

        Returns:
            Queryset : A Queryset with loans belonging to the current logged in user
        """
        loans = cls.objects.filter(lender=user)
        return loans

    @classmethod
    def get_user_current_month_loans(cls, user):
        """Get current month user loans

        Args:
            user (User): A User instance

        Returns:
            Queryset : A Queryset with the current month loans belonging to the current logged in user
        """
        today = datetime.now()
        current_month = today.month
        loans = cls.objects.filter(lender=user).filter(created_at__month=current_month)
        return loans

    @classmethod
    def total_loan_amount(cls, user):
        """Total loan amount for the current logged in user

        Args:
            user (User): A User instance

        Returns:
            Queryset : A Queryset with the Total loan amount for the current logged in user
        """
        total = cls.objects.filter(lender=user).aggregate(total_loan=Sum("loan_amount"))
        return total
