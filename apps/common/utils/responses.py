from rest_framework.response import Response
from rest_framework import status as http_status


def success_response(data=None, message="Success", status=http_status.HTTP_200_OK):
    """
    Standard success response format
    
    Response format:
    {
        "status": true,
        "message": "Success message",
        "data": {...}
    }
    """
    return Response(
        {
            "status": True,
            "message": message,
            "data": data
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
        "data": {
            "errors": {...}
        }
    }
    """
    return Response(
        {
            "status": False,
            "message": message,
            "data": {
                "errors": errors
            }
        },
        status=status
    )