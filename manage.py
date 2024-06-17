import os
import sys

from django.core.management import execute_from_command_line
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amocrm_proj.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Use PORT environment variable if set, otherwise default to 8000
    port = os.environ.get('PORT', '8000')
    execute_from_command_line([sys.argv[0], 'runserver', '0.0.0.0:' + port])


if __name__ == '__main__':
    main()
