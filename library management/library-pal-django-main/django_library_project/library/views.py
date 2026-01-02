"""
Views for Library Management System
All views are function-based as per requirement
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Book, IssuedBook
from .forms import StudentLoginForm, BookSearchForm


def student_login(request):
    """
    Login view for students
    Uses Django's built-in authentication
    
    GET: Display login form
    POST: Authenticate and login user
    """
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            # Get username and password from form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate user
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Check if user is superuser (librarian)
                if user.is_superuser:
                    messages.info(request, "Librarians should use the Admin Panel")
                    return redirect('/admin/')
                
                # Login the student
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = StudentLoginForm()
    
    return render(request, 'library/login.html', {'form': form})


def student_logout(request):
    """
    Logout view for students
    Logs out the user and redirects to login page
    """
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect('login')


@login_required
def student_dashboard(request):
    """
    Dashboard for logged-in students
    Shows overview of their borrowed books
    
    Requires: User must be logged in
    """
    # Get books issued to this student that are not returned
    issued_books = IssuedBook.objects.filter(
        student=request.user,
        is_returned=False
    ).select_related('book')
    
    # Count statistics
    total_issued = issued_books.count()
    
    context = {
        'issued_books': issued_books,
        'total_issued': total_issued,
    }
    return render(request, 'library/student_dashboard.html', context)


@login_required
def book_list(request):
    """
    View all available books in the library
    Includes search functionality
    
    Requires: User must be logged in
    """
    # Get search query from GET parameters
    search_form = BookSearchForm(request.GET)
    query = request.GET.get('query', '')
    
    # Get all books
    books = Book.objects.all()
    
    # Filter by search query if provided
    if query:
        # Search in title OR author using Q objects
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    
    context = {
        'books': books,
        'search_form': search_form,
        'query': query,
    }
    return render(request, 'library/book_list.html', context)


@login_required
def my_issued_books(request):
    """
    View books issued to the logged-in student
    Shows both current and returned books
    
    Requires: User must be logged in
    """
    # Get all books issued to this student
    issued_books = IssuedBook.objects.filter(
        student=request.user
    ).select_related('book').order_by('-issue_date')
    
    # Separate current and returned books
    current_books = issued_books.filter(is_returned=False)
    returned_books = issued_books.filter(is_returned=True)
    
    context = {
        'current_books': current_books,
        'returned_books': returned_books,
    }
    return render(request, 'library/issued_books.html', context)
