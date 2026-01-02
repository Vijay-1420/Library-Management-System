"""
URL configuration for library_system project.
Main URL routing - includes admin and library app URLs
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin Panel - Librarian access
    path('admin/', admin.site.urls),
    
    # Library app URLs - Student access
    path('', include('library.urls')),
]
