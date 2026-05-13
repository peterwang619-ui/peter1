"""Command-line interface for TokScale."""

import argparse
import sys
from pathlib import Path

from tokscale import __version__
from tokscale.counter import count_tokens, estimate_context


def main():
    parser = argparse.ArgumentParser(
        prog="tokscale",
        description="TokScale - Token scaling and estimation tool for LLM context management.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tokscale count "Hello, world!"
  tokscale count file.txt
  tokscale count file.txt --encoding p50k_base
  tokscale estimate large_file.py
        """,
    )
    parser.add_argument("--version", action="version", version=f"tokscale {__version__}")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # count command
    count_parser = subparsers.add_parser("count", help="Count tokens in text or file")
    count_parser.add_argument("input", help="Text string or file path")
    count_parser.add_argument(
        "--encoding",
        default="cl100k_base",
        help="Token encoding (default: cl100k_base)",
    )

    # estimate command
    estimate_parser = subparsers.add_parser("estimate", help="Estimate context usage for a file")
    estimate_parser.add_argument("file", help="File path to analyze")
    estimate_parser.add_argument(
        "--encoding",
        default="cl100k_base",
        help="Token encoding (default: cl100k_base)",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "count":
        path = Path(args.input)
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            token_count = count_tokens(text, args.encoding)
            print(f"File: {args.input}")
            print(f"Tokens ({args.encoding}): {token_count}")
        else:
            token_count = count_tokens(args.input, args.encoding)
            print(f"Text: {args.input}")
            print(f"Tokens ({args.encoding}): {token_count}")

    elif args.command == "estimate":
        result = estimate_context(args.file, args.encoding)
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        print(f"File: {result['file']}")
        print(f"Characters: {result['characters']}")
        print(f"Tokens ({result['encoding']}): {result['tokens']}")
        print(f"Context usage: {result['context_usage_pct']}%")


if __name__ == "__main__":
    main()
