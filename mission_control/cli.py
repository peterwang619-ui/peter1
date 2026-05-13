"""Command-line interface for Mission Control."""

import argparse
import sys
from mission_control import TaskManager, TaskStatus, Scheduler


def main():
    parser = argparse.ArgumentParser(
        prog="mission-control",
        description="Mission Control - Command center for tasks, agents, and workflows.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mission-control list
  mission-control create "Deploy service" --description "Deploy to prod"
  mission-control status <task-id>
  mission-control complete <task-id>
  mission-control delete <task-id>
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--status",
        choices=[s.value for s in TaskStatus],
        help="Filter by status",
    )

    # create command
    create_parser = subparsers.add_parser("create", help="Create a new task")
    create_parser.add_argument("name", help="Task name")
    create_parser.add_argument("--description", default="", help="Task description")

    # status command
    status_parser = subparsers.add_parser("status", help="Show task status")
    status_parser.add_argument("task_id", help="Task ID")

    # complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task as completed")
    complete_parser.add_argument("task_id", help="Task ID")

    # cancel command
    cancel_parser = subparsers.add_parser("cancel", help="Cancel a task")
    cancel_parser.add_argument("task_id", help="Task ID")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", help="Task ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    manager = TaskManager()

    if args.command == "list":
        status_filter = TaskStatus(args.status) if args.status else None
        tasks = manager.list_tasks(status_filter)
        if not tasks:
            print("No tasks found.")
            return
        for t in tasks:
            status_icon = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.RUNNING: "🔄",
                TaskStatus.COMPLETED: "✅",
                TaskStatus.FAILED: "❌",
                TaskStatus.CANCELLED: "🚫",
            }.get(t.status, "❓")
            print(f"{status_icon} [{t.id}] {t.name} - {t.status.value}")
            if t.description:
                print(f"   {t.description}")
            print()

    elif args.command == "create":
        task = manager.create_task(args.name, args.description)
        print(f"Created task [{task.id}]: {task.name}")

    elif args.command == "status":
        task = manager.get_task(args.task_id)
        if not task:
            print(f"Task '{args.task_id}' not found.")
            sys.exit(1)
        print(f"Task: {task.name}")
        print(f"ID: {task.id}")
        print(f"Status: {task.status.value}")
        print(f"Created: {task.created_at}")
        if task.started_at:
            print(f"Started: {task.started_at}")
        if task.completed_at:
            print(f"Completed: {task.completed_at}")
        if task.error:
            print(f"Error: {task.error}")
        if task.result:
            print(f"Result: {task.result}")

    elif args.command == "complete":
        success = manager.complete_task(args.task_id)
        print("Task completed." if success else "Task not found.")

    elif args.command == "cancel":
        success = manager.update_task_status(args.task_id, TaskStatus.CANCELLED)
        print("Task cancelled." if success else "Task not found.")

    elif args.command == "delete":
        success = manager.delete_task(args.task_id)
        print("Task deleted." if success else "Task not found.")


if __name__ == "__main__":
    main()
