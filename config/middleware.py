class ProxyMiddleware:
    """
    Middleware to resolve the client IP address when behind a reverse proxy.
    It takes the first IP from HTTP_X_FORWARDED_FOR and sets it as REMOTE_ADDR.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # X-Forwarded-For can be a comma-separated list of IPs.
            # The client IP is the first one.
            ip = x_forwarded_for.split(',')[0].strip()
            request.META['REMOTE_ADDR'] = ip
        return self.get_response(request)

class SecurityHeadersMiddleware:
    """
    Middleware to add security headers to every response,
    including Content-Security-Policy (CSP) and Permissions-Policy.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Content-Security-Policy (CSP)
        # Note: 'unsafe-inline' is often required by rich text editors (TinyMCE) and some framework scripts.
        # 'unsafe-eval' might be needed by some third-party JS.
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://code.jquery.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://www.google.com https://www.gstatic.com",
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com",
            "img-src 'self' data: https: http:",
            "font-src 'self' data: https://cdnjs.cloudflare.com https://fonts.gstatic.com",
            "connect-src 'self' https://generativelanguage.googleapis.com https://www.google-analytics.com",
            "frame-src 'self' https://www.youtube.com https://www.google.com",
            "media-src 'self' https://www.youtube.com",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
        ]
        response['Content-Security-Policy'] = "; ".join(csp_directives)

        # Permissions-Policy (replaces Feature-Policy)
        permissions_policy = (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(), "
            "usb=()"
        )
        response['Permissions-Policy'] = permissions_policy

        # Ensure these are always set even if Django's SecurityMiddleware misses them in some edge cases
        if not response.has_header('X-Content-Type-Options'):
            response['X-Content-Type-Options'] = 'nosniff'
            
        if not response.has_header('X-Frame-Options'):
            response['X-Frame-Options'] = 'DENY'
            
        if not response.has_header('Referrer-Policy'):
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        return response
