from rest_framework.response import Response

def api_response(data=None, message="OK", status_code=200):
    """
    Универсальный формат ответа API
    """
    return Response({
        "status": status_code,
        "message": message,
        "data": data
    }, status=status_code)
