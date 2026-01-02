"""
URL configuration for library app
Maps URLs to view functions
"""

from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.student_login, name='login'),  # Login page (home)
    path('logout/', views.student_logout, name='logout'),  # Logout
    
    # Student URLs
    path('dashboard/', views.student_dashboard, name='student_dashboard'),  # Student dashboard
    path('books/', views.book_list, name='book_list'),  # View all books
    path('my-books/', views.my_issued_books, name='my_issued_books'),  # View issued books
]
