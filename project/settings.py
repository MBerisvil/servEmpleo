MIDDLEWARE = [
    # ... otros middleware ...
    'seapp.middleware.TimingMiddleware',
]

# Mejoras de seguridad
SECURE_SSL_REDIRECT = True  # Solo en producción
SECURE_BROWSER_XSS_FILTER = True
CONN_MAX_AGE = 60 