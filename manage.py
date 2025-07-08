#manage.py
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kamna_traders.settings")

    # 1) Determine environment (defaults to "dev")
    env = os.getenv("DJANGO_ENV", "dev")

    # 2) Load the right .env file (e.g. .env.dev / .env.production)
    BASE_DIR = Path(__file__).resolve().parent
    load_dotenv(BASE_DIR / f".env.{env}")

    # 3) Default runserver port if none is specified
    if len(sys.argv) >= 2 and sys.argv[1] == "runserver" and len(sys.argv) == 2:
        default_port = os.getenv("RUNSERVER_PORT", "8002")
        sys.argv.append(default_port)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
