from storage import InMemoryStorage
from services import ToDoService

def main():
    storage = InMemoryStorage()
    service = ToDoService(storage)

    print(" Welcome to ToDo CLI (In-Memory Mode)")
    print("Type 'help' to see commands, 'exit' to quit.")

    while True:
        cmd = input("\n> ").strip()

        if cmd == "exit":
            print("Bye!")
            break

        elif cmd == "help":
            print("""
Commands:
  project-create <name> [desc]
  project-list
  project-delete <name_or_id>
  task-add <project_name_or_id> <title> [desc] [deadline]
  task-list <project_name_or_id>
  task-status <project_name_or_id> <task_id_or_title> <new_status>
  task-delete <project_name_or_id> <task_id_or_title> # NEW Command
""")

        elif cmd.startswith("project-create"):
            parts = cmd.split(" ", 2)
            name = parts[1] if len(parts) > 1 else input("Project name: ")
            desc = parts[2] if len(parts) > 2 else ""
            try:
                p = service.create_project(name, desc)
                print(f"Created project: {p.name} (id={p.id[:8]})")
            except ValueError as e:
                print(f"Error: {e}")

        elif cmd == "project-list":
            projects = service.list_projects()
            if not projects:
                # AC (8) - Appropriate message [cite: 115]
                print("No projects yet.")
            else:
                for p in projects:
                    # AC (8) - Display ID, Name, Description [cite: 114]
                    print(f"{p.id[:8]} - {p.name} - {p.description}")

        elif cmd.startswith("project-delete"):
            parts = cmd.split(" ", 1)
            if len(parts) < 2:
                print("Usage: project-delete <name_or_id>")
            else:
                try:
                    service.delete_project(parts[1])
                    # AC (3) - Appropriate success message [cite: 74]
                    print("Project and its tasks deleted successfully.")
                except ValueError as e:
                    print(f"Error: {e}")

        elif cmd.startswith("task-add"):
            # Fixed logic to support [desc] and [deadline] from command line
            parts = cmd.split(" ", 5) 
            
            if len(parts) < 3:
                print("Usage: task-add <project_name_or_id> <title> [description] [deadline]")
            else:
                project_identifier = parts[1]
                title = parts[2]
                desc = parts[3] if len(parts) > 3 else ""
                deadline = parts[4] if len(parts) > 4 else ""
                
                try:
                    t = service.add_task(project_identifier, title, desc, deadline)
                    # AC (4) - Default status is 'todo' and is displayed [cite: 87]
                    print(f"Added task: {t.title} (status={t.status.upper()})")
                except ValueError as e:
                    print(f"Error: {e}")

        elif cmd.startswith("task-list"):
            parts = cmd.split(" ", 1)
            if len(parts) < 2:
                print("Usage: task-list <project_name_or_id>")
            else:
                project_identifier = parts[1]
                try:
                    tasks = service.list_tasks(project_identifier)
                    if not tasks:
                        # AC (9) - Appropriate message [cite: 126]
                        print("No tasks in this project.")
                    else:
                        for t in tasks:
                            # AC (9) - Display ID, Title, Status, Deadline [cite: 125]
                            print(f"[{t.status.upper()}] {t.id[:8]} - {t.title} (Deadline: {t.deadline or '—'})")
                except ValueError as e:
                    print(f"Error: {e}")


        elif cmd.startswith("task-status"):
            parts = cmd.split(" ", 3)
            if len(parts) < 4:
                print("Usage: task-status <project_name_or_id> <task_id_or_title> <new_status> (e.g., todo, doing, done)")
            else:
                project_identifier, task_identifier, new_status = parts[1], parts[2], parts[3]
                try:
                    t = service.update_task_status(project_identifier, task_identifier, new_status)
                    print(f"Updated task: {t.title} to status [{t.status.upper()}]")
                except ValueError as e:
                    print(f"Error: {e}")
                    
        # NEW: task-delete implementation (AC 7) 
        elif cmd.startswith("task-delete"):
            parts = cmd.split(" ", 2)
            if len(parts) < 3:
                print("Usage: task-delete <project_name_or_id> <task_id_or_title>")
            else:
                project_identifier, task_identifier = parts[1], parts[2]
                try:
                    service.delete_task(project_identifier, task_identifier)
                    # AC (7) - Appropriate success message [cite: 109]
                    print(f"Task '{task_identifier}' deleted successfully.")
                except ValueError as e:
                    print(f"Error: {e}")

        else:
            print("Unknown command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()