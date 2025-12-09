# main.py

import sys
import os

# اضافه کردن مسیر پروژه به PYTHONPATH
sys.path.append(os.path.dirname(__file__))

# ایمپورت کردن توابع
from app.commands.autoclose_overdue import autoclose_overdue_command
from app.cli.console import run_test_cli
from app.commands.help import show_help
from app.commands.project import (
    project_help, project_create, project_list, 
    project_delete, project_show
)
from app.commands.task import (
    task_create, task_list, task_update_status,
    task_delete, task_show, task_schedule
)


def main():
    """
    Main entry point for running commands and CLI.
    """
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    command = sys.argv[1]

    # دستور help
    if command == "help":
        show_help()
        return

    # اجرای کامندها
    if command == "tasks:autoclose-overdue":
        autoclose_overdue_command()

    elif command == "run:cli":
        run_test_cli()

    elif command == "project":
        if len(sys.argv) < 3:
            project_help()
            return

        subcommand = sys.argv[2]

        if subcommand == "help":
            project_help()
        elif subcommand == "create":
            if len(sys.argv) < 4:
                print("Error: Project name is required")
                print("Usage: python main.py project create <name> [description]")
                return
            name = sys.argv[3]
            description = sys.argv[4] if len(sys.argv) > 4 else None
            project_create(name, description)
        elif subcommand == "list":
            project_list()
        elif subcommand == "delete":
            if len(sys.argv) < 4:
                print("Error: project_id is required")
                print("Usage: python main.py project delete <project_id>")
                return
            project_id = int(sys.argv[3])
            project_delete(project_id)
        elif subcommand == "show":
            if len(sys.argv) < 4:
                print("Error: project_id is required")
                print("Usage: python main.py project show <project_id>")
                return
            project_id = int(sys.argv[3])
            project_show(project_id)
        else:
            print(f"Error: Invalid command: '{subcommand}'")
            print("For available commands: python main.py project help")

    elif command == "task":
        if len(sys.argv) < 3:
            print("Error: task command requires a subcommand")
            print("For available commands: python main.py help")
            return

        subcommand = sys.argv[2]

        if subcommand == "create":
            if len(sys.argv) < 5:
                print("Error: title and project_id are required")
                print("Usage: python main.py task create <title> <project_id> [description] [deadline]")
                return
            title = sys.argv[3]
            project_id = int(sys.argv[4])
            description = sys.argv[5] if len(sys.argv) > 5 else None
            deadline = sys.argv[6] if len(sys.argv) > 6 else None
            task_create(title, project_id, description, deadline)
        elif subcommand == "list":
            project_id = int(sys.argv[3]) if len(sys.argv) > 3 else None
            task_list(project_id)
        elif subcommand == "update-status":
            if len(sys.argv) < 5:
                print("Error: task_id and status are required")
                print("Usage: python main.py task update-status <task_id> <status>")
                print("   status can be: todo, doing, done")
                return
            task_id = int(sys.argv[3])
            status = sys.argv[4]
            task_update_status(task_id, status)
        elif subcommand == "delete":
            if len(sys.argv) < 4:
                print("Error: task_id is required")
                print("Usage: python main.py task delete <task_id>")
                return
            task_id = int(sys.argv[3])
            task_delete(task_id)
        elif subcommand == "show":
            if len(sys.argv) < 4:
                print("Error: task_id is required")
                print("Usage: python main.py task show <task_id>")
                return
            task_id = int(sys.argv[3])
            task_show(task_id)
        elif subcommand == "schedule":
            if len(sys.argv) < 5:
                print("Error: task_id and deadline are required")
                print("Usage: python main.py task schedule <task_id> <deadline>")
                print("   deadline format: YYYY-MM-DD or YYYY-MM-DD HH:MM")
                return
            task_id = int(sys.argv[3])
            deadline = sys.argv[4]
            task_schedule(task_id, deadline)
        else:
            print(f"Error: Invalid command: '{subcommand}'")
            print("For available commands: python main.py help")

    else:
        print(f"Error: Invalid command: '{command}'")
        print("For command list: python main.py help")


if __name__ == "__main__":
    main()
