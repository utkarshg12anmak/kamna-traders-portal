#manage.py
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kamna_traders.settings")

    # 1) Determine environment
    env = os.getenv("DJANGO_ENV", "dev")

    # 2) Load base .env and then env-specific overrides
    BASE_DIR = Path(__file__).resolve().parent
    load_dotenv(BASE_DIR / f".env.{env}")

    # 3) Default runserver port
    if len(sys.argv) >= 2 and sys.argv[1] == "runserver":
        default_port = os.getenv("RUNSERVER_PORT", "8002")
        if len(sys.argv) == 2:
            sys.argv.append(default_port)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)