# main.py

import sys
import os

# اضافه کردن مسیر پروژه به PYTHONPATH
sys.path.append(os.path.dirname(__file__))

# ایمپورت کردن توابع
from app.commands.autoclose_overdue import autoclose_overdue_command
from app.cli.console import run_test_cli
from app.commands.project import project_help


def main():
    """
    Main entry point for running commands and CLI.
    Example usage:
        python main.py tasks:autoclose-overdue
        python main.py run:cli
        python main.py project help
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <command>")
        print("Available commands: tasks:autoclose-overdue | run:cli | project help")
        sys.exit(1)

    command = sys.argv[1]

    # اجرای کامندها
    if command == "tasks:autoclose-overdue":
        autoclose_overdue_command()

    elif command == "run:cli":
        run_test_cli()

    elif command == "project":
        # اگر فقط project زده شده
        if len(sys.argv) == 2:
            print("Usage: python main.py project help")
            sys.exit(0)

        subcommand = sys.argv[2]

        if subcommand == "help":
            project_help()
        else:
            print(f"Unknown project command: '{subcommand}'")
            print("Try: python main.py project help")

    else:
        print(f"Error: Unknown command '{command}'")


if __name__ == "__main__":
    main()
