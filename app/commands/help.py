def show_help():
    """Display TodoList commands"""
    print("\n" + "="*60)
    print("TodoList Commands")
    print("="*60)
    
    print("\nProject Commands:")
    print("  python main.py project create <name> [description]")
    print("    -> Create a new project")
    print("  python main.py project list")
    print("    -> List all projects")
    print("  python main.py project delete <project_id>")
    print("    -> Delete a project (tasks will be automatically deleted)")
    print("  python main.py project show <project_id>")
    print("    -> Show project details and its tasks")
    
    print("\nTask Commands:")
    print("  python main.py task create <title> <project_id> [description] [deadline]")
    print("    -> Create a new task")
    print("    -> deadline format: YYYY-MM-DD or YYYY-MM-DD HH:MM")
    print("  python main.py task list [project_id]")
    print("    -> List all tasks (or tasks of a specific project)")
    print("  python main.py task update-status <task_id> <status>")
    print("    -> Update task status")
    print("    -> status can be: todo, doing, done")
    print("  python main.py task delete <task_id>")
    print("    -> Delete a task")
    print("  python main.py task show <task_id>")
    print("    -> Show task details")
    
    print("\nScheduling Commands:")
    print("  python main.py task schedule <task_id> <deadline>")
    print("    -> Set or update task deadline")
    print("    -> deadline format: YYYY-MM-DD or YYYY-MM-DD HH:MM")
    print("  python main.py tasks:autoclose-overdue")
    print("    -> Automatically close overdue tasks that are still open")
    
    print("\nHelp Commands:")
    print("  python main.py help")
    print("    -> Show this command list")
    
    print("\n" + "="*60 + "\n")

