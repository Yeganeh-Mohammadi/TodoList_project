import argparse
from .storage import InMemoryStorage
from .services import ToDoService

def main():
    storage = InMemoryStorage()
    service = ToDoService(storage)

    parser = argparse.ArgumentParser(description="Simple ToDo List CLI")
    subparsers = parser.add_subparsers(dest="command")

    #  Project commands 
    create_proj = subparsers.add_parser("project-create", help="Create a new project")
    create_proj.add_argument("--name", required=True)
    create_proj.add_argument("--desc", default="")

    list_proj = subparsers.add_parser("project-list", help="List all projects")

    delete_proj = subparsers.add_parser("project-delete", help="Delete a project by ID")
    delete_proj.add_argument("--id", required=True)

    #  Task commands 
    add_task = subparsers.add_parser("task-add", help="Add a new task to a project")
    add_task.add_argument("--project-id", required=True)
    add_task.add_argument("--title", required=True)
    add_task.add_argument("--desc", default="")
    add_task.add_argument("--deadline", default="")

    list_task = subparsers.add_parser("task-list", help="List all tasks of a project")
    list_task.add_argument("--project-id", required=True)

    args = parser.parse_args()

    if args.command == "project-create":
        p = service.create_project(args.name, args.desc)
        print(f"Created project: {p.name} (id={p.id})")

    elif args.command == "project-list":
        projects = service.list_projects()
        if not projects:
            print("No projects yet.")
        for p in projects:
            print(f"{p.id} - {p.name} - {p.description}")

    elif args.command == "project-delete":
        service.delete_project(args.id)
        print("Project deleted.")

    elif args.command == "task-add":
        t = service.add_task(args.project_id, args.title, args.desc, args.deadline)
        print(f"Added task: {t.title} (status={t.status})")

    elif args.command == "task-list":
        tasks = service.list_tasks(args.project_id)
        if not tasks:
            print("No tasks.")
        for t in tasks:
            print(f"{t.id} - {t.title} [{t.status}] (deadline: {t.deadline or '—'})")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

