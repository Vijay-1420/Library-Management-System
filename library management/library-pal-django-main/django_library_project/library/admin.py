"""
Admin configuration for Library Management System
Registers models with Django Admin for librarian access
"""

from django.contrib import admin
from django.contrib import messages
from datetime import date
from .models import Book, IssuedBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for Book model
    Librarian can add, edit, delete books from here
    """
    # Fields to display in the list view
    list_display = ('book_id', 'title', 'author', 'quantity', 'availability_status')
    
    # Fields to search
    search_fields = ('title', 'author')
    
    # Fields to filter by
    list_filter = ('author',)
    
    # Fields that can be edited directly in list view
    list_editable = ('quantity',)
    
    # Order of fields in the form
    fields = ('title', 'author', 'quantity')
    
    def availability_status(self, obj):
        """Display availability status"""
        if obj.quantity > 0:
            return f"✓ Available ({obj.quantity})"
        return "✗ Not Available"
    availability_status.short_description = 'Availability'


@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    """
    Admin configuration for IssuedBook model
    Librarian can issue and return books from here
    """
    # Fields to display in the list view
    list_display = ('book', 'student', 'issue_date', 'return_date', 'is_returned', 'days_kept_display')
    
    # Fields to search
    search_fields = ('book__title', 'student__username')
    
    # Fields to filter by
    list_filter = ('is_returned', 'issue_date')
    
    # Read-only fields
    readonly_fields = ('issue_date',)
    
    # Fields in the form
    fields = ('book', 'student', 'issue_date', 'is_returned', 'return_date')
    
    # Custom actions
    actions = ['mark_as_returned']
    
    def days_kept_display(self, obj):
        """Display number of days the book has been kept"""
        days = obj.days_kept()
        if days == 0:
            return "Today"
        elif days == 1:
            return "1 day"
        else:
            return f"{days} days"
    days_kept_display.short_description = 'Days Kept'
    
    def save_model(self, request, obj, form, change):
        """
        Override save to handle quantity changes
        - Reduce quantity when book is issued
        - Increase quantity when book is returned
        """
        if not change:  # New issue
            # Check if book is available
            if obj.book.quantity <= 0:
                messages.error(request, f"Cannot issue '{obj.book.title}' - No copies available!")
                return
            # Reduce book quantity
            obj.book.quantity -= 1
            obj.book.save()
            messages.success(request, f"Book '{obj.book.title}' issued to {obj.student.username}")
        else:  # Updating existing record
            # Check if book is being returned
            old_obj = IssuedBook.objects.get(pk=obj.pk)
            if obj.is_returned and not old_obj.is_returned:
                # Book is being returned - increase quantity
                obj.return_date = date.today()
                obj.book.quantity += 1
                obj.book.save()
                messages.success(request, f"Book '{obj.book.title}' returned by {obj.student.username}")
        
        super().save_model(request, obj, form, change)
    
    @admin.action(description="Mark selected books as returned")
    def mark_as_returned(self, request, queryset):
        """Bulk action to mark books as returned"""
        for issued_book in queryset.filter(is_returned=False):
            issued_book.is_returned = True
            issued_book.return_date = date.today()
            issued_book.book.quantity += 1
            issued_book.book.save()
            issued_book.save()
        messages.success(request, f"Marked {queryset.count()} books as returned")


# Customize Admin Site Header
admin.site.site_header = "Library Management System"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Welcome to Library Administration"
