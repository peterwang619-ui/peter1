"""Command-line interface for Hindsight."""

import argparse
import sys
from pathlib import Path

from hindsight import search_sessions, list_sessions, save_memory, load_memory


def main():
    parser = argparse.ArgumentParser(
        prog="hindsight",
        description="Hindsight - Retrospective analysis and memory management.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  hindsight list
  hindsight search "python"
  hindsight memory get mykey
  hindsight memory set mykey myvalue
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list command
    list_parser = subparsers.add_parser("list", help="List recent sessions")
    list_parser.add_argument("--limit", type=int, default=10, help="Max sessions to show")

    # search command
    search_parser = subparsers.add_parser("search", help="Search sessions")
    search_parser.add_argument("query", help="Search keyword")
    search_parser.add_argument("--limit", type=int, default=10, help="Max results")

    # memory command
    memory_parser = subparsers.add_parser("memory", help="Memory management")
    memory_sub = memory_parser.add_subparsers(dest="memory_cmd")

    memory_get = memory_sub.add_parser("get", help="Get memory value")
    memory_get.add_argument("key", help="Memory key")

    memory_set = memory_sub.add_parser("set", help="Set memory value")
    memory_set.add_argument("key", help="Memory key")
    memory_set.add_argument("value", help="Memory value")

    memory_delete = memory_sub.add_parser("delete", help="Delete memory entry")
    memory_delete.add_argument("key", help="Memory key")

    memory_list = memory_sub.add_parser("list", help="List all memory keys")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "list":
        sessions = list_sessions(args.limit)
        if not sessions:
            print("No sessions found.")
            return
        for s in sessions:
            print(f"[{s['id']}] {s['title']} - {s['timestamp']}")
            print(f"  {s['preview']}...")
            print()

    elif args.command == "search":
        results = search_sessions(args.query, args.limit)
        if not results:
            print(f"No results for '{args.query}'.")
            return
        for r in results:
            print(f"[{r['id']}] {r['title']} - {r['timestamp']}")
            print(f"  {r['preview']}...")
            print()

    elif args.command == "memory":
        if not args.memory_cmd:
            memory_parser.print_help()
            sys.exit(0)

        if args.memory_cmd == "get":
            value = load_memory(args.key)
            if value is None:
                print(f"Key '{args.key}' not found.")
            else:
                print(json.dumps(value, indent=2))

        elif args.memory_cmd == "set":
            success = save_memory(args.key, args.value)
            print("Saved." if success else "Failed to save.")

        elif args.memory_cmd == "delete":
            success = delete_memory(args.key)
            print("Deleted." if success else "Key not found.")

        elif args.memory_cmd == "list":
            data = load_memory()
            if not data:
                print("No memory entries.")
            else:
                for k in data:
                    print(k)


if __name__ == "__main__":
    main()
