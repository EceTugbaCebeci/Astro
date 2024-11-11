from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        }),
        help_text="Enter your first name."
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        }),
        help_text="Enter your last name."
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        }),
        help_text="Enter a unique username. Only letters and numbers are allowed."
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }),
        help_text="Enter a valid email address."
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }),
        help_text="The password must be at least 8 characters."
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-Type Password'
        }),
        help_text="Enter the same password as before, for verification."
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Birth Date'
        }),
        help_text="Select your birth date."
    )
    birth_hour = forms.ChoiceField(
        choices=[(str(i), f"{i:02d}:00") for i in range(24)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select your birth hour."
    )
    birth_country = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_birth_country'}),
        help_text="Select your birth country."
    )
    birth_place = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_birth_place'}),
        help_text="Select your birth place."
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2',
                  'birth_date', 'birth_hour', 'birth_country', 'birth_place']
        

