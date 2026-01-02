"""
App configuration for library app
"""

from django.apps import AppConfig


class LibraryConfig(AppConfig):
    """Configuration for Library app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'
    verbose_name = 'Library Management'
