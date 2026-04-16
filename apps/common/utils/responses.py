from rest_framework.response import Response
from rest_framework import status as http_status


def format_serializer_errors(errors):
    """
    Transform serializer errors from DRF format to flat error format.
    
    Converts from:
        {"field": ["error message 1", "error message 2"]}
    
    To:
        {"field": "error message 1"}
    
    Also handles non_field_errors by converting them to a generic message.
    """
    formatted_errors = {}
    
    for field, error_list in errors.items():
        if isinstance(error_list, list) and error_list:
            # Get the first error message
            formatted_errors[field] = str(error_list[0])
        else:
            formatted_errors[field] = str(error_list)
    
    return formatted_errors


def success_response(data=None, message="Success", status=http_status.HTTP_200_OK):
    """
    Standard success response format
    
    Response format:
    {
        "status": true,
        "message": "Success message",
        "results": {...}
    }
    """
    return Response(
        {
            "status": True,
            "message": message,
            "results": data
        },
        status=status
    )


def error_response(message="Error", errors=None, status=http_status.HTTP_400_BAD_REQUEST):
    """
    Standard error response format
    
    Response format:
    {
        "status": false,
        "message": "Error message",
        "errors": {...}
    }
    """
    # Format serializer errors if provided
    if errors:
        errors = format_serializer_errors(errors)
    
    return Response(
        {
            "status": False,
            "message": message,
            "errors": errors
        },
        status=status
    )