"""
Test settings for portfolio project.
This file contains settings optimized for running tests.
"""

from .settings import *
import tempfile

# Override settings for testing
DEBUG = True

# Use in-memory SQLite database for faster tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


# Disable migrations for faster tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Use temporary directory for media files during tests
MEDIA_ROOT = tempfile.mkdtemp()

# Disable external API calls during tests
GEMINI_API_KEY = "test-gemini-key"

# Email backend for testing
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Password hashers for faster tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable caching during tests
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Logging configuration for tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# Static files for testing
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Secret key for testing
SECRET_KEY = "test-secret-key-not-for-production-use-only"

# Allowed hosts for testing
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]

# Disable HTTPS redirect in tests
SECURE_SSL_REDIRECT = False

# Test-specific app settings
TINYMCE_API_KEY = "test-tinymce-key"
