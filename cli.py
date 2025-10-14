from .storage import InMemoryStorage
from .services import ToDoService

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
  project-delete <id>
  task-add <project_id> <title> [desc] [deadline]
  task-list <project_id>
""")

        elif cmd.startswith("project-create"):
            parts = cmd.split(" ", 2)
            name = parts[1] if len(parts) > 1 else input("Project name: ")
            desc = parts[2] if len(parts) > 2 else ""
            p = service.create_project(name, desc)
            print(f"Created project: {p.name} (id={p.id[:8]})")

        elif cmd == "project-list":
            projects = service.list_projects()
            if not projects:
                print("No projects yet.")
            else:
                for p in projects:
                    print(f"{p.id[:8]} - {p.name} - {p.description}")

        elif cmd.startswith("project-delete"):
            parts = cmd.split(" ", 1)
            if len(parts) < 2:
                print("Usage: project-delete <id>")
            else:
                service.delete_project(parts[1])
                print("Project deleted.")

        elif cmd.startswith("task-add"):
            parts = cmd.split(" ", 3)
            if len(parts) < 3:
                print("Usage: task-add <project_id> <title>")
            else:
                project_id, title = parts[1], parts[2]
                desc = input("Description: ")
                deadline = input("Deadline: ")
                t = service.add_task(project_id, title, desc, deadline)
                print(f"Added task: {t.title} (status={t.status})")

        elif cmd.startswith("task-list"):
            parts = cmd.split(" ", 1)
            if len(parts) < 2:
                print("Usage: task-list <project_id>")
            else:
                tasks = service.list_tasks(parts[1])
                if not tasks:
                    print("No tasks.")
                else:
                    for t in tasks:
                        print(f"{t.id[:8]} - {t.title} [{t.status}]")

        else:
            print("Unknown command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
