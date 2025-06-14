#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Импорт и очистка сессий после инициализации окружения
    import django
    django.setup()  # Инициализация Django
    from django.contrib.sessions.models import Session
    from django.utils import timezone
    Session.objects.filter(expire_date__lt=timezone.now()).delete()

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()