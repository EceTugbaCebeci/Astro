"""
This module contains views for rendering the index page of the application.
"""

from django.shortcuts import render

def index(request):
    """
    Renders the index page.
    """
    return render(request, 'index.html')
