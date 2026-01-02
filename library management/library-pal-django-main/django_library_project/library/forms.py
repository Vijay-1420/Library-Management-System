"""
Forms for Library Management System
Handles user input validation
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm


class StudentLoginForm(AuthenticationForm):
    """
    Custom login form for students
    Uses Django's built-in AuthenticationForm with custom styling
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })
    )


class BookSearchForm(forms.Form):
    """
    Form for searching books by title or author
    """
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by book title or author...',
        })
    )
