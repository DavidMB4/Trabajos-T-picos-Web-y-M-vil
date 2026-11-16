from django.http import HttpResponse


class CorsMiddleware:
    """
    Middleware para permitir peticiones entre origenes distintos (CORS).
    Necesario cuando el frontend de Flutter corre en navegador web (Chrome)
    en un puerto distinto al del backend de Django.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Responder preflight OPTIONS para navegadores web
        if request.method == "OPTIONS":
            response = HttpResponse()
            response["Content-Length"] = "0"
        else:
            response = self.get_response(request)

        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        response["Access-Control-Max-Age"] = "86400"
        return response
