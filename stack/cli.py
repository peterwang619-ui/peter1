"""Command-line interface for Stack."""

import argparse
import sys
from stack import StackManager


def main():
    parser = argparse.ArgumentParser(
        prog="stack",
        description="Stack - Go project stack management tool.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  stack list
  stack init myproject /path/to/myproject --module github.com/user/myproject
  stack build myproject
  stack run myproject --args "arg1 arg2"
  stack remove myproject
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list command
    list_parser = subparsers.add_parser("list", help="List all Go projects")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new Go project")
    init_parser.add_argument("name", help="Project name")
    init_parser.add_argument("path", help="Project path")
    init_parser.add_argument("--module", default="", help="Go module name")

    # build command
    build_parser = subparsers.add_parser("build", help="Build a Go project")
    build_parser.add_argument("name", help="Project name")

    # run command
    run_parser = subparsers.add_parser("run", help="Run a Go project")
    run_parser.add_argument("name", help="Project name")
    run_parser.add_argument("--args", default="", help="Arguments to pass to the program")

    # remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a project")
    remove_parser.add_argument("name", help="Project name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    manager = StackManager()

    if args.command == "list":
        projects = manager.list_projects()
        if not projects:
            print("No Go projects in stack.")
            return
        for p in projects:
            print(f"{p.name}")
            print(f"  Path: {p.path}")
            print(f"  Module: {p.module}")
            print()

    elif args.command == "init":
        project = manager.init_project(args.name, args.path, args.module)
        print(f"Initialized Go project '{project.name}' at {project.path}")
        print(f"Module: {project.module}")

    elif args.command == "build":
        result = manager.build_project(args.name)
        if result["success"]:
            print(f"Build successful for '{args.name}'.")
            if result.get("output"):
                print(result["output"])
        else:
            print(f"Build failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)

    elif args.command == "run":
        args_list = args.args.split() if args.args else None
        result = manager.run_project(args.name, args_list)
        if result["success"]:
            if result.get("output"):
                print(result["output"])
        else:
            print(f"Run failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)

    elif args.command == "remove":
        success = manager.remove_project(args.name)
        if success:
            print(f"Removed project '{args.name}'.")
        else:
            print(f"Project '{args.name}' not found.")
            sys.exit(1)


if __name__ == "__main__":
    main()
