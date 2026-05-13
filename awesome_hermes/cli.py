"""Command-line interface for Awesome Hermes."""

import argparse
import sys
from awesome_hermes import SkillCatalog


def main():
    parser = argparse.ArgumentParser(
        prog="awesome-hermes",
        description="Awesome Hermes - Curated collection of Hermes Agent skills.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  awesome-hermes list
  awesome-hermes search "python"
  awesome-hermes show repomix
  awesome-hermes recommend "I need to manage tasks"
  awesome-hermes mark-installed stack /tmp/peter1/stack
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list command
    list_parser = subparsers.add_parser("list", help="List all skills")
    list_parser.add_argument(
        "--category",
        help="Filter by category (dev-tools, task-management, analysis, meta, other)",
    )

    # search command
    search_parser = subparsers.add_parser("search", help="Search skills")
    search_parser.add_argument("query", help="Search keyword")

    # show command
    show_parser = subparsers.add_parser("show", help="Show skill details")
    show_parser.add_argument("name", help="Skill name")

    # recommend command
    recommend_parser = subparsers.add_parser("recommend", help="Recommend skills")
    recommend_parser.add_argument("description", help="Task description")

    # mark-installed command
    mark_parser = subparsers.add_parser("mark-installed", help="Mark skill as installed")
    mark_parser.add_argument("name", help="Skill name")
    mark_parser.add_argument("path", nargs="?", default="", help="Installation path")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    catalog = SkillCatalog()

    if args.command == "list":
        category_filter = args.category
        skills = catalog.list_all()
        if category_filter:
            skills = [s for s in skills if s.category == category_filter]
        
        if not skills:
            print("No skills found.")
            return
        
        for s in skills:
            status = "✅" if s.installed else "⬜"
            print(f"{status} {s.name} [{s.category}]")
            print(f"   {s.description}")
            if s.repo_url:
                print(f"   Repo: {s.repo_url}")
            if s.installed_path:
                print(f"   Path: {s.installed_path}")
            print()

    elif args.command == "search":
        results = catalog.search(args.query)
        if not results:
            print(f"No results for '{args.query}'.")
            return
        for s in results:
            status = "✅" if s.installed else "⬜"
            print(f"{status} {s.name} - {s.description}")

    elif args.command == "show":
        skill = catalog.get_skill(args.name)
        if not skill:
            print(f"Skill '{args.name}' not found.")
            sys.exit(1)
        
        status = "Installed" if skill.installed else "Not installed"
        print(f"Name: {skill.name}")
        print(f"Description: {skill.description}")
        print(f"Category: {skill.category}")
        print(f"Status: {status}")
        if skill.repo_url:
            print(f"Repository: {skill.repo_url}")
        if skill.installed_path:
            print(f"Installed at: {skill.installed_path}")

    elif args.command == "recommend":
        recommendations = catalog.recommend(args.description)
        if not recommendations:
            print("No recommendations found. Try a different description.")
            return
        print(f"Recommended skills for: {args.description}")
        print()
        for s in recommendations:
            status = "✅" if s.installed else "⬜"
            print(f"{status} {s.name} [{s.category}]")
            print(f"   {s.description}")
            print()

    elif args.command == "mark-installed":
        catalog.mark_installed(args.name, args.path)
        print(f"Marked '{args.name}' as installed.")


if __name__ == "__main__":
    main()
