from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import ValidationError


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides better error messages
    and proper HTTP status codes.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Now add custom handling
    if response is not None:
        custom_response_data = {
            'error': {
                'status_code': response.status_code,
                'message': 'An error occurred',
                'details': {}
            }
        }

        # Handle validation errors
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_response_data['error']['message'] = 'Validation error'
            if isinstance(response.data, dict):
                custom_response_data['error']['details'] = response.data
            else:
                custom_response_data['error']['details'] = {'non_field_errors': response.data}

        # Handle not found errors
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_response_data['error']['message'] = 'Resource not found'
            custom_response_data['error']['details'] = {'detail': 'The requested resource does not exist'}

        # Handle permission denied
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_response_data['error']['message'] = 'Permission denied'
            custom_response_data['error']['details'] = {'detail': 'You do not have permission to perform this action'}

        # Handle unauthorized
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_response_data['error']['message'] = 'Authentication required'
            custom_response_data['error']['details'] = {'detail': 'Authentication credentials were not provided'}

        response.data = custom_response_data

    return response

