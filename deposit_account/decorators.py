from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def error_catch(func):
    @wraps(func)
    def wrapper_error_catch(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return wrapper_error_catch