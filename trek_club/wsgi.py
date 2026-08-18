import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trek_club.settings')

application = get_wsgi_application()

# Run database migrations automatically on server startup
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception as e:
    print(f"Startup migration failed: {e}")