import os
import sys
import django
from django.core.management import execute_from_command_line

def run_migrations():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyWeb.settings')
    django.setup()
    
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Collect static files with WhiteNoise
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])

if __name__ == '__main__':
    run_migrations() 