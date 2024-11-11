from django import forms
from .models import Relative
from .models import AskAstroQuestion
from django.contrib.auth.models import User


class RelativeForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=[
            ('Parent', 'Parent'),
            ('Sibling', 'Sibling'),
            ('Spouse', 'Spouse'),
            ('Friend', 'Friend'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select the relative's role."
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        }),
        help_text="Enter the relative's first name."
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        }),
        help_text="Enter the relative's last name."
    )
    gender = forms.ChoiceField(
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other')
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select the relative's gender."
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Birth Date'
        }),
        help_text="Select the relative's birth date."
    )
    birth_hour = forms.ChoiceField(
        choices=[(str(i), f"{i:02d}:00") for i in range(24)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select the relative's birth hour."
    )
    birth_country = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_birth_country'}),
        help_text="Select the relative's birth country."
    )
    birth_place = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_birth_place'}),
        help_text="Select the relative's birth place."
    )

    class Meta:
        model = Relative
        fields = ['first_name', 'last_name', 'gender','birth_date', 'birth_hour', 'birth_country', 'birth_place', 'role']


class AskAstroQuestionForm(forms.ModelForm):
    class Meta:
        model = AskAstroQuestion
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ask your question...'}),
        }


from django import forms
from django.contrib.auth.models import User

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        help_text="Enter your first name."
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        help_text="Enter your last name."
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'readonly': 'readonly'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'readonly': 'readonly'}),
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Birth Date'}),
        help_text="Select your birth date."
    )
    birth_hour = forms.ChoiceField(
        choices=[(str(i), f"{i:02d}:00") for i in range(24)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select your birth hour."
    )
    birth_place = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_birth_place'}),
        help_text="Select your birth place."
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'birth_date', 'birth_hour', 'birth_place']


class UpdatePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'}),
        required=False,
        help_text="Enter your current password."
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        required=False,
        help_text="Enter a new password."
    )
    new_password_again = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        required=False,
        help_text="Enter the same password as before, for verification."
    )