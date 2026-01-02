"""
Models for Library Management System
Defines the database structure for books and issued books
"""

from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Book(models.Model):
    """
    Book model - Stores information about library books
    
    Fields:
        book_id: Auto-generated primary key
        title: Name of the book
        author: Author of the book
        quantity: Number of copies available
    """
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, help_text="Enter the book title")
    author = models.CharField(max_length=100, help_text="Enter the author name")
    quantity = models.PositiveIntegerField(default=1, help_text="Number of copies available")
    
    class Meta:
        ordering = ['title']  # Order books alphabetically by title
    
    def __str__(self):
        """String representation of the book"""
        return f"{self.title} by {self.author}"
    
    def is_available(self):
        """Check if book is available for issue"""
        return self.quantity > 0


class IssuedBook(models.Model):
    """
    IssuedBook model - Tracks which books are issued to which students
    
    Fields:
        book: Reference to the Book being issued
        student: Reference to the User (student) who borrowed the book
        issue_date: Date when book was issued
        return_date: Date when book was returned (null if not returned)
        is_returned: Boolean flag to track return status
    """
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE,  # Delete issued records if book is deleted
        related_name='issued_records',
        help_text="Select the book to issue"
    )
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # Delete issued records if user is deleted
        related_name='borrowed_books',
        help_text="Select the student"
    )
    issue_date = models.DateField(auto_now_add=True, help_text="Date of issue")
    return_date = models.DateField(null=True, blank=True, help_text="Date of return")
    is_returned = models.BooleanField(default=False, help_text="Has the book been returned?")
    
    class Meta:
        ordering = ['-issue_date']  # Most recent issues first
        verbose_name = "Issued Book"
        verbose_name_plural = "Issued Books"
    
    def __str__(self):
        """String representation of the issued book record"""
        status = "Returned" if self.is_returned else "Not Returned"
        return f"{self.book.title} - {self.student.username} ({status})"
    
    def days_kept(self):
        """
        Calculate how many days the book has been kept
        If returned, calculate from issue_date to return_date
        If not returned, calculate from issue_date to today
        """
        if self.is_returned and self.return_date:
            # Book has been returned
            delta = self.return_date - self.issue_date
        else:
            # Book is still with student
            delta = date.today() - self.issue_date
        return delta.days
