"""Command-line interface for Hermes Workspace."""

import argparse
import sys
from hermes_workspace import WorkspaceManager


def main():
    parser = argparse.ArgumentParser(
        prog="hermes-workspace",
        description="Hermes Workspace - Multi-project workspace manager.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  hermes-workspace list
  hermes-workspace add myproject /path/to/myproject --description "My awesome project"
  hermes-workspace switch myproject
  hermes-workspace remove myproject
  hermes-workspace current
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list command
    list_parser = subparsers.add_parser("list", help="List all projects")

    # add command
    add_parser = subparsers.add_parser("add", help="Add a new project")
    add_parser.add_argument("name", help="Project name")
    add_parser.add_argument("path", help="Project path")
    add_parser.add_argument("--description", default="", help="Project description")

    # switch command
    switch_parser = subparsers.add_parser("switch", help="Switch to a project")
    switch_parser.add_argument("name", help="Project name")

    # remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a project")
    remove_parser.add_argument("name", help="Project name")

    # current command
    current_parser = subparsers.add_parser("current", help="Show current project")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    wm = WorkspaceManager()

    if args.command == "list":
        projects = wm.list_projects()
        if not projects:
            print("No projects in workspace.")
            return
        current = wm.current_project
        for p in projects:
            marker = " (current)" if p.name == current else ""
            print(f"{p.name}{marker}")
            print(f"  Path: {p.path}")
            if p.description:
                print(f"  Description: {p.description}")
            print()

    elif args.command == "add":
        project = wm.add_project(args.name, args.path, args.description)
        print(f"Added project '{project.name}' at {project.path}")

    elif args.command == "switch":
        success = wm.switch_project(args.name)
        if success:
            print(f"Switched to project '{args.name}'.")
        else:
            print(f"Project '{args.name}' not found.")
            sys.exit(1)

    elif args.command == "remove":
        success = wm.remove_project(args.name)
        if success:
            print(f"Removed project '{args.name}'.")
        else:
            print(f"Project '{args.name}' not found.")
            sys.exit(1)

    elif args.command == "current":
        project = wm.get_current_project()
        if project:
            print(f"Current project: {project.name}")
            print(f"Path: {project.path}")
        else:
            print("No current project set.")


if __name__ == "__main__":
    main()
