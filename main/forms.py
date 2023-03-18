from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password',)