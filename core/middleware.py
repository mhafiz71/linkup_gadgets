from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware:
    """
    Custom middleware to handle common errors gracefully
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """
        Handle exceptions that occur during request processing
        """
        logger.error(f"Unhandled exception: {exception}", exc_info=True)
        
        # For AJAX requests, return JSON error
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'error': 'An unexpected error occurred. Please try again.',
                'success': False
            }, status=500)
        
        # For regular requests, show error page with message
        messages.error(request, 'An unexpected error occurred. Please try again.')
        return render(request, 'core/error.html', {
            'error_message': 'Something went wrong. Our team has been notified.'
        }, status=500)