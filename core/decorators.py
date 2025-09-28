from functools import wraps
from django.core.cache import cache
from django.http import HttpResponseTooManyRequests
from django.contrib import messages
from django.shortcuts import redirect
import time

def rate_limit(max_requests=5, window_seconds=300, block_seconds=900):
    """
    Rate limiting decorator for views
    max_requests: Maximum number of requests allowed
    window_seconds: Time window for counting requests
    block_seconds: How long to block after limit exceeded
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Create unique key for this user/IP and view
            if request.user.is_authenticated:
                key = f"rate_limit_{view_func.__name__}_{request.user.id}"
            else:
                key = f"rate_limit_{view_func.__name__}_{request.META.get('REMOTE_ADDR')}"
            
            # Check if user is currently blocked
            block_key = f"{key}_blocked"
            if cache.get(block_key):
                messages.error(request, "Too many attempts. Please try again later.")
                return redirect('index')
            
            # Get current request count
            current_requests = cache.get(key, 0)
            
            if current_requests >= max_requests:
                # Block the user
                cache.set(block_key, True, block_seconds)
                cache.delete(key)  # Reset counter
                messages.error(request, f"Too many attempts. Please wait {block_seconds//60} minutes before trying again.")
                return redirect('index')
            
            # Increment counter
            cache.set(key, current_requests + 1, window_seconds)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator